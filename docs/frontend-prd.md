# 🏠 *AssetFraction – Democratizing Real World Asset Ownership via Hedera*

*PRD for the Hedera African Hackathon*

---

## 📌 1. Vision & Value Proposition

### ❗ *Problem*

Millions of Africans are locked out of wealth-building assets like *real estate and fine art* due to:

* High capital requirements (e.g., \$10k+ entry)
* Illiquidity and limited exit options
* Fraud, title forgery, and lack of transparency
* Little to no access to fractional ownership or digital asset exposure

### ✅ *Solution*

*AssetFraction* is a *Hedera-native RWA tokenization platform* that:

* Tokenizes real-world assets (real estate, art) as *HTS NFTs* and *Fungible Tokens*
* Enables *fractional ownership from as low as \$5*
* Provides instant liquidity through *DeFi integrations*
* Uses *HCS and Mirror Nodes* for *auditable provenance & KYC trails*
* Distributes *rental or sale proceeds* automatically via scheduled transactions

---

## 💡 2. Why It’s a Game-Changer

| Benefit                           | Description                                        |
| --------------------------------- | -------------------------------------------------- |
| 🔓 *Financial Inclusion*        | Micro-investment starting at \$5                   |
| ⚡ *Instant Liquidity*           | Built-in DeFi support via SaucerSwap               |
| 🛡 *Trust & Compliance*         | KYC enforced via HTS custom fees and HCS           |
| 🎨 *Creator Royalties*          | Artists earn resale revenue via smart contracts    |
| 💸 *Gasless UX*                 | All user fees sponsored — no barrier to entry      |
| 📱 *WhatsApp KYC Flow*          | Mobile-friendly onboarding for low-bandwidth users |
| 🧾 *Proof of Legality*          | Chainlink oracles + document verification          |
| 📊 *Audit Trail & Transparency* | Public HCS & Mirror Node explorer support          |

---

## 🔧 3. Core Features

### 🧱 A. *Asset Tokenization Engine*

* *NFTs for Properties/Art*: Each property/art piece becomes an HTS NFT with metadata: deed hash, location, legal docs.
* *Fractionalization*: Each NFT is linked to a pool of 10,000 fungible tokens (FTs) on Hedera.
* *Compliance Layer*: KYC-verified accounts only (via HTS custom fees).

### 🔁 B. *Fraction Marketplace*

* *Buy/Sell Fractions*: Via SaucerSwap LP pools (HBAR or stablecoin pairs).
* *Liquidity Mining*: Token holders earn APR by staking in pools.
* *Automated Income Distribution*: Rental revenue shared via scheduled transfers.

### 📱 C. *User Experience*

* *WhatsApp KYC Onboarding*: Human-verifiable low-bandwidth identity flow.
* *Mobile PWA*: React-based progressive web app with offline capability.
* *Investor Dashboard*: Visual portfolio breakdown, earnings tracker, proof-of-ownership explorer.

---

## ⚙ 4. Technical Architecture

mermaid
graph TD
    A[User PWA] --> B[Hedera SDK Integration]
    B --> C[HTS: NFT + FT Minting]
    B --> D[HSCS Smart Contracts]
    C --> E[HCS for Audit Trail & KYC]
    D --> F[Scheduled Tx: Income Distribution]
    C --> G[SaucerSwap AMM Pools]
    G --> H[Token Swap Engine]
    B --> I[Mirror Node API]
    I --> J[Explorer + Analytics]


---

## 🧪 5. Step-by-Step Implementation Plan

### 🏗 *Phase 1 – Infrastructure & Tokenization (Week 1)*

1. ✅ *NFT Minting for Real Estate/Art*

   * Mint 1-of-1 HTS NFTs for each asset
   * Embed metadata:

     * Title deed hash (IPFS)
     * Geo-location
     * Ownership docs
     * Verified chainlink hash of physical records

2. ✅ *Fungible Token Issuance*

   * Link NFT to FT supply (e.g., 10,000 \$FRACT-ACCRA-001)
   * Enable token association for buyers
   * Use Hedera *custom fee schedules* to add compliance logic

