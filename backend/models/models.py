"""
SQLAlchemy models for AssetFraction Backend
"""

from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.database import Base


class User(Base):
    """User model for wallet and KYC information"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(String, unique=True, index=True, nullable=False)
    public_key = Column(String, nullable=False)
    private_key_encrypted = Column(Text, nullable=True)  # Encrypted private key
    kyc_verified = Column(Boolean, default=False)
    kyc_hash = Column(String, nullable=True)  # SHA256 hash of KYC documents
    phone_number = Column(String, nullable=True)
    email = Column(String, nullable=True)
    name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    holdings = relationship("Holding", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")


class Asset(Base):
    """Asset model for tokenized real estate and art"""
    __tablename__ = "assets"
    
    id = Column(Integer, primary_key=True, index=True)
    nft_id = Column(String, unique=True, index=True, nullable=False)  # Hedera NFT ID
    ft_id = Column(String, unique=True, index=True, nullable=False)   # Hedera FT ID
    asset_type = Column(String, nullable=False)  # 'real_estate' or 'art'
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String, nullable=True)
    valuation = Column(Float, nullable=False)  # USD value
    total_supply = Column(Integer, default=10000)  # Total fractional tokens
    extra_data = Column(JSON, nullable=True)  # IPFS links, deed hash, etc.
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    royalty_percentage = Column(Float, default=5.0)  # Royalty percentage for resales
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    creator = relationship("User")
    holdings = relationship("Holding", back_populates="asset")
    income_distributions = relationship("IncomeDistribution", back_populates="asset")


class Holding(Base):
    """Token holdings for users"""
    __tablename__ = "holdings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    ft_id = Column(String, nullable=False)  # Hedera FT ID
    amount = Column(Float, nullable=False)  # Number of fractional tokens held
    purchase_price = Column(Float, nullable=True)  # Price paid per token
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="holdings")
    asset = relationship("Asset", back_populates="holdings")


class Transaction(Base):
    """Transaction history"""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    transaction_id = Column(String, unique=True, index=True, nullable=False)  # Hedera TX ID
    transaction_type = Column(String, nullable=False)  # 'mint', 'transfer', 'income', 'royalty'
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=True)
    amount = Column(Float, nullable=True)
    token_id = Column(String, nullable=True)  # NFT or FT ID
    status = Column(String, default="pending")  # 'pending', 'success', 'failed'
    extra_data = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    asset = relationship("Asset")


class IncomeDistribution(Base):
    """Income distribution records"""
    __tablename__ = "income_distributions"
    
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    total_income = Column(Float, nullable=False)  # Total income to distribute
    distribution_date = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, default="scheduled")  # 'scheduled', 'processing', 'completed', 'failed'
    extra_data = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    asset = relationship("Asset", back_populates="income_distributions")
    payouts = relationship("IncomePayout", back_populates="distribution")


class IncomePayout(Base):
    """Individual income payouts to token holders"""
    __tablename__ = "income_payouts"
    
    id = Column(Integer, primary_key=True, index=True)
    distribution_id = Column(Integer, ForeignKey("income_distributions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)  # Amount paid to user
    transaction_id = Column(String, nullable=True)  # Hedera TX ID
    status = Column(String, default="pending")  # 'pending', 'success', 'failed'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    distribution = relationship("IncomeDistribution", back_populates="payouts")
    user = relationship("User")


class KYCSubmission(Base):
    """KYC submission records"""
    __tablename__ = "kyc_submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    document_hash = Column(String, nullable=False)  # SHA256 hash of documents
    document_type = Column(String, nullable=False)  # 'passport', 'id_card', 'drivers_license'
    hcs_message_id = Column(String, nullable=True)  # HCS message ID
    verification_status = Column(String, default="pending")  # 'pending', 'approved', 'rejected'
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    verified_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User")
