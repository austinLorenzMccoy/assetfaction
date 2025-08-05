"""
Test cases for AssetFraction Backend
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch, AsyncMock

from main import app
from database.database import get_db, Base
from models.models import User, Asset
from utils.config import settings

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create test database
Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


class TestAPI:
    """Test class for API endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "🏠 AssetFraction Backend API"
        assert data["status"] == "running"
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "database" in data
        assert "scheduler" in data
    
    @patch('services.hedera_service.hedera_service.create_sponsored_account')
    def test_create_wallet(self, mock_create_account):
        """Test wallet creation"""
        # Mock Hedera service response
        mock_create_account.return_value = {
            "account_id": "0.0.123456",
            "transaction_id": "0.0.123456@1234567890.123456789",
            "status": "success"
        }
        
        wallet_data = {
            "public_key": "302a300506032b6570032100abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
            "initial_balance": 10.0
        }
        
        response = client.post("/api/v1/wallet/create", json=wallet_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert data["data"]["wallet_id"] == "0.0.123456"
    
    def test_create_wallet_duplicate(self):
        """Test creating wallet with duplicate public key"""
        wallet_data = {
            "public_key": "duplicate_key",
            "initial_balance": 5.0
        }
        
        # Create first wallet
        with patch('services.hedera_service.hedera_service.create_sponsored_account') as mock_create:
            mock_create.return_value = {
                "account_id": "0.0.111111",
                "transaction_id": "0.0.111111@1234567890.123456789",
                "status": "success"
            }
            
            response1 = client.post("/api/v1/wallet/create", json=wallet_data)
            assert response1.status_code == 200
        
        # Try to create duplicate
        response2 = client.post("/api/v1/wallet/create", json=wallet_data)
        assert response2.status_code == 400
    
    @patch('services.hedera_service.hedera_service.submit_kyc_to_hcs')
    def test_submit_kyc(self, mock_submit_kyc):
        """Test KYC submission"""
        # First create a user
        with patch('services.hedera_service.hedera_service.create_sponsored_account') as mock_create:
            mock_create.return_value = {
                "account_id": "0.0.222222",
                "transaction_id": "0.0.222222@1234567890.123456789",
                "status": "success"
            }
            
            wallet_data = {
                "public_key": "kyc_test_key",
                "initial_balance": 0.0
            }
            client.post("/api/v1/wallet/create", json=wallet_data)
        
        # Mock HCS submission
        mock_submit_kyc.return_value = {
            "message_id": 12345,
            "transaction_id": "0.0.987654@1234567890.123456789",
            "status": "success"
        }
        
        kyc_data = {
            "wallet_id": "0.0.222222",
            "document_hash": "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
            "document_type": "passport",
            "name": "Test User",
            "phone_number": "+1234567890"
        }
        
        response = client.post("/api/v1/kyc/submit", json=kyc_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert data["data"]["hcs_message_id"] == "12345"
    
    def test_list_assets(self):
        """Test listing assets"""
        response = client.get("/api/v1/assets/list")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "assets" in data["data"]
    
    def test_get_nonexistent_asset(self):
        """Test getting non-existent asset"""
        response = client.get("/api/v1/assets/99999")
        assert response.status_code == 404
    
    @patch('services.mirror_service.mirror_service.get_account_info')
    def test_get_account_info(self, mock_get_account):
        """Test getting account info from Mirror Node"""
        mock_get_account.return_value = {
            "account": "0.0.123456",
            "balance": {"balance": 1000000000},
            "created_timestamp": "1234567890.123456789"
        }
        
        response = client.get("/api/v1/mirror/account/0.0.123456")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert data["data"]["account"] == "0.0.123456"
    
    @patch('services.mirror_service.mirror_service.get_account_transactions')
    def test_get_account_transactions(self, mock_get_transactions):
        """Test getting account transactions"""
        mock_get_transactions.return_value = {
            "transactions": [
                {
                    "transaction_id": "0.0.123456@1234567890.123456789",
                    "consensus_timestamp": "1234567890.123456789",
                    "name": "CRYPTOTRANSFER",
                    "result": "SUCCESS",
                    "charged_tx_fee": 100000,
                    "transfers": []
                }
            ]
        }
        
        response = client.get("/api/v1/mirror/transactions/0.0.123456")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]["transactions"]) == 1


