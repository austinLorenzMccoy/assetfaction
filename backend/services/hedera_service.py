"""
Hedera SDK service for blockchain interactions
"""

import hashlib
import json
from typing import Optional, Dict, Any
from hedera import (
    Client, AccountCreateTransaction, AccountId, PrivateKey, PublicKey,
    TokenCreateTransaction, TokenType, TokenSupplyType, TokenMintTransaction,
    TransferTransaction, Hbar, TopicMessageSubmitTransaction, TopicId,
    TokenAssociateTransaction, TokenId, NftId
)
from utils.config import settings


class HederaService:
    """Service for interacting with Hedera network"""
    
    def __init__(self):
        """Initialize Hedera client"""
        self.client = self._create_client()
        self.operator_id = AccountId.fromString(settings.OPERATOR_ID)
        self.operator_key = PrivateKey.fromString(settings.OPERATOR_KEY)
        self.treasury_id = AccountId.fromString(settings.TREASURY_ID)
        self.treasury_key = PrivateKey.fromString(settings.TREASURY_KEY)
        self.hcs_topic_id = TopicId.fromString(settings.HCS_TOPIC_ID)
    
    def _create_client(self) -> Client:
        """Create and configure Hedera client"""
        if settings.HEDERA_NETWORK == "testnet":
            client = Client.forTestnet()
        elif settings.HEDERA_NETWORK == "mainnet":
            client = Client.forMainnet()
        else:
            client = Client.forPreviewnet()
        
        client.setOperator(
            AccountId.fromString(settings.OPERATOR_ID),
            PrivateKey.fromString(settings.OPERATOR_KEY)
        )
        return client
    
    async def create_sponsored_account(self, public_key: str, initial_balance: float = 0) -> Dict[str, Any]:
        """Create a new sponsored Hedera account"""
        try:
            pub_key = PublicKey.from_string(public_key)
            
            # Create account transaction
            transaction = (
                AccountCreateTransaction()
                .set_key(pub_key)
                .set_initial_balance(Hbar.from_hbars(initial_balance))
                .set_account_memo("AssetFraction Sponsored Account")
                .freeze_with(self.client)
                .sign(self.treasury_key)
            )
            
            # Execute transaction
            response = await transaction.execute_async(self.client)
            receipt = await response.get_receipt_async(self.client)
            
            return {
                "account_id": receipt.account_id.to_string(),
                "transaction_id": response.transaction_id.to_string(),
                "status": "success"
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "status": "failed"
            }
    
    async def submit_kyc_to_hcs(self, account_id: str, kyc_hash: str) -> Dict[str, Any]:
        """Submit KYC hash to Hedera Consensus Service"""
        try:
            message = f"KYC:{account_id}:{kyc_hash}"
            
            transaction = (
                TopicMessageSubmitTransaction()
                .set_topic_id(self.hcs_topic_id)
                .set_message(message.encode())
                .freeze_with(self.client)
                .sign(self.operator_key)
            )
            
            response = await transaction.execute_async(self.client)
            receipt = await response.get_receipt_async(self.client)
            
            return {
                "message_id": receipt.topic_sequence_number,
                "transaction_id": response.transaction_id.to_string(),
                "status": "success"
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "status": "failed"
            }
    
    async def create_nft_token(self, name: str, symbol: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Create an NFT token for asset representation"""
        try:
            transaction = (
                TokenCreateTransaction()
                .set_token_name(name)
                .set_token_symbol(symbol)
                .set_token_type(TokenType.NON_FUNGIBLE_UNIQUE)
                .set_decimals(0)
                .set_initial_supply(0)
                .set_treasury_account_id(self.treasury_id)
                .set_supply_type(TokenSupplyType.FINITE)
                .set_max_supply(1)  # Only one NFT per asset
                .set_supply_key(self.treasury_key.public_key)
                .set_admin_key(self.treasury_key.public_key)
                .freeze_with(self.client)
                .sign(self.treasury_key)
            )
            
            response = await transaction.execute_async(self.client)
            receipt = await response.get_receipt_async(self.client)
            
            # Mint the NFT with metadata
            metadata_bytes = json.dumps(metadata).encode()
            mint_transaction = (
                TokenMintTransaction()
                .set_token_id(receipt.token_id)
                .add_metadata(metadata_bytes)
                .freeze_with(self.client)
                .sign(self.treasury_key)
            )
            
            mint_response = await mint_transaction.execute_async(self.client)
            mint_receipt = await mint_response.get_receipt_async(self.client)
            
            return {
                "token_id": receipt.token_id.to_string(),
                "nft_id": f"{receipt.token_id.to_string()}/{mint_receipt.serials[0]}",
                "transaction_id": response.transaction_id.to_string(),
                "mint_transaction_id": mint_response.transaction_id.to_string(),
                "status": "success"
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "status": "failed"
            }
    
    async def create_fungible_token(self, name: str, symbol: str, supply: int) -> Dict[str, Any]:
        """Create a fungible token for fractional ownership"""
        try:
            transaction = (
                TokenCreateTransaction()
                .set_token_name(name)
                .set_token_symbol(symbol)
                .set_token_type(TokenType.FUNGIBLE_COMMON)
                .set_decimals(2)  # Allow fractional tokens
                .set_initial_supply(supply * 100)  # Account for decimals
                .set_treasury_account_id(self.treasury_id)
                .set_supply_type(TokenSupplyType.FINITE)
                .set_max_supply(supply * 100)
                .set_admin_key(self.treasury_key.public_key)
                .freeze_with(self.client)
                .sign(self.treasury_key)
            )
            
            response = await transaction.execute_async(self.client)
            receipt = await response.get_receipt_async(self.client)
            
            return {
                "token_id": receipt.token_id.to_string(),
                "transaction_id": response.transaction_id.to_string(),
                "status": "success"
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "status": "failed"
            }
    
    async def associate_token(self, account_id: str, token_id: str, private_key: str) -> Dict[str, Any]:
        """Associate a token with an account"""
        try:
            account = AccountId.from_string(account_id)
            token = TokenId.from_string(token_id)
            key = PrivateKey.from_string(private_key)
            
            transaction = (
                TokenAssociateTransaction()
                .set_account_id(account)
                .set_token_ids([token])
                .freeze_with(self.client)
                .sign(key)
            )
            
            response = await transaction.execute_async(self.client)
            receipt = await response.get_receipt_async(self.client)
            
            return {
                "transaction_id": response.transaction_id.to_string(),
                "status": "success"
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "status": "failed"
            }
    
    async def transfer_tokens(self, token_id: str, from_account: str, to_account: str, 
                            amount: int, private_key: str) -> Dict[str, Any]:
        """Transfer fungible tokens between accounts"""
        try:
            token = TokenId.from_string(token_id)
            from_acc = AccountId.from_string(from_account)
            to_acc = AccountId.from_string(to_account)
            key = PrivateKey.from_string(private_key)
            
            transaction = (
                TransferTransaction()
                .add_token_transfer(token, from_acc, -amount)
                .add_token_transfer(token, to_acc, amount)
                .freeze_with(self.client)
                .sign(key)
            )
            
            response = await transaction.execute_async(self.client)
            receipt = await response.get_receipt_async(self.client)
            
            return {
                "transaction_id": response.transaction_id.to_string(),
                "status": "success"
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "status": "failed"
            }
    
    async def transfer_hbar(self, from_account: str, to_account: str, 
                          amount: float, private_key: str) -> Dict[str, Any]:
        """Transfer HBAR between accounts"""
        try:
            from_acc = AccountId.from_string(from_account)
            to_acc = AccountId.from_string(to_account)
            key = PrivateKey.from_string(private_key)
            
            transaction = (
                TransferTransaction()
                .add_hbar_transfer(from_acc, Hbar.from_hbars(-amount))
                .add_hbar_transfer(to_acc, Hbar.from_hbars(amount))
                .freeze_with(self.client)
                .sign(key)
            )
            
            response = await transaction.execute_async(self.client)
            receipt = await response.get_receipt_async(self.client)
            
            return {
                "transaction_id": response.transaction_id.to_string(),
                "status": "success"
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "status": "failed"
            }
    
    @staticmethod
    def generate_key_pair() -> Dict[str, str]:
        """Generate a new key pair"""
        private_key = PrivateKey.generate()
        public_key = private_key.public_key
        
        return {
            "private_key": private_key.to_string(),
            "public_key": public_key.to_string()
        }
    
    @staticmethod
    def hash_document(content: str) -> str:
        """Generate SHA256 hash of document content"""
        return hashlib.sha256(content.encode()).hexdigest()


# Global service instance
hedera_service = HederaService()
