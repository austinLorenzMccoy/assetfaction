// Type definitions for AssetFraction app

export interface Asset {
  id: number
  title: string
  location: string
  image: string
  totalValue: number
  tokenPrice: number
  tokensAvailable: number
  totalTokens: number
  investors: number
  monthlyReturn: number
  annualReturn: number
  verified: boolean
  featured: boolean
  type: string
  category: string
  description: string
  documents: string[]
  nftId: string
  tokenId: string
  yearBuilt: number
  occupancy: number
  nextIncomePayout: string
  riskLevel: string
  minInvestment: number
  tags: string[]
  propertyManager: string
  lastValuation: string
  curator?: string
  artist?: string
  yearCreated?: number
  medium?: string
  dimensions?: string
  provenance?: string
  exhibitions?: string[]
  culturalSignificance?: string
}

export interface User {
  id: string
  name: string
  email: string
  phone: string
  kycStatus: string
  walletAddress: string
  totalInvested: number
  totalEarnings: number
  walletBalance: number
  joinDate: string
  riskProfile: string
  profileImage: string
  referralCode: string
  referralEarnings: number
  investmentGoals: {
    targetAmount: number
    timeframe: string
    riskTolerance: string
  }
  achievements: Achievement[]
  assets: AssetHolding[]
}

export interface Achievement {
  id: string
  title: string
  description: string
  icon: string
  earnedDate: string
  category: string
}

export interface AssetHolding {
  assetId: number
  tokensOwned: number
  totalInvested: number
  currentValue: number
  totalReturns: number
  purchaseDate: string
}

export interface Notification {
  id: number
  type: string
  message: string
  time: string
  read: boolean
}

export interface KycData {
  name: string
  phone: string
  document: File | null
}

export interface Transaction {
  id: string
  type: string
  amount: number
  asset: string
  date: string
  status: string
  hash: string
}
