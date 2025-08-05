#!/usr/bin/env python3
"""
AssetFraction API Demo Script
Demonstrates the complete workflow of the AssetFraction backend
"""

import asyncio
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
DEMO_USER_PUBLIC_KEY = "302a300506032b6570032100abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"
DEMO_PRIVATE_KEY = "302e020100300506032b6570042204201234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"


class AssetFractionDemo:
    """Demo class for AssetFraction API"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.user_wallet_id = None
        self.access_token = None
        self.asset_id = None
        
    def _make_request(self, method: str, endpoint: str, data: Dict[Any, Any] = None, 
                     auth_required: bool = False) -> Dict[str, Any]:
        """Make HTTP request to API"""
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        if auth_required and self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, headers=headers)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, headers=headers)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            print(f"❌ Request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return {"error": str(e)}
    
    def print_step(self, step: str, description: str):
        """Print demo step"""
        print(f"\n{'='*60}")
        print(f"🚀 {step}: {description}")
        print(f"{'='*60}")
    
    def print_result(self, result: Dict[str, Any]):
        """Print API result"""
        if result.get("success"):
            print(f"✅ Success: {result.get('message')}")
            if result.get("data"):
                print(f"📊 Data: {json.dumps(result['data'], indent=2, default=str)}")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
    
    def demo_step_1_create_wallet(self):
        """Step 1: Create sponsored wallet"""
        self.print_step("STEP 1", "Create Sponsored Wallet")
        
        data = {
            "public_key": DEMO_USER_PUBLIC_KEY,
            "initial_balance": 10.0
        }
        
        result = self._make_request("POST", "/wallet/create", data)
        self.print_result(result)
        
        if result.get("success") and result.get("data"):
            self.user_wallet_id = result["data"]["wallet_id"]
            print(f"💰 Created wallet: {self.user_wallet_id}")
        
        return result.get("success", False)
    
    def demo_step_2_submit_kyc(self):
        """Step 2: Submit KYC information"""
        self.print_step("STEP 2", "Submit KYC Information")
        
        if not self.user_wallet_id:
            print("❌ No wallet ID available")
            return False
        
        # Generate a mock document hash
        import hashlib
        doc_content = f"KYC Document for {self.user_wallet_id} - {datetime.now()}"
        doc_hash = hashlib.sha256(doc_content.encode()).hexdigest()
        
        data = {
            "wallet_id": self.user_wallet_id,
            "document_hash": doc_hash,
            "document_type": "passport",
            "name": "Demo User",
            "phone_number": "+1234567890"
        }
        
        result = self._make_request("POST", "/kyc/submit", data)
        self.print_result(result)
        
        return result.get("success", False)
    
    def demo_step_3_check_balance(self):
        """Step 3: Check wallet balance"""
        self.print_step("STEP 3", "Check Wallet Balance")
        
        if not self.user_wallet_id:
            print("❌ No wallet ID available")
            return False
        
        result = self._make_request("GET", f"/wallet/balance/{self.user_wallet_id}")
        self.print_result(result)
        
        return result.get("success", False)
    
    def demo_step_4_tokenize_asset(self):
        """Step 4: Tokenize a real estate asset"""
        self.print_step("STEP 4", "Tokenize Real Estate Asset")
        
        # For demo purposes, we'll simulate having an access token
        # In a real implementation, you'd have a login endpoint
        
        data = {
            "asset_type": "real_estate",
            "name": "Lagos Luxury Apartment",
            "description": "A beautiful 3-bedroom apartment in Victoria Island, Lagos",
            "location": "Victoria Island, Lagos, Nigeria",
            "valuation": 250000.0,
            "total_supply": 10000,
            "royalty_percentage": 5.0,
            "metadata": {
                "bedrooms": 3,
                "bathrooms": 2,
                "square_feet": 1200,
                "year_built": 2020,
                "amenities": ["Swimming Pool", "Gym", "Security", "Parking"]
            }
        }
        
        result = self._make_request("POST", "/assets/tokenize", data, auth_required=True)
        self.print_result(result)
        
        if result.get("success") and result.get("data"):
            self.asset_id = result["data"]["asset_id"]
            print(f"🏠 Tokenized asset ID: {self.asset_id}")
        
        return result.get("success", False)
    
    def demo_step_5_list_assets(self):
        """Step 5: List all assets"""
        self.print_step("STEP 5", "List All Assets")
        
        result = self._make_request("GET", "/assets/list")
        self.print_result(result)
        
        return result.get("success", False)
    
    def demo_step_6_schedule_income(self):
        """Step 6: Schedule income distribution"""
        self.print_step("STEP 6", "Schedule Income Distribution")
        
        if not self.asset_id:
            print("❌ No asset ID available")
            return False
        
        # Schedule distribution for 1 minute from now (for demo purposes)
        distribution_date = datetime.utcnow() + timedelta(minutes=1)
        
        data = {
            "asset_id": self.asset_id,
            "total_income": 1000.0,
            "distribution_date": distribution_date.isoformat()
        }
        
        result = self._make_request("POST", "/rewards/schedule", data, auth_required=True)
        self.print_result(result)
        
        return result.get("success", False)
    
    def demo_step_7_get_portfolio(self):
        """Step 7: Get user portfolio"""
        self.print_step("STEP 7", "Get User Portfolio")
        
        if not self.user_wallet_id:
            print("❌ No wallet ID available")
            return False
        
        result = self._make_request("GET", f"/wallet/portfolio/{self.user_wallet_id}")
        self.print_result(result)
        
        return result.get("success", False)
    
    def demo_step_8_mirror_node_data(self):
        """Step 8: Query Mirror Node data"""
        self.print_step("STEP 8", "Query Mirror Node Data")
        
        if not self.user_wallet_id:
            print("❌ No wallet ID available")
            return False
        
        # Get account info
        result = self._make_request("GET", f"/mirror/account/{self.user_wallet_id}")
        self.print_result(result)
        
        # Get transaction history
        print("\n📜 Transaction History:")
        tx_result = self._make_request("GET", f"/mirror/transactions/{self.user_wallet_id}")
        self.print_result(tx_result)
        
        return result.get("success", False)
    
    def demo_step_9_health_check(self):
        """Step 9: Check API health"""
        self.print_step("STEP 9", "API Health Check")
        
        # Check root endpoint
        try:
            response = self.session.get(f"{self.base_url.replace('/api/v1', '')}/")
            root_result = response.json()
            print(f"✅ Root endpoint: {root_result.get('message')}")
        except Exception as e:
            print(f"❌ Root endpoint error: {e}")
        
        # Check health endpoint
        try:
            response = self.session.get(f"{self.base_url.replace('/api/v1', '')}/health")
            health_result = response.json()
            print(f"✅ Health check: {health_result.get('status')}")
            print(f"📊 Health data: {json.dumps(health_result, indent=2)}")
        except Exception as e:
            print(f"❌ Health check error: {e}")
        
        return True
    
    def run_complete_demo(self):
        """Run the complete demo workflow"""
        print("🏠 AssetFraction Backend API Demo")
        print("=" * 60)
        print("This demo will showcase the complete AssetFraction workflow:")
        print("1. Create sponsored wallet")
        print("2. Submit KYC information")
        print("3. Check wallet balance")
        print("4. Tokenize real estate asset")
        print("5. List all assets")
        print("6. Schedule income distribution")
        print("7. Get user portfolio")
        print("8. Query Mirror Node data")
        print("9. API health check")
        
        input("\nPress Enter to start the demo...")
        
        # Run demo steps
        steps = [
            self.demo_step_1_create_wallet,
            self.demo_step_2_submit_kyc,
            self.demo_step_3_check_balance,
            # Note: Steps 4-6 require authentication which would need to be implemented
            # self.demo_step_4_tokenize_asset,
            self.demo_step_5_list_assets,
            # self.demo_step_6_schedule_income,
            self.demo_step_7_get_portfolio,
            self.demo_step_8_mirror_node_data,
            self.demo_step_9_health_check
        ]
        
        successful_steps = 0
        for i, step in enumerate(steps, 1):
            try:
                if step():
                    successful_steps += 1
                input(f"\nPress Enter to continue to next step...")
            except KeyboardInterrupt:
                print("\n\n👋 Demo interrupted by user")
                break
            except Exception as e:
                print(f"\n❌ Step {i} failed with error: {e}")
        
        # Summary
        print(f"\n{'='*60}")
        print(f"📊 DEMO SUMMARY")
        print(f"{'='*60}")
        print(f"✅ Successful steps: {successful_steps}/{len(steps)}")
        print(f"🏠 AssetFraction Backend Demo Complete!")
        
        if self.user_wallet_id:
            print(f"💰 Demo wallet created: {self.user_wallet_id}")
        if self.asset_id:
            print(f"🏠 Demo asset created: {self.asset_id}")


def main():
    """Main demo function"""
    demo = AssetFractionDemo()
    demo.run_complete_demo()


if __name__ == "__main__":
    main()