class TestServices:
    """Test class for service functions"""
    
    def test_hedera_service_key_generation(self):
        """Test Hedera service key generation"""
        from services.hedera_service import HederaService
        
        keys = HederaService.generate_key_pair()
        assert "private_key" in keys
        assert "public_key" in keys
        assert len(keys["private_key"]) > 0
        assert len(keys["public_key"]) > 0
    
    def test_document_hashing(self):
        """Test document hashing"""
        from services.hedera_service import HederaService
        
        content = "Test document content"
        hash1 = HederaService.hash_document(content)
        hash2 = HederaService.hash_document(content)
        
        assert hash1 == hash2
        assert len(hash1) == 64  # SHA256 hex length
    
    def test_mirror_service_transaction_formatting(self):
        """Test Mirror Node transaction formatting"""
        from services.mirror_service import mirror_service
        
        raw_transaction = {
            "transaction_id": "0.0.123456@1234567890.123456789",
            "consensus_timestamp": "1234567890.123456789",
            "name": "CRYPTOTRANSFER",
            "result": "SUCCESS",
            "charged_tx_fee": 100000,
            "transfers": [],
            "token_transfers": []
        }
        
        formatted = mirror_service.format_transaction_for_frontend(raw_transaction)
        
        assert formatted["transaction_id"] == raw_transaction["transaction_id"]
        assert formatted["type"] == "CRYPTOTRANSFER"
        assert formatted["result"] == "SUCCESS"


class TestModels:
    """Test class for database models"""
    
    def test_user_model(self):
        """Test User model"""
        db = TestingSessionLocal()
        
        user = User(
            wallet_id="0.0.test123",
            public_key="test_public_key",
            name="Test User",
            kyc_verified=False
        )
        
        db.add(user)
        db.commit()
        
        # Query the user
        queried_user = db.query(User).filter(User.wallet_id == "0.0.test123").first()
        assert queried_user is not None
        assert queried_user.name == "Test User"
        assert queried_user.kyc_verified is False
        
        db.close()
    
    def test_asset_model(self):
        """Test Asset model"""
        db = TestingSessionLocal()
        
        # Create a user first
        user = User(
            wallet_id="0.0.creator123",
            public_key="creator_public_key",
            kyc_verified=True
        )
        db.add(user)
        db.flush()
        
        # Create an asset
        asset = Asset(
            nft_id="0.0.nft123",
            ft_id="0.0.ft123",
            asset_type="real_estate",
            name="Test Property",
            valuation=100000.0,
            total_supply=10000,
            creator_id=user.id
        )
        
        db.add(asset)
        db.commit()
        
        # Query the asset
        queried_asset = db.query(Asset).filter(Asset.name == "Test Property").first()
        assert queried_asset is not None
        assert queried_asset.asset_type == "real_estate"
        assert queried_asset.valuation == 100000.0
        assert queried_asset.creator_id == user.id
        
        db.close()


class TestScheduler:
    """Test class for scheduler functionality"""
    
    def test_scheduler_initialization(self):
        """Test scheduler initialization"""
        from services.scheduler import scheduler
        
        # Scheduler should be initialized
        assert scheduler is not None
        assert hasattr(scheduler, 'scheduler')
    
    def test_get_scheduled_jobs(self):
        """Test getting scheduled jobs"""
        from services.scheduler import scheduler
        
        jobs = scheduler.get_scheduled_jobs()
        assert isinstance(jobs, list)


# Pytest fixtures
@pytest.fixture
def test_user():
    """Create a test user"""
    db = TestingSessionLocal()
    user = User(
        wallet_id="0.0.testuser",
        public_key="test_public_key_fixture",
        name="Fixture User",
        kyc_verified=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user
    db.delete(user)
    db.commit()
    db.close()


@pytest.fixture
def test_asset(test_user):
    """Create a test asset"""
    db = TestingSessionLocal()
    asset = Asset(
        nft_id="0.0.testnft",
        ft_id="0.0.testft",
        asset_type="art",
        name="Test Artwork",
        valuation=50000.0,
        total_supply=5000,
        creator_id=test_user.id
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    yield asset
    db.delete(asset)
    db.commit()
    db.close()


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
