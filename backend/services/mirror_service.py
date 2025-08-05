"""
Mirror Node service for querying Hedera transaction data
"""

import requests
from typing import Dict, Any, List, Optional
from utils.config import settings


class MirrorNodeService:
    """Service for interacting with Hedera Mirror Node API"""
    
    def __init__(self):
        """Initialize Mirror Node service"""
        self.base_url = settings.MIRROR_NODE_API
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'AssetFraction-Backend/1.0.0'
        })
    
    async def get_account_info(self, account_id: str) -> Dict[str, Any]:
        """Get account information from Mirror Node"""
        try:
            url = f"{self.base_url}/accounts/{account_id}"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "status": "failed"}
    
    async def get_account_transactions(self, account_id: str, limit: int = 25, 
                                     order: str = "desc") -> Dict[str, Any]:
        """Get transaction history for an account"""
        try:
            url = f"{self.base_url}/accounts/{account_id}/transactions"
            params = {
                "limit": limit,
                "order": order
            }
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "status": "failed"}
    
    async def get_token_info(self, token_id: str) -> Dict[str, Any]:
        """Get token information from Mirror Node"""
        try:
            url = f"{self.base_url}/tokens/{token_id}"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "status": "failed"}
    
    async def get_token_balances(self, account_id: str) -> Dict[str, Any]:
        """Get token balances for an account"""
        try:
            url = f"{self.base_url}/accounts/{account_id}/tokens"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "status": "failed"}
    
    async def get_nft_info(self, token_id: str, serial_number: int) -> Dict[str, Any]:
        """Get NFT information from Mirror Node"""
        try:
            url = f"{self.base_url}/tokens/{token_id}/nfts/{serial_number}"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "status": "failed"}
    
    async def get_transaction_info(self, transaction_id: str) -> Dict[str, Any]:
        """Get detailed transaction information"""
        try:
            url = f"{self.base_url}/transactions/{transaction_id}"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "status": "failed"}
    
    async def get_topic_messages(self, topic_id: str, limit: int = 25, 
                               order: str = "desc") -> Dict[str, Any]:
        """Get messages from a HCS topic"""
        try:
            url = f"{self.base_url}/topics/{topic_id}/messages"
            params = {
                "limit": limit,
                "order": order
            }
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "status": "failed"}
    
    async def search_transactions(self, account_id: str, transaction_type: Optional[str] = None,
                                token_id: Optional[str] = None, limit: int = 25) -> Dict[str, Any]:
        """Search transactions with filters"""
        try:
            url = f"{self.base_url}/transactions"
            params = {
                "account.id": account_id,
                "limit": limit,
                "order": "desc"
            }
            
            if transaction_type:
                params["transactiontype"] = transaction_type
            if token_id:
                params["token.id"] = token_id
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "status": "failed"}
    
    async def get_asset_related_transactions(self, account_id: str, 
                                           asset_tokens: List[str]) -> Dict[str, Any]:
        """Get transactions related to specific asset tokens"""
        try:
            all_transactions = []
            
            for token_id in asset_tokens:
                result = await self.search_transactions(
                    account_id=account_id,
                    token_id=token_id,
                    limit=50
                )
                
                if "transactions" in result:
                    all_transactions.extend(result["transactions"])
            
            # Sort by consensus timestamp (most recent first)
            all_transactions.sort(
                key=lambda x: x.get("consensus_timestamp", ""),
                reverse=True
            )
            
            return {
                "transactions": all_transactions[:25],  # Limit to 25 most recent
                "total": len(all_transactions)
            }
            
        except Exception as e:
            return {"error": str(e), "status": "failed"}
    
    async def get_income_distribution_proof(self, transaction_ids: List[str]) -> Dict[str, Any]:
        """Get proof of income distribution transactions"""
        try:
            proofs = []
            
            for tx_id in transaction_ids:
                tx_info = await self.get_transaction_info(tx_id)
                if "error" not in tx_info:
                    proofs.append({
                        "transaction_id": tx_id,
                        "consensus_timestamp": tx_info.get("consensus_timestamp"),
                        "result": tx_info.get("result"),
                        "transfers": tx_info.get("transfers", []),
                        "token_transfers": tx_info.get("token_transfers", [])
                    })
            
            return {
                "proofs": proofs,
                "total": len(proofs)
            }
            
        except Exception as e:
            return {"error": str(e), "status": "failed"}
    
    def format_transaction_for_frontend(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """Format transaction data for frontend consumption"""
        return {
            "transaction_id": transaction.get("transaction_id"),
            "consensus_timestamp": transaction.get("consensus_timestamp"),
            "type": transaction.get("name", "Unknown"),
            "result": transaction.get("result"),
            "charged_fee": transaction.get("charged_tx_fee", 0),
            "transfers": transaction.get("transfers", []),
            "token_transfers": transaction.get("token_transfers", []),
            "memo": transaction.get("memo_base64", ""),
            "valid_start_timestamp": transaction.get("valid_start_timestamp")
        }
    
    async def get_portfolio_summary(self, account_id: str) -> Dict[str, Any]:
        """Get portfolio summary for an account"""
        try:
            # Get account info
            account_info = await self.get_account_info(account_id)
            if "error" in account_info:
                return account_info
            
            # Get token balances
            token_balances = await self.get_token_balances(account_id)
            if "error" in token_balances:
                return token_balances
            
            # Get recent transactions
            transactions = await self.get_account_transactions(account_id, limit=10)
            if "error" in transactions:
                return transactions
            
            return {
                "account_id": account_id,
                "balance": account_info.get("balance", {}).get("balance", 0),
                "tokens": token_balances.get("tokens", []),
                "recent_transactions": [
                    self.format_transaction_for_frontend(tx)
                    for tx in transactions.get("transactions", [])
                ],
                "status": "success"
            }
            
        except Exception as e:
            return {"error": str(e), "status": "failed"}


# Global service instance
mirror_service = MirrorNodeService()