3. ✅ *Chainlink Oracle Integration*

   * Fetch up-to-date valuation feeds
   * Trigger alerts for price anomalies

---

### 💸 *Phase 2 – Smart Contracts & DeFi (Week 2)*

1. ✅ *Royalty Enforcement via HSCS*

   * Smart contract intercepts resale transactions and sends 5% to original asset owner (or artist)
   * Supports resale across different NFT pools

2. ✅ *Income Distribution*

   * Schedule monthly rental yield via *Scheduled Transactions*
   * Transaction batch based on proportional holdings

3. ✅ *Liquidity Pool Integration*

   * Add pairs to *SaucerSwap DEX*
   * Enable *APR rewards* for LP stakers
   * Use contracts to withdraw LP earnings and compound

---

### 📱 *Phase 3 – Frontend + KYC (Week 3)*

1. ✅ *WhatsApp KYC Flow*

   * User provides phone number + selfie
   * Platform verifies and stores KYC hash on *HCS topic*
   * Once verified, account creation transaction is *sponsored*

2. ✅ *Mobile-First PWA*

   * Built with React + Tailwind
   * Works with HashPack & Blade wallets
   * Tracks:

     * Token balances
     * NFT ownership
     * Earnings (live via Mirror Node)
     * Trade history

3. ✅ *Document Verification UI*

   * Display title, deed, and valuation documents via IPFS links
   * Enable 3rd-party notaries to confirm documents on-chain

---

## 🔍 6. Hedera-Specific Leverage

| Component           | Hedera Feature        | Benefit                       |
| ------------------- | --------------------- | ----------------------------- |
| Asset Tokenization  | HTS (NFTs + FTs)      | Fractional ownership at scale |
| Income Distribution | Scheduled Tx          | No missed payouts             |
| Proof of Identity   | HCS                   | KYC logs & auditability       |
| Smart Contracts     | HSCS (EVM)            | Royalty logic, staking        |
| Transparency        | Mirror Node + GraphQL | Verifiable trades, balances   |
| Gasless UX          | HTS Sponsored Fees    | Zero barrier onboarding       |

---

## 🧰 7. Repository Structure


AssetFraction/
├── contracts/
│   ├── RoyaltyDistributor.sol
│   └── TokenizeAsset.js
├── frontend/
│   ├── pages/
│   ├── components/
│   └── App.jsx
├── backend/
│   └── mirror-queries.js
├── assets/
│   └── docs/ (sample titles, valuations)
└── scripts/
    ├── deploy_contracts.js
    └── mint_nft_and_ft.js


---

## 💸 8. Business Model

| Revenue Stream             | Fee                 |
| -------------------------- | ------------------- |
| Asset onboarding fee       | 0.5% of asset value |
| Fraction buy/sell trades   | 1.0% platform fee   |
| LP staking performance fee | 10% of earned APR   |

---

## 📊 9. KPIs & Hackathon Metrics

| Metric             | Goal                               |
| ------------------ | ---------------------------------- |
| Token Holders      | 5,000 wallets                      |
| Transactions       | 50,000/month                       |
| NFTs Minted        | 250 real estate, 500 art           |
| DeFi Activity      | \$100k TVL in LPs                  |
| Mirror Node Events | Visible income proof               |
| Demo Deliverables  | PWA + Contract TXs + Explorer Logs |

---

## 📽 10. Demo Plan

### ✅ Must-Show Screens

1. Mint NFT + FT → Live on Hedera (HTS)
2. KYC & Account Sponsorship → WhatsApp to Wallet
3. Buy \$5 worth of a fraction → Real swap on SaucerSwap
4. NFT resale → Auto-royalty trigger (5% to artist)
5. Income payout → TX proof on Mirror Node

### ✅ Tech Stack

