"""
Mirror Node API routes for querying Hedera transaction data
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database.database import get_db
from models.models import User, Asset
from schemas.schemas import APIResponse
from services.mirror_service import mirror_service

router = APIRouter()


@router.get("/account/{account_id}", response_model=APIResponse)
async def get_account_info(account_id: str):
    """Get account information from Mirror Node"""
    try:
        account_info = await mirror_service.get_account_info(account_id)
        
        if "error" in account_info:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get account info: {account_info['error']}"
            )
        
        return APIResponse(
            success=True,
            message="Account information retrieved",
            data=account_info
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/transactions/{account_id}", response_model=APIResponse)
async def get_account_transactions(
    account_id: str,
    limit: int = 25,
    order: str = "desc"
):
    """Get transaction history for an account"""
    try:
        transactions = await mirror_service.get_account_transactions(
            account_id=account_id,
            limit=limit,
            order=order
        )
        
        if "error" in transactions:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get transactions: {transactions['error']}"
            )
        
        # Format transactions for frontend
        formatted_transactions = []
        for tx in transactions.get("transactions", []):
            formatted_transactions.append(
                mirror_service.format_transaction_for_frontend(tx)
            )
        
        return APIResponse(
            success=True,
            message="Transaction history retrieved",
            data={
                "account_id": account_id,
                "transactions": formatted_transactions,
                "total": len(formatted_transactions)
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/tokens/{token_id}", response_model=APIResponse)
async def get_token_info(token_id: str):
    """Get token information from Mirror Node"""
    try:
        token_info = await mirror_service.get_token_info(token_id)
        
        if "error" in token_info:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get token info: {token_info['error']}"
            )
        
        return APIResponse(
            success=True,
            message="Token information retrieved",
            data=token_info
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/balances/{account_id}", response_model=APIResponse)
async def get_token_balances(account_id: str):
    """Get token balances for an account"""
    try:
        balances = await mirror_service.get_token_balances(account_id)
        
        if "error" in balances:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get token balances: {balances['error']}"
            )
        
        return APIResponse(
            success=True,
            message="Token balances retrieved",
            data=balances
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/nft/{token_id}/{serial_number}", response_model=APIResponse)
async def get_nft_info(token_id: str, serial_number: int):
    """Get NFT information from Mirror Node"""
    try:
        nft_info = await mirror_service.get_nft_info(token_id, serial_number)
        
        if "error" in nft_info:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get NFT info: {nft_info['error']}"
            )
        
        return APIResponse(
            success=True,
            message="NFT information retrieved",
            data=nft_info
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/transaction/{transaction_id}", response_model=APIResponse)
async def get_transaction_info(transaction_id: str):
    """Get detailed transaction information"""
    try:
        tx_info = await mirror_service.get_transaction_info(transaction_id)
        
        if "error" in tx_info:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get transaction info: {tx_info['error']}"
            )
        
        formatted_tx = mirror_service.format_transaction_for_frontend(tx_info)
        
        return APIResponse(
            success=True,
            message="Transaction information retrieved",
            data=formatted_tx
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/topic/{topic_id}/messages", response_model=APIResponse)
async def get_topic_messages(
    topic_id: str,
    limit: int = 25,
    order: str = "desc"
):
    """Get messages from a HCS topic"""
    try:
        messages = await mirror_service.get_topic_messages(
            topic_id=topic_id,
            limit=limit,
            order=order
        )
        
        if "error" in messages:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get topic messages: {messages['error']}"
            )
        
        return APIResponse(
            success=True,
            message="Topic messages retrieved",
            data=messages
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/portfolio/{account_id}", response_model=APIResponse)
async def get_portfolio_summary(account_id: str, db: Session = Depends(get_db)):
    """Get complete portfolio summary for an account"""
    try:
        portfolio = await mirror_service.get_portfolio_summary(account_id)
        
        if "error" in portfolio:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get portfolio: {portfolio['error']}"
            )
        
        # Enhance with local database information
        user = db.query(User).filter(User.wallet_id == account_id).first()
        if user:
            from models.models import Holding
            holdings = db.query(Holding).filter(
                Holding.user_id == user.id
            ).join(Asset).all()
            
            # Add asset fraction holdings
            asset_holdings = []
            for holding in holdings:
                asset_holdings.append({
                    "asset_id": holding.asset.id,
                    "asset_name": holding.asset.name,
                    "asset_type": holding.asset.asset_type,
                    "tokens_held": holding.amount,
                    "total_supply": holding.asset.total_supply,
                    "ownership_percentage": (holding.amount / holding.asset.total_supply) * 100,
                    "asset_valuation": holding.asset.valuation,
                    "estimated_value": (holding.amount / holding.asset.total_supply) * holding.asset.valuation
                })
            
            portfolio["asset_fraction_holdings"] = asset_holdings
            portfolio["user_info"] = {
                "kyc_verified": user.kyc_verified,
                "name": user.name,
                "email": user.email
            }
        
        return APIResponse(
            success=True,
            message="Portfolio summary retrieved",
            data=portfolio
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/asset-transactions/{account_id}", response_model=APIResponse)
async def get_asset_related_transactions(
    account_id: str,
    asset_ids: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get transactions related to specific assets"""
    try:
        # Get asset tokens from database
        query = db.query(Asset)
        if asset_ids:
            asset_id_list = [int(id.strip()) for id in asset_ids.split(",")]
            query = query.filter(Asset.id.in_(asset_id_list))
        
        assets = query.all()
        asset_tokens = [asset.ft_id for asset in assets] + [asset.nft_id for asset in assets]
        
        if not asset_tokens:
            return APIResponse(
                success=True,
                message="No assets found",
                data={"transactions": [], "total": 0}
            )
        
        # Get asset-related transactions
        transactions = await mirror_service.get_asset_related_transactions(
            account_id=account_id,
            asset_tokens=asset_tokens
        )
        
        if "error" in transactions:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get asset transactions: {transactions['error']}"
            )
        
        # Format transactions and add asset context
        formatted_transactions = []
        for tx in transactions.get("transactions", []):
            formatted_tx = mirror_service.format_transaction_for_frontend(tx)
            
            # Add asset context
            for asset in assets:
                if any(transfer.get("token_id") in [asset.ft_id, asset.nft_id] 
                      for transfer in formatted_tx.get("token_transfers", [])):
                    formatted_tx["asset_context"] = {
                        "asset_id": asset.id,
                        "asset_name": asset.name,
                        "asset_type": asset.asset_type
                    }
                    break
            
            formatted_transactions.append(formatted_tx)
        
        return APIResponse(
            success=True,
            message="Asset-related transactions retrieved",
            data={
                "account_id": account_id,
                "transactions": formatted_transactions,
                "total": len(formatted_transactions)
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/income-proof/{distribution_id}", response_model=APIResponse)
async def get_income_distribution_proof(
    distribution_id: int,
    db: Session = Depends(get_db)
):
    """Get blockchain proof of income distribution"""
    try:
        from models.models import IncomeDistribution, IncomePayout
        
        # Get distribution and payouts
        distribution = db.query(IncomeDistribution).filter(
            IncomeDistribution.id == distribution_id
        ).first()
        
        if not distribution:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Distribution not found"
            )
        
        payouts = db.query(IncomePayout).filter(
            IncomePayout.distribution_id == distribution_id,
            IncomePayout.transaction_id.isnot(None)
        ).all()
        
        # Get transaction proofs from Mirror Node
        transaction_ids = [payout.transaction_id for payout in payouts]
        
        if not transaction_ids:
            return APIResponse(
                success=True,
                message="No transaction proofs available",
                data={
                    "distribution_id": distribution_id,
                    "proofs": [],
                    "total": 0
                }
            )
        
        proofs = await mirror_service.get_income_distribution_proof(transaction_ids)
        
        if "error" in proofs:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get income proofs: {proofs['error']}"
            )
        
        return APIResponse(
            success=True,
            message="Income distribution proof retrieved",
            data={
                "distribution_id": distribution_id,
                "asset_name": distribution.asset.name,
                "total_income": distribution.total_income,
                "distribution_date": distribution.distribution_date,
                "status": distribution.status,
                **proofs
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
