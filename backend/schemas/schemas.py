"""
Pydantic schemas for request/response validation
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field, validator


# User Schemas
class UserCreate(BaseModel):
    """Schema for creating a new user"""
    public_key: str = Field(..., description="User's public key")
    name: Optional[str] = Field(None, description="User's full name")
    email: Optional[str] = Field(None, description="User's email address")
    phone_number: Optional[str] = Field(None, description="User's phone number")


class UserResponse(BaseModel):
    """Schema for user response"""
    id: int
    wallet_id: str
    public_key: str
    kyc_verified: bool
    name: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# Wallet Schemas
class WalletCreateRequest(BaseModel):
    """Schema for wallet creation request"""
    public_key: str = Field(..., description="Public key for the new wallet")
    initial_balance: Optional[float] = Field(0, description="Initial HBAR balance")


class WalletCreateResponse(BaseModel):
    """Schema for wallet creation response"""
    wallet_id: str = Field(..., description="Created wallet ID")
    public_key: str = Field(..., description="Wallet public key")
    transaction_id: str = Field(..., description="Creation transaction ID")
    status: str = Field(..., description="Creation status")


# KYC Schemas
class KYCSubmissionRequest(BaseModel):
    """Schema for KYC submission"""
    wallet_id: str = Field(..., description="User's wallet ID")
    document_hash: str = Field(..., description="SHA256 hash of KYC documents")
    document_type: str = Field(..., description="Type of document submitted")
    name: str = Field(..., description="User's full name")
    phone_number: Optional[str] = Field(None, description="User's phone number")
    
    @validator('document_type')
    def validate_document_type(cls, v):
        allowed_types = ['passport', 'id_card', 'drivers_license']
        if v not in allowed_types:
            raise ValueError(f'Document type must be one of: {allowed_types}')
        return v


class KYCSubmissionResponse(BaseModel):
    """Schema for KYC submission response"""
    submission_id: int
    hcs_message_id: str
    status: str
    submitted_at: datetime


# Asset Schemas
class AssetTokenizeRequest(BaseModel):
    """Schema for asset tokenization request"""
    asset_type: str = Field(..., description="Type of asset (real_estate or art)")
    name: str = Field(..., description="Asset name")
    description: Optional[str] = Field(None, description="Asset description")
    location: Optional[str] = Field(None, description="Asset location")
    valuation: float = Field(..., description="Asset valuation in USD")
    total_supply: int = Field(10000, description="Total fractional tokens to create")
    extra_data: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    royalty_percentage: float = Field(5.0, description="Royalty percentage for resales")
    
    @validator('asset_type')
    def validate_asset_type(cls, v):
        allowed_types = ['real_estate', 'art']
        if v not in allowed_types:
            raise ValueError(f'Asset type must be one of: {allowed_types}')
        return v
    
    @validator('royalty_percentage')
    def validate_royalty_percentage(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Royalty percentage must be between 0 and 100')
        return v


class AssetTokenizeResponse(BaseModel):
    """Schema for asset tokenization response"""
    asset_id: int
    nft_id: str
    ft_id: str
    name: str
    valuation: float
    total_supply: int
    transaction_id: str
    status: str


class AssetResponse(BaseModel):
    """Schema for asset response"""
    id: int
    nft_id: str
    ft_id: str
    asset_type: str
    name: str
    description: Optional[str]
    location: Optional[str]
    valuation: float
    total_supply: int
    royalty_percentage: float
    created_at: datetime
    extra_data: Optional[Dict[str, Any]]
    
    class Config:
        from_attributes = True


# Holding Schemas
class HoldingResponse(BaseModel):
    """Schema for holding response"""
    id: int
    ft_id: str
    amount: float
    purchase_price: Optional[float]
    asset: AssetResponse
    created_at: datetime
    
    class Config:
        from_attributes = True


# Income Distribution Schemas
class IncomeDistributionRequest(BaseModel):
    """Schema for scheduling income distribution"""
    asset_id: int = Field(..., description="Asset ID for income distribution")
    total_income: float = Field(..., description="Total income to distribute")
    distribution_date: datetime = Field(..., description="When to distribute income")


class IncomeDistributionResponse(BaseModel):
    """Schema for income distribution response"""
    id: int
    asset_id: int
    total_income: float
    distribution_date: datetime
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class IncomePayoutResponse(BaseModel):
    """Schema for income payout response"""
    id: int
    user_id: int
    amount: float
    transaction_id: Optional[str]
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# Transaction Schemas
class TransactionResponse(BaseModel):
    """Schema for transaction response"""
    id: int
    transaction_id: str
    transaction_type: str
    amount: Optional[float]
    token_id: Optional[str]
    status: str
    extra_data: Optional[Dict[str, Any]]
    created_at: datetime
    
    class Config:
        from_attributes = True


# Mirror Node Schemas
class MirrorNodeTransaction(BaseModel):
    """Schema for Mirror Node transaction data"""
    transaction_id: str
    consensus_timestamp: str
    transaction_type: str
    result: str
    charged_tx_fee: int
    transfers: List[Dict[str, Any]]
    token_transfers: List[Dict[str, Any]]


class MirrorNodeResponse(BaseModel):
    """Schema for Mirror Node API response"""
    transactions: List[MirrorNodeTransaction]
    links: Dict[str, Optional[str]]


# API Response Schemas
class APIResponse(BaseModel):
    """Generic API response schema"""
    success: bool = Field(..., description="Whether the request was successful")
    message: str = Field(..., description="Response message")
    data: Optional[Any] = Field(None, description="Response data")
    error: Optional[str] = Field(None, description="Error message if any")


class PaginatedResponse(BaseModel):
    """Schema for paginated responses"""
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int