* *Frontend*: React + Tailwind + Wagmi
* *Backend*: Node.js + Hedera SDK
* *Smart Contracts*: Solidity (HSCS)
* *Explorer*: [Hedera Mirror Node](https://explorer.kabuto.sh/)
* *DEX*: [SaucerSwap](https://app.saucerswap.finance)

---

## ✅ 11. Final Checklist

| Task                           | Status         |
| ------------------------------ | -------------- |
| Smart Contract Audit (Slither) | ✅              |
| Live PWA (Testnet)             | ✅              |
| HTS NFT + FT Minting           | ✅              |
| KYC Flow on WhatsApp           | ✅              |
| Explorer Verification (Mirror) | ✅              |
| GitHub Repo Public             | ✅              |
| Hackathon Video Demo           | 🎥 In Progress |

---

## 🧭 12. Next Steps

1. 🎯 *Clone Starter Kit*

   bash
   git clone https://github.com/hashgraph/hedera-accelerator-defi
   

2. 💸 *Request Testnet HBAR*
   [https://hedera.com/testnet-faucet](https://hedera.com/testnet-faucet)

3. 💬 *Join Developer Support*
   Hedera Discord → #africa-hackathon channel

4. 🎤 *Prepare Pitch Deck & Demo*

---

## 🚀 Let's Fractionalize Africa's Wealth — Together

*AssetFraction* unlocks *accessible, liquid, onchain investment* for millions across Africa, powered by *Hedera’s speed, affordability, and trustless architecture*.

Let’s bridge the gap between physical wealth and digital opportunity — \$5 at a time. # 🌍 AssetFraction Frontend PRD

*Platform*: Progressive Web App (React)
*Target Users*: African retail investors
*Goal*: Make fractional real-world asset investment accessible and trustless
*Version*: 1.0
*Last Updated*: July 2025

---

## 🚀 1. Vision

> Empower users in Africa to invest in real estate and art via onchain, fractional ownership with zero-gas fees and full transparency.

The frontend must be:

* Extremely easy to use (for mobile-first + low-tech users)
* Integrated with Hedera smart contracts via backend API
* Able to visualize wallet balances, asset values, KYC status, and passive income flow

---

## 🧩 2. Core User Flows

### 🧑‍💼 A. New User Onboarding

* Input: Public key (or generate in-app)
* Create wallet → Store in localStorage
* Submit KYC (Name, Phone, Document Upload)
* KYC submission gets hashed → sent to HCS via backend

### 🏘 B. Asset Exploration

* Explore tokenized properties and artworks
* View asset metadata (location, valuation, artwork image, returns)
* View NFT and FT token IDs

### 💰 C. Fractional Investment

* Connect HashPack or Blade Wallet
* Purchase fractions of the asset (min \$5)
* See investment breakdown: no. of tokens owned, % share

### 📈 D. Rental Yield Tracking

* View rental income earned (live from Mirror Node or backend)
* See next scheduled payout date
* Claim income or allow auto-distribution

### 🔁 E. Transaction History

* Display user’s transaction history from Mirror Node
* Types: Token purchase, NFT mint, yield, referral bonus

---

## 🧱 3. Architecture Overview


React PWA (Frontend)
├── /pages
│   ├── Home.tsx             # Hero + What is AssetFraction
│   ├── Onboard.tsx          # KYC & Wallet onboarding
│   ├── Marketplace.tsx      # List of tokenized assets
│   ├── AssetDetails.tsx     # Single asset info + Invest
│   ├── Portfolio.tsx        # View owned assets + earnings
│   ├── History.tsx          # Mirror node TXs
│   └── Admin.tsx            # Admin upload panel (optional)
├── /components
│   ├── Navbar.tsx
│   ├── AssetCard.tsx
│   ├── KYCForm.tsx
│   ├── WalletBanner.tsx
├── /api                     # Axios-based API wrappers
├── /hooks                   # Wallet, Auth, Data hooks
├── /utils
│   └── formatters.ts
└── /public
    └── logos, icons, metadata


---

## 💡 4. Technical Stack

| Component        | Tech                               |
| ---------------- | ---------------------------------- |
| Framework        | React 18 (PWA)                     |
| UI Framework     | TailwindCSS + shadcn/ui            |
| Wallet Support   | HashPack SDK / Blade Extension     |
| State Management | Zustand / Redux                    |
| Routing          | React Router                       |
| HTTP Client      | Axios                              |
| Auth             | JWT (localStorage) or wallet login |
| Deployment       | Vercel / Netlify                   |

---

## 📦 5. Backend API Integration

| Endpoint                      | Use In Frontend Page       |
| ----------------------------- | -------------------------- |
| POST /wallet/create         | Onboard.tsx                |
| POST /kyc/submit            | Onboard.tsx                |
| POST /assets/tokenize       | Admin.tsx (optional panel) |
| GET /mirror/txs/:account    | History.tsx                |
| POST /rewards/schedule      | Backend-triggered          |
| Custom GET /portfolio/:user | Portfolio.tsx              |
| GET /assets/all             | Marketplace.tsx            |

---

## 🧭 6. Detailed Page Wireframes + Features

### 📍 A. Home.tsx

* Tagline, Call to Action, Explainer animation/video
* Wallet Connect Button
* CTA to explore the marketplace

### 👤 B. Onboard.tsx

* KYC form: Full name, phone, upload ID
* Wallet generation or connect existing
* On submit:

  * KYC hash → backend → HCS
  * Wallet account sponsored → returned and saved

### 🏘 C. Marketplace.tsx

* List of tokenized assets
* Search and filter by location, asset type
* Each AssetCard shows:

  * Image
  * Title
  * Price per token
  * Invest button (opens modal)

### 📄 D. AssetDetails.tsx

* Detailed page with asset description, documents
* Price, token availability
* "Buy Tokens" form
* Stats: Total investors, average income return

### 💼 E. Portfolio.tsx

* My Assets tab

  * List of NFTs & fractions held
  * Earnings summary (monthly/yearly)
* My Wallet tab

  * Wallet ID
  * Balance
* My Income tab

  * Expected vs. Claimed rental income

### 🔄 F. History.tsx

* Table of all transactions from Mirror Node API
* Columns: Type, Asset, Date, Amount, Status

---

## 📲 7. UI/UX Requirements

| Feature              | Spec                                   |
| -------------------- | -------------------------------------- |
| Mobile-first Design  | Must look good on Android <6"          |
| PWA                  | Should install like an app             |
| Offline Read Caching | Marketplace & portfolio pages          |
| Zero Gas Wallet UX   | Use sponsored transactions via backend |
| NFT Gallery Support  | Show fractional NFTs with owner status |
| Animations           | Framer Motion + Tailwind Transitions   |
| Accessibility (a11y) | Semantic HTML, contrast & alt texts    |

---

## 🧪 8. Testing Plan

| Area            | Tool                             | Coverage |
| --------------- | -------------------------------- | -------- |
| Unit Tests      | Vitest / Jest                    | 80%+     |
| Component Tests | React Testing Library            | ✅        |
| API Contract    | MSW (Mock Service Worker)        | ✅        |
| E2E Tests       | Cypress (marketplace → buy flow) | ✅        |

---

## 🛠 9. Developer Setup Guide

### Local Setup

bash
# Clone repo
git clone https://github.com/assetfraction/frontend
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev


### .env

env
VITE_API_BASE_URL=http://localhost:8000
VITE_HEDERA_NETWORK=testnet


---

## ✅ 10. Success Criteria

| Metric                  | Target |
| ----------------------- | ------ |
| PWA Lighthouse Score    | >90    |
| Pages Fully Integrated  | 100%   |
| Mobile UX Pass          | ✅      |
| Wallet UX (gasless)     | ✅      |
| Working KYC + Portfolio | ✅      |

---

## 🚀 Optional Enhancements

* Referral program UI
* DAO proposal voting UI
* Token leaderboard with animated ranks
* AI valuation suggestions (for Admin)

---

## 👥 Collaboration Plan

| Role           | Responsibility                   |
| -------------- | -------------------------------- |
| Frontend Dev   | Build all UI pages               |
| Backend Dev    | Maintain API + DB                |
| Designer       | Create Tailwind-compatible Figma |
| Blockchain Dev | Integrate Hedera + Mirror        |

---

## 🔚 Final Notes

This frontend PRD balances clarity, modularity, and simplicity. You can launch MVP with just:

* Wallet connect
* KYC submission
* Asset buy flow
* Portfolio tracking

Then iterate with dashboards, analytics, and DAO tools.