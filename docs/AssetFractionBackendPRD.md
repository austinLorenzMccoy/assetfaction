

# 🧰 **AssetFraction Backend PRD (Python + SQLite + Hedera)**

### *Backend for RWA Tokenization and Income Distribution on Hedera*

**Version**: 2.0
**Author**: Augustine Chibueze
**Use Case**: Hedera African Hackathon

---

## 📌 1. Objective

Develop a lightweight, SQLite-powered **backend API** using **FastAPI + Hedera SDK**, to:

* Tokenize real estate and art assets into NFTs + fractional FTs on Hedera
* Store and manage user KYC metadata
* Sponsor wallets for users
* Schedule and distribute rental income
* Sync and serve Mirror Node data
* Support a React frontend and mobile PWA

---

## 🧱 2. Architecture Overview

```
FastAPI + SQLite
├── /api/                 # REST endpoints
├── /services/            # Hedera SDK logic
├── /models/              # SQLite ORM models (SQLAlchemy)
├── /schemas/             # Pydantic request/response schemas
├── /tasks/               # Rental payout scheduler (APScheduler)
├── /utils/               # Signature handling, validation, HCS tools
├── main.py               # API runner
└── .env                  # Secrets & config
```

---

## 🧾 3. API Endpoints

| Method | Route                   | Description                           |
| ------ | ----------------------- | ------------------------------------- |
| POST   | `/wallet/create`        | Sponsor and create new Hedera account |
| POST   | `/kyc/submit`           | Submit KYC info, log hash to HCS      |
| POST   | `/assets/tokenize`      | Mint NFT + FT for real estate or art  |
| POST   | `/rewards/schedule`     | Schedule income payout by FT holdings |
| GET    | `/mirror/txs/{account}` | Fetch Mirror Node transaction history |

---

## 🧰 4. Technologies

| Stack Element        | Tool                              |
| -------------------- | --------------------------------- |
| Language             | Python 3.11+                      |
| Web Framework        | FastAPI                           |
| DB                   | SQLite 3 (via SQLAlchemy)         |
| Blockchain SDK       | Hedera SDK for Python             |
| Task Scheduler       | APScheduler                       |
| Wallets              | HashPack / Blade                  |
| Logging              | HCS (Hedera Consensus Service)    |
| Explorer Integration | Mirror Node API (Kabuto / Hashio) |

---

## 🔐 5. Sample `.env`

```ini
# .env
HEDERA_NETWORK=testnet
OPERATOR_ID=0.0.456789
OPERATOR_KEY=302e020100300506032b6570...

TREASURY_ID=0.0.123456
TREASURY_KEY=302e020100300506032b6570...

HCS_TOPIC_ID=0.0.987654
MIRROR_NODE_API=https://testnet.mirrornode.hedera.com/api/v1

JWT_SECRET=supersecretkey
```

---

## 🔄 6. Step-by-Step Backend Implementation

---

### ✅ Phase 1: Wallet Sponsorship & KYC Logging

#### Step 1: `POST /wallet/create`

* Sponsors a new Hedera account with zero-fee onboarding
* Stores wallet ID and public key locally

```python
from hedera import Client, AccountCreateTransaction, PrivateKey

client = Client.for_testnet().set_operator(OPERATOR_ID, OPERATOR_KEY)

def sponsor_wallet(pub_key_str):
    pub_key = PrivateKey.from_string(pub_key_str).public_key
    tx = AccountCreateTransaction().set_key(pub_key).set_initial_balance(0)
    response = tx.execute(client)
    receipt = response.get_receipt(client)
    return receipt.account_id.to_string()
```

#### Step 2: `POST /kyc/submit`

* Accepts `name`, `phone`, `doc_hash`
* Logs KYC hash on HCS
* Stores locally in SQLite

```python
from hedera import TopicMessageSubmitTransaction

def submit_kyc(account_id, kyc_data):
    message = f"{account_id}:{kyc_data['doc_hash']}"
    TopicMessageSubmitTransaction().set_topic_id(HCS_TOPIC_ID).set_message(message).execute(client)
```

---

### ✅ Phase 2: Asset Tokenization API

#### Step 3: `POST /assets/tokenize`

* Mint 1-of-1 NFT for real estate/artwork
* Create fungible token linked to that NFT (10,000 units)
* Store both token IDs and metadata in SQLite

```python
def tokenize_asset(asset_data):
    # Mint NFT with metadata (deed, location, valuation)
    # Mint FT with 10,000 supply
    # Store in local DB: NFT_ID, FT_ID, asset_type, metadata
    pass
```

---

### ✅ Phase 3: Income Distribution

#### Step 4: `POST /rewards/schedule`

* Calculate share % of rental income for each token holder
* Schedule monthly payouts using **APScheduler**

```python
from apscheduler.schedulers.background import BackgroundScheduler

def distribute_income(ft_id, total_income):
    holders = db.get_token_holders(ft_id)
    for holder in holders:
        amount = total_income * holder.share
        send_hbar(holder.account_id, amount)

scheduler = BackgroundScheduler()
scheduler.add_job(lambda: distribute_income("0.0.XXXX", 500), "interval", weeks=4)
scheduler.start()
```

---

### ✅ Phase 4: Mirror Node Integration

#### Step 5: `GET /mirror/txs/{account}`

* Calls Hedera Mirror Node API
* Returns asset-related activity (FT buys, NFT mints, royalties)

```python
import requests

def get_account_transactions(account_id):
    url = f"{MIRROR_NODE_API}/accounts/{account_id}/transactions"
    res = requests.get(url)
    return res.json()
```

---

## 📊 7. SQLite DB Schema (via SQLAlchemy)

```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    wallet_id = Column(String, unique=True)
    public_key = Column(String)
    kyc_verified = Column(Boolean, default=False)

class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True)
    nft_id = Column(String)
    ft_id = Column(String)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class Holding(Base):
    __tablename__ = "holdings"
    id = Column(Integer, primary_key=True)
    wallet_id = Column(String)
    ft_id = Column(String)
    amount = Column(Float)
```

---

## ✅ 8. Testing & Local Dev Setup

### Dev Setup

```bash
# 1. Clone repo
git clone https://github.com/yourname/assetfraction-backend

# 2. Setup virtual env
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run server
uvicorn main:app --reload
```

### Key Dependencies

```txt
fastapi
uvicorn
python-dotenv
sqlalchemy
apscheduler
requests
hedera-sdk-py
```

---

## 🔐 9. Security Practices

| Area         | Best Practice                                |
| ------------ | -------------------------------------------- |
| Secret keys  | Loaded via `.env` using `python-dotenv`      |
| Transactions | Signed securely with private keys in env     |
| DB Access    | Input sanitization with Pydantic models      |
| Rate Limits  | `fastapi-limiter` (optional for production)  |
| Logging      | KYC only logs SHA256 doc hashes, not raw PII |

---

## 📝 10. Final Notes

* SQLite is portable for MVP/hackathon use and can be upgraded to PostgreSQL later
* Scheduler (APScheduler) replaces Celery for simplicity
* Designed to work with low-bandwidth wallets + mobile-first frontend

---

## ✅ Ready to Build?

Would you like me to:

* Generate the FastAPI project scaffold with SQLite?
* Auto-deploy the SQLite DB and run test cases?
* Package the code as a public GitHub repo?

Let’s deploy **AssetFraction’s backend** and win the Hedera Hackathon 💥