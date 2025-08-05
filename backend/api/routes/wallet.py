"""
Wallet management API routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any

from database.database import get_db
from models.models import User
from schemas.schemas import (
    WalletCreateRequest, WalletCreateResponse, UserResponse, APIResponse
)
from services.hedera_service import hedera_service
from utils.auth import get_current_user

router = APIRouter()


@router.post("/create", response_model=APIResponse)
async def create_sponsored_wallet(
    request: WalletCreateRequest,
    db: Session = Depends(get_db)
):
    """Create a new sponsored Hedera wallet"""
    try:
        # Check if wallet already exists
        existing_user = db.query(User).filter(
            User.public_key == request.public_key
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Wallet with this public key already exists"
            )
        
        # Create sponsored account on Hedera
        result = await hedera_service.create_sponsored_account(
            public_key=request.public_key,
            initial_balance=request.initial_balance
        )
        
        if result.get("status") != "success":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create Hedera account: {result.get('error')}"
            )
        
        # Store user in database
        user = User(
            wallet_id=result["account_id"],
            public_key=request.public_key,
            kyc_verified=False
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return APIResponse(
            success=True,
            message="Wallet created successfully",
            data=WalletCreateResponse(
                wallet_id=result["account_id"],
                public_key=request.public_key,
                transaction_id=result["transaction_id"],
                status="success"
            )
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/info/{wallet_id}", response_model=APIResponse)
async def get_wallet_info(
    wallet_id: str,
    db: Session = Depends(get_db)
):
    """Get wallet information"""
    try:
        # Get user from database
        user = db.query(User).filter(User.wallet_id == wallet_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wallet not found"
            )
        
        return APIResponse(
            success=True,
            message="Wallet information retrieved",
            data=UserResponse.from_orm(user)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/balance/{wallet_id}", response_model=APIResponse)
async def get_wallet_balance(wallet_id: str):
    """Get wallet HBAR balance from Mirror Node"""
    try:
        from services.mirror_service import mirror_service
        
        account_info = await mirror_service.get_account_info(wallet_id)
        
        if "error" in account_info:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get balance: {account_info['error']}"
            )
        
        balance_info = account_info.get("balance", {})
        
        return APIResponse(
            success=True,
            message="Balance retrieved successfully",
            data={
                "account_id": wallet_id,
                "balance": balance_info.get("balance", 0),
                "timestamp": balance_info.get("timestamp")
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/transfer", response_model=APIResponse)
async def transfer_hbar(
    transfer_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Transfer HBAR between accounts"""
    try:
        from_account = transfer_data.get("from_account")
        to_account = transfer_data.get("to_account")
        amount = transfer_data.get("amount")
        private_key = transfer_data.get("private_key")
        
        if not all([from_account, to_account, amount, private_key]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing required fields: from_account, to_account, amount, private_key"
            )
        
        # Execute transfer
        result = await hedera_service.transfer_hbar(
            from_account=from_account,
            to_account=to_account,
            amount=float(amount),
            private_key=private_key
        )
        
        if result.get("status") != "success":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Transfer failed: {result.get('error')}"
            )
        
        return APIResponse(
            success=True,
            message="Transfer completed successfully",
            data={
                "transaction_id": result["transaction_id"],
                "from_account": from_account,
                "to_account": to_account,
                "amount": amount
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/portfolio/{wallet_id}", response_model=APIResponse)
async def get_portfolio(wallet_id: str, db: Session = Depends(get_db)):
    """Get complete portfolio information for a wallet"""
    try:
        from services.mirror_service import mirror_service
        
        # Get user from database
        user = db.query(User).filter(User.wallet_id == wallet_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wallet not found"
            )
        
        # Get portfolio summary from Mirror Node
        portfolio = await mirror_service.get_portfolio_summary(wallet_id)
        
        if "error" in portfolio:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get portfolio: {portfolio['error']}"
            )
        
        # Get holdings from database
        from models.models import Holding, Asset
        holdings = db.query(Holding).filter(
            Holding.user_id == user.id
        ).join(Asset).all()
        
        portfolio_data = {
            "user_info": UserResponse.from_orm(user),
            "hbar_balance": portfolio.get("balance", 0),
            "token_balances": portfolio.get("tokens", []),
            "asset_holdings": [
                {
                    "asset_name": holding.asset.name,
                    "asset_type": holding.asset.asset_type,
                    "tokens_held": holding.amount,
                    "purchase_price": holding.purchase_price,
                    "current_value": holding.amount * (holding.asset.valuation / holding.asset.total_supply)
                }
                for holding in holdings
            ],
            "recent_transactions": portfolio.get("recent_transactions", [])
        }
        
        return APIResponse(
            success=True,
            message="Portfolio retrieved successfully",
            data=portfolio_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
