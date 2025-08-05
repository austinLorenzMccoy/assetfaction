"""
KYC management API routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database.database import get_db
from models.models import User, KYCSubmission
from schemas.schemas import (
    KYCSubmissionRequest, KYCSubmissionResponse, APIResponse
)
from services.hedera_service import hedera_service
from utils.auth import get_current_user

router = APIRouter()


@router.post("/submit", response_model=APIResponse)
async def submit_kyc(
    request: KYCSubmissionRequest,
    db: Session = Depends(get_db)
):
    """Submit KYC information and log to HCS"""
    try:
        # Get user by wallet ID
        user = db.query(User).filter(User.wallet_id == request.wallet_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wallet not found"
            )
        
        # Check if KYC already submitted
        existing_kyc = db.query(KYCSubmission).filter(
            KYCSubmission.user_id == user.id,
            KYCSubmission.verification_status.in_(["pending", "approved"])
        ).first()
        
        if existing_kyc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="KYC already submitted for this wallet"
            )
        
        # Submit KYC hash to HCS
        hcs_result = await hedera_service.submit_kyc_to_hcs(
            account_id=request.wallet_id,
            kyc_hash=request.document_hash
        )
        
        if hcs_result.get("status") != "success":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to submit to HCS: {hcs_result.get('error')}"
            )
        
        # Create KYC submission record
        kyc_submission = KYCSubmission(
            user_id=user.id,
            document_hash=request.document_hash,
            document_type=request.document_type,
            hcs_message_id=str(hcs_result["message_id"]),
            verification_status="pending"
        )
        db.add(kyc_submission)
        
        # Update user information
        user.name = request.name
        user.phone_number = request.phone_number
        user.kyc_hash = request.document_hash
        
        db.commit()
        db.refresh(kyc_submission)
        
        return APIResponse(
            success=True,
            message="KYC submitted successfully",
            data=KYCSubmissionResponse(
                submission_id=kyc_submission.id,
                hcs_message_id=kyc_submission.hcs_message_id,
                status=kyc_submission.verification_status,
                submitted_at=kyc_submission.submitted_at
            )
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/status/{wallet_id}", response_model=APIResponse)
async def get_kyc_status(
    wallet_id: str,
    db: Session = Depends(get_db)
):
    """Get KYC verification status for a wallet"""
    try:
        # Get user by wallet ID
        user = db.query(User).filter(User.wallet_id == wallet_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wallet not found"
            )
        
        # Get latest KYC submission
        kyc_submission = db.query(KYCSubmission).filter(
            KYCSubmission.user_id == user.id
        ).order_by(KYCSubmission.submitted_at.desc()).first()
        
        if not kyc_submission:
            return APIResponse(
                success=True,
                message="No KYC submission found",
                data={
                    "wallet_id": wallet_id,
                    "kyc_verified": False,
                    "status": "not_submitted"
                }
            )
        
        return APIResponse(
            success=True,
            message="KYC status retrieved",
            data={
                "wallet_id": wallet_id,
                "kyc_verified": user.kyc_verified,
                "status": kyc_submission.verification_status,
                "submitted_at": kyc_submission.submitted_at,
                "verified_at": kyc_submission.verified_at,
                "hcs_message_id": kyc_submission.hcs_message_id
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/verify/{submission_id}", response_model=APIResponse)
async def verify_kyc(
    submission_id: int,
    verification_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Verify KYC submission (admin only)"""
    try:
        # Get KYC submission
        kyc_submission = db.query(KYCSubmission).filter(
            KYCSubmission.id == submission_id
        ).first()
        
        if not kyc_submission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="KYC submission not found"
            )
        
        # Update verification status
        approved = verification_data.get("approved", False)
        kyc_submission.verification_status = "approved" if approved else "rejected"
        
        if approved:
            kyc_submission.verified_at = db.func.now()
            # Update user KYC status
            user = db.query(User).filter(User.id == kyc_submission.user_id).first()
            if user:
                user.kyc_verified = True
        
        db.commit()
        
        return APIResponse(
            success=True,
            message=f"KYC {'approved' if approved else 'rejected'} successfully",
            data={
                "submission_id": submission_id,
                "status": kyc_submission.verification_status,
                "verified_at": kyc_submission.verified_at
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/submissions", response_model=APIResponse)
async def list_kyc_submissions(
    status_filter: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List KYC submissions (admin only)"""
    try:
        query = db.query(KYCSubmission).join(User)
        
        if status_filter:
            query = query.filter(KYCSubmission.verification_status == status_filter)
        
        submissions = query.offset(skip).limit(limit).all()
        
        submissions_data = []
        for submission in submissions:
            submissions_data.append({
                "id": submission.id,
                "user_id": submission.user_id,
                "wallet_id": submission.user.wallet_id,
                "user_name": submission.user.name,
                "document_type": submission.document_type,
                "verification_status": submission.verification_status,
                "submitted_at": submission.submitted_at,
                "verified_at": submission.verified_at,
                "hcs_message_id": submission.hcs_message_id
            })
        
        return APIResponse(
            success=True,
            message="KYC submissions retrieved",
            data={
                "submissions": submissions_data,
                "total": len(submissions_data)
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/hcs-messages/{topic_id}", response_model=APIResponse)
async def get_kyc_hcs_messages(topic_id: str):
    """Get KYC messages from HCS topic"""
    try:
        from services.mirror_service import mirror_service
        
        messages = await mirror_service.get_topic_messages(
            topic_id=topic_id,
            limit=50
        )
        
        if "error" in messages:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get HCS messages: {messages['error']}"
            )
        
        return APIResponse(
            success=True,
            message="HCS messages retrieved",
            data=messages
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
