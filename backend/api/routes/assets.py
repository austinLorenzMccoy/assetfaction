"""
Asset tokenization API routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database.database import get_db
from models.models import User, Asset, Transaction
from schemas.schemas import (
    AssetTokenizeRequest, AssetTokenizeResponse, AssetResponse, APIResponse
)
from services.hedera_service import hedera_service
from utils.auth import get_current_user

router = APIRouter()


@router.post("/tokenize", response_model=APIResponse)
async def tokenize_asset(
    request: AssetTokenizeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Tokenize a real estate or art asset"""
    try:
        # Verify user is KYC verified
        if not current_user.kyc_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="KYC verification required to tokenize assets"
            )
        
        # Create NFT for the asset
        nft_name = f"{request.name} NFT"
        nft_symbol = f"{request.asset_type.upper()[:3]}{request.name[:3].upper()}"
        
        nft_metadata = {
            "name": request.name,
            "description": request.description,
            "asset_type": request.asset_type,
            "location": request.location,
            "valuation": request.valuation,
            "creator": current_user.wallet_id
        }
        
        # Add extra data if provided
        if request.extra_data:
            nft_metadata.update(request.extra_data)
        
        nft_result = await hedera_service.create_nft_token(
            name=nft_name,
            symbol=nft_symbol,
            metadata=nft_metadata
        )
        
        if nft_result.get("status") != "success":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create NFT: {nft_result.get('error')}"
            )
        
        # Create fungible token for fractional ownership
        ft_name = f"{request.name} Fractions"
        ft_symbol = f"F{nft_symbol}"
        
        ft_result = await hedera_service.create_fungible_token(
            name=ft_name,
            symbol=ft_symbol,
            supply=request.total_supply
        )
        
        if ft_result.get("status") != "success":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create fungible token: {ft_result.get('error')}"
            )
        
        # Store asset in database
        asset = Asset(
            nft_id=nft_result["token_id"],
            ft_id=ft_result["token_id"],
            asset_type=request.asset_type,
            name=request.name,
            description=request.description,
            location=request.location,
            valuation=request.valuation,
            total_supply=request.total_supply,
            extra_data=nft_metadata,
            creator_id=current_user.id,
            royalty_percentage=request.royalty_percentage
        )
        db.add(asset)
        db.flush()  # Get asset ID
        
        # Record transactions
        nft_transaction = Transaction(
            user_id=current_user.id,
            transaction_id=nft_result["transaction_id"],
            transaction_type="mint_nft",
            asset_id=asset.id,
            token_id=nft_result["token_id"],
            status="success",
            extra_data={"nft_id": nft_result["nft_id"]}
        )
        db.add(nft_transaction)
        
        ft_transaction = Transaction(
            user_id=current_user.id,
            transaction_id=ft_result["transaction_id"],
            transaction_type="mint_ft",
            asset_id=asset.id,
            amount=float(request.total_supply),
            token_id=ft_result["token_id"],
            status="success"
        )
        db.add(ft_transaction)
        
        db.commit()
        db.refresh(asset)
        
        return APIResponse(
            success=True,
            message="Asset tokenized successfully",
            data=AssetTokenizeResponse(
                asset_id=asset.id,
                nft_id=nft_result["token_id"],
                ft_id=ft_result["token_id"],
                name=asset.name,
                valuation=asset.valuation,
                total_supply=asset.total_supply,
                transaction_id=nft_result["transaction_id"],
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


@router.get("/list", response_model=APIResponse)
async def list_assets(
    asset_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all tokenized assets"""
    try:
        query = db.query(Asset)
        
        if asset_type:
            query = query.filter(Asset.asset_type == asset_type)
        
        assets = query.offset(skip).limit(limit).all()
        
        assets_data = [AssetResponse.from_orm(asset) for asset in assets]
        
        return APIResponse(
            success=True,
            message="Assets retrieved successfully",
            data={
                "assets": assets_data,
                "total": len(assets_data)
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/{asset_id}", response_model=APIResponse)
async def get_asset(
    asset_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed asset information"""
    try:
        asset = db.query(Asset).filter(Asset.id == asset_id).first()
        
        if not asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asset not found"
            )
        
        # Get token holders
        from models.models import Holding
        holdings = db.query(Holding).filter(
            Holding.asset_id == asset_id
        ).join(User).all()
        
        # Calculate ownership distribution
        total_held = sum(holding.amount for holding in holdings)
        ownership_distribution = []
        
        for holding in holdings:
            ownership_percentage = (holding.amount / asset.total_supply) * 100
            ownership_distribution.append({
                "wallet_id": holding.user.wallet_id,
                "tokens_held": holding.amount,
                "ownership_percentage": ownership_percentage,
                "purchase_price": holding.purchase_price
            })
        
        asset_data = {
            **AssetResponse.from_orm(asset).dict(),
            "tokens_in_circulation": total_held,
            "ownership_distribution": ownership_distribution,
            "creator_wallet": asset.creator.wallet_id if asset.creator else None
        }
        
        return APIResponse(
            success=True,
            message="Asset information retrieved",
            data=asset_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/{asset_id}/associate", response_model=APIResponse)
async def associate_token(
    asset_id: int,
    association_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Associate user with asset token"""
    try:
        asset = db.query(Asset).filter(Asset.id == asset_id).first()
        
        if not asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asset not found"
            )
        
        private_key = association_data.get("private_key")
        if not private_key:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Private key required for token association"
            )
        
        # Associate with fungible token
        result = await hedera_service.associate_token(
            account_id=current_user.wallet_id,
            token_id=asset.ft_id,
            private_key=private_key
        )
        
        if result.get("status") != "success":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Token association failed: {result.get('error')}"
            )
        
        # Record transaction
        transaction = Transaction(
            user_id=current_user.id,
            transaction_id=result["transaction_id"],
            transaction_type="associate",
            asset_id=asset.id,
            token_id=asset.ft_id,
            status="success"
        )
        db.add(transaction)
        db.commit()
        
        return APIResponse(
            success=True,
            message="Token associated successfully",
            data={
                "transaction_id": result["transaction_id"],
                "token_id": asset.ft_id,
                "account_id": current_user.wallet_id
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/{asset_id}/transfer", response_model=APIResponse)
async def transfer_asset_tokens(
    asset_id: int,
    transfer_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Transfer asset tokens between accounts"""
    try:
        asset = db.query(Asset).filter(Asset.id == asset_id).first()
        
        if not asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asset not found"
            )
        
        to_account = transfer_data.get("to_account")
        amount = transfer_data.get("amount")
        private_key = transfer_data.get("private_key")
        
        if not all([to_account, amount, private_key]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing required fields: to_account, amount, private_key"
            )
        
        # Execute token transfer
        result = await hedera_service.transfer_tokens(
            token_id=asset.ft_id,
            from_account=current_user.wallet_id,
            to_account=to_account,
            amount=int(float(amount) * 100),  # Account for decimals
            private_key=private_key
        )
        
        if result.get("status") != "success":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Token transfer failed: {result.get('error')}"
            )
        
        # Update holdings in database
        from models.models import Holding
        
        # Reduce sender's holding
        sender_holding = db.query(Holding).filter(
            Holding.user_id == current_user.id,
            Holding.asset_id == asset_id
        ).first()
        
        if sender_holding:
            sender_holding.amount -= float(amount)
            if sender_holding.amount <= 0:
                db.delete(sender_holding)
        
        # Increase receiver's holding
        receiver = db.query(User).filter(User.wallet_id == to_account).first()
        if receiver:
            receiver_holding = db.query(Holding).filter(
                Holding.user_id == receiver.id,
                Holding.asset_id == asset_id
            ).first()
            
            if receiver_holding:
                receiver_holding.amount += float(amount)
            else:
                new_holding = Holding(
                    user_id=receiver.id,
                    asset_id=asset_id,
                    ft_id=asset.ft_id,
                    amount=float(amount)
                )
                db.add(new_holding)
        
        # Record transaction
        transaction = Transaction(
            user_id=current_user.id,
            transaction_id=result["transaction_id"],
            transaction_type="transfer",
            asset_id=asset.id,
            amount=float(amount),
            token_id=asset.ft_id,
            status="success",
            extra_data={"to_account": to_account}
        )
        db.add(transaction)
        
        db.commit()
        
        return APIResponse(
            success=True,
            message="Tokens transferred successfully",
            data={
                "transaction_id": result["transaction_id"],
                "from_account": current_user.wallet_id,
                "to_account": to_account,
                "amount": amount,
                "token_id": asset.ft_id
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
