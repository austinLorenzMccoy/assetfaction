"""
Income distribution and rewards API routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional

from database.database import get_db
from models.models import User, Asset, IncomeDistribution, IncomePayout, Holding
from schemas.schemas import (
    IncomeDistributionRequest, IncomeDistributionResponse, 
    IncomePayoutResponse, APIResponse
)
from services.scheduler import scheduler
from utils.auth import get_current_user

router = APIRouter()


@router.post("/schedule", response_model=APIResponse)
async def schedule_income_distribution(
    request: IncomeDistributionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Schedule income distribution for an asset"""
    try:
        # Verify asset exists and user is the creator
        asset = db.query(Asset).filter(Asset.id == request.asset_id).first()
        
        if not asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asset not found"
            )
        
        if asset.creator_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only asset creator can schedule income distributions"
            )
        
        # Validate distribution date is in the future
        if request.distribution_date <= datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Distribution date must be in the future"
            )
        
        # Create income distribution record
        distribution = IncomeDistribution(
            asset_id=request.asset_id,
            total_income=request.total_income,
            distribution_date=request.distribution_date,
            status="scheduled"
        )
        db.add(distribution)
        db.commit()
        db.refresh(distribution)
        
        # Schedule the distribution job
        success = scheduler.schedule_income_distribution(
            distribution_id=distribution.id,
            distribution_date=request.distribution_date
        )
        
        if not success:
            # Rollback if scheduling failed
            db.delete(distribution)
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to schedule income distribution"
            )
        
        return APIResponse(
            success=True,
            message="Income distribution scheduled successfully",
            data=IncomeDistributionResponse.from_orm(distribution)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/distributions", response_model=APIResponse)
async def list_income_distributions(
    asset_id: Optional[int] = None,
    status_filter: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List income distributions"""
    try:
        query = db.query(IncomeDistribution).join(Asset)
        
        if asset_id:
            query = query.filter(IncomeDistribution.asset_id == asset_id)
        
        if status_filter:
            query = query.filter(IncomeDistribution.status == status_filter)
        
        distributions = query.offset(skip).limit(limit).all()
        
        distributions_data = []
        for dist in distributions:
            distributions_data.append({
                **IncomeDistributionResponse.from_orm(dist).dict(),
                "asset_name": dist.asset.name,
                "asset_type": dist.asset.asset_type
            })
        
        return APIResponse(
            success=True,
            message="Income distributions retrieved",
            data={
                "distributions": distributions_data,
                "total": len(distributions_data)
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/distributions/{distribution_id}", response_model=APIResponse)
async def get_distribution_details(
    distribution_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific distribution"""
    try:
        distribution = db.query(IncomeDistribution).filter(
            IncomeDistribution.id == distribution_id
        ).first()
        
        if not distribution:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Distribution not found"
            )
        
        # Get payouts for this distribution
        payouts = db.query(IncomePayout).filter(
            IncomePayout.distribution_id == distribution_id
        ).join(User).all()
        
        payouts_data = []
        for payout in payouts:
            payouts_data.append({
                **IncomePayoutResponse.from_orm(payout).dict(),
                "wallet_id": payout.user.wallet_id,
                "user_name": payout.user.name
            })
        
        distribution_data = {
            **IncomeDistributionResponse.from_orm(distribution).dict(),
            "asset_name": distribution.asset.name,
            "asset_type": distribution.asset.asset_type,
            "payouts": payouts_data,
            "total_payouts": len(payouts_data),
            "successful_payouts": len([p for p in payouts if p.status == "success"]),
            "failed_payouts": len([p for p in payouts if p.status == "failed"])
        }
        
        return APIResponse(
            success=True,
            message="Distribution details retrieved",
            data=distribution_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/distributions/{distribution_id}/execute", response_model=APIResponse)
async def execute_distribution_now(
    distribution_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Execute income distribution immediately"""
    try:
        distribution = db.query(IncomeDistribution).filter(
            IncomeDistribution.id == distribution_id
        ).first()
        
        if not distribution:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Distribution not found"
            )
        
        # Verify user is the asset creator
        if distribution.asset.creator_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only asset creator can execute distributions"
            )
        
        if distribution.status != "scheduled":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Distribution is not in scheduled status"
            )
        
        # Execute distribution via scheduler
        from services.scheduler import scheduler
        await scheduler._execute_income_distribution(distribution_id)
        
        # Refresh distribution status
        db.refresh(distribution)
        
        return APIResponse(
            success=True,
            message="Distribution executed successfully",
            data={
                "distribution_id": distribution_id,
                "status": distribution.status
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/payouts/user/{wallet_id}", response_model=APIResponse)
async def get_user_payouts(
    wallet_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get income payouts for a specific user"""
    try:
        # Get user by wallet ID
        user = db.query(User).filter(User.wallet_id == wallet_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Get payouts for this user
        payouts = db.query(IncomePayout).filter(
            IncomePayout.user_id == user.id
        ).join(IncomeDistribution).join(Asset).offset(skip).limit(limit).all()
        
        payouts_data = []
        for payout in payouts:
            payouts_data.append({
                **IncomePayoutResponse.from_orm(payout).dict(),
                "asset_name": payout.distribution.asset.name,
                "asset_type": payout.distribution.asset.asset_type,
                "distribution_date": payout.distribution.distribution_date
            })
        
        # Calculate total earnings
        total_earnings = sum(payout.amount for payout in payouts if payout.status == "success")
        
        return APIResponse(
            success=True,
            message="User payouts retrieved",
            data={
                "wallet_id": wallet_id,
                "payouts": payouts_data,
                "total_payouts": len(payouts_data),
                "total_earnings": total_earnings
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/analytics/asset/{asset_id}", response_model=APIResponse)
async def get_asset_income_analytics(
    asset_id: int,
    db: Session = Depends(get_db)
):
    """Get income analytics for an asset"""
    try:
        asset = db.query(Asset).filter(Asset.id == asset_id).first()
        
        if not asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asset not found"
            )
        
        # Get all distributions for this asset
        distributions = db.query(IncomeDistribution).filter(
            IncomeDistribution.asset_id == asset_id
        ).all()
        
        # Calculate analytics
        total_distributed = sum(
            dist.total_income for dist in distributions 
            if dist.status == "completed"
        )
        
        total_scheduled = sum(
            dist.total_income for dist in distributions 
            if dist.status == "scheduled"
        )
        
        # Get token holders
        holdings = db.query(Holding).filter(
            Holding.asset_id == asset_id
        ).all()
        
        analytics_data = {
            "asset_id": asset_id,
            "asset_name": asset.name,
            "asset_valuation": asset.valuation,
            "total_supply": asset.total_supply,
            "tokens_in_circulation": sum(holding.amount for holding in holdings),
            "total_holders": len(holdings),
            "total_distributions": len(distributions),
            "completed_distributions": len([d for d in distributions if d.status == "completed"]),
            "total_income_distributed": total_distributed,
            "total_income_scheduled": total_scheduled,
            "average_distribution": total_distributed / len(distributions) if distributions else 0,
            "yield_percentage": (total_distributed / asset.valuation * 100) if asset.valuation > 0 else 0
        }
        
        return APIResponse(
            success=True,
            message="Asset analytics retrieved",
            data=analytics_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/scheduler/jobs", response_model=APIResponse)
async def get_scheduled_jobs(
    current_user: User = Depends(get_current_user)
):
    """Get list of scheduled jobs"""
    try:
        jobs = scheduler.get_scheduled_jobs()
        
        return APIResponse(
            success=True,
            message="Scheduled jobs retrieved",
            data={
                "jobs": jobs,
                "total": len(jobs),
                "scheduler_running": scheduler.running
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
