"use client"

import { useState, useEffect, useCallback, useMemo } from "react"
import { motion, AnimatePresence, useSpring, useTransform, useScroll } from "framer-motion"
import {
  Home,
  Building2,
  Wallet,
  TrendingUp,
  History,
  ArrowUp,
  ArrowDown,
  MapPin,
  DollarSign,
  Users,
  Check,
  Upload,
  Search,
  ChevronRight,
  Star,
  Shield,
  Zap,
  Bell,
  Share2,
  CheckCircle,
  Loader,
  Copy,
  QrCode,
  Menu,
  X,
  Heart,
  Award,
  Target,
  BarChart3,
  Activity,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Separator } from "@/components/ui/separator"

// Enhanced mock data with more realistic African assets
const mockAssets = [
  {
    id: 1,
    title: "Prime Lagos Apartment Complex",
    location: "Victoria Island, Lagos, Nigeria",
    image: "/placeholder.svg?height=300&width=400",
    totalValue: 250000,
    tokenPrice: 25,
    tokensAvailable: 8500,
    totalTokens: 10000,
    investors: 156,
    monthlyReturn: 8.5,
    annualReturn: 12.4,
    verified: true,
    featured: true,
    type: "real-estate",
    category: "Residential",
    description:
      "Modern 24-unit apartment complex in prime Victoria Island location. Fully occupied with stable rental income and excellent growth potential.",
    documents: ["title_deed.pdf", "valuation_report.pdf", "rental_agreement.pdf"],
    nftId: "0.0.123456",
    tokenId: "0.0.123457",
    yearBuilt: 2019,
    occupancy: 96,
    nextIncomePayout: "2024-08-15",
    riskLevel: "Low",
    minInvestment: 5,
    tags: ["High Yield", "Prime Location", "Fully Occupied"],
    propertyManager: "Lagos Property Group",
    lastValuation: "2024-06-01",
  },
  {
    id: 2,
    title: "Contemporary Art Collection",
    location: "Accra, Ghana",
    image: "/placeholder.svg?height=300&width=400",
    totalValue: 150000,
    tokenPrice: 15,
    tokensAvailable: 6200,
    totalTokens: 10000,
    investors: 89,
    monthlyReturn: 12.3,
    annualReturn: 18.7,
    verified: true,
    featured: true,
    type: "art",
    category: "Contemporary",
    description:
      "Curated collection of 15 contemporary African artworks by emerging and established artists. Exhibited in prestigious galleries across West Africa.",
    documents: ["authenticity_cert.pdf", "appraisal_report.pdf", "insurance_policy.pdf"],
    nftId: "0.0.234567",
    tokenId: "0.0.234568",
    artist: "Multiple Artists",
    exhibition: "Accra Art Gallery",
    nextIncomePayout: "2024-08-20",
    riskLevel: "Medium",
    minInvestment: 5,
    tags: ["High Growth", "Cultural Value", "Emerging Artists"],
    curator: "West African Art Collective",
    lastValuation: "2024-07-01",
  },
  {
    id: 3,
    title: "Nairobi Commercial Building",
    location: "Westlands, Nairobi, Kenya",
    image: "/placeholder.svg?height=300&width=400",
    totalValue: 180000,
    tokenPrice: 18,
    tokensAvailable: 7800,
    totalTokens: 10000,
    investors: 203,
    monthlyReturn: 6.8,
    annualReturn: 9.2,
    verified: true,
    featured: false,
    type: "real-estate",
    category: "Commercial",
    description:
      "5-story commercial building housing offices and retail spaces in Westlands business district. Strategic location with excellent transport links.",
    documents: ["commercial_lease.pdf", "building_permit.pdf", "tax_clearance.pdf"],
    nftId: "0.0.345678",
    tokenId: "0.0.345679",
    yearBuilt: 2021,
    occupancy: 88,
    nextIncomePayout: "2024-08-10",
    riskLevel: "Low",
    minInvestment: 5,
    tags: ["Stable Income", "Commercial Hub", "Growing Area"],
    propertyManager: "Nairobi Commercial Properties",
    lastValuation: "2024-05-15",
  },
  {
    id: 4,
    title: "Cape Town Wine Estate",
    location: "Stellenbosch, South Africa",
    image: "/placeholder.svg?height=300&width=400",
    totalValue: 320000,
    tokenPrice: 32,
    tokensAvailable: 9100,
    totalTokens: 10000,
    investors: 67,
    monthlyReturn: 5.5,
    annualReturn: 8.1,
    verified: true,
    featured: true,
    type: "real-estate",
    category: "Agricultural",
    description:
      "Historic wine estate with 50 hectares of vineyards and modern production facilities. Award-winning wines with international distribution.",
    documents: ["land_title.pdf", "wine_license.pdf", "production_report.pdf"],
    nftId: "0.0.456789",
    tokenId: "0.0.456790",
    yearBuilt: 1890,
    occupancy: 100,
    nextIncomePayout: "2024-08-25",
    riskLevel: "Medium",
    minInvestment: 10,
    tags: ["Heritage Property", "Wine Production", "Tourism Potential"],
    propertyManager: "Stellenbosch Wine Estates",
    lastValuation: "2024-04-20",
  },
  {
    id: 5,
    title: "Kigali Tech Hub",
    location: "Kigali, Rwanda",
    image: "/placeholder.svg?height=300&width=400",
    totalValue: 200000,
    tokenPrice: 20,
    tokensAvailable: 9500,
    totalTokens: 10000,
    investors: 45,
    monthlyReturn: 7.2,
    annualReturn: 10.8,
    verified: true,
    featured: false,
    type: "real-estate",
    category: "Technology",
    description:
      "State-of-the-art technology hub in Kigali's innovation district. Home to multiple tech startups and international companies.",
    documents: ["tech_hub_license.pdf", "tenant_agreements.pdf", "development_permit.pdf"],
    nftId: "0.0.567890",
    tokenId: "0.0.567891",
    yearBuilt: 2022,
    occupancy: 92,
    nextIncomePayout: "2024-08-18",
    riskLevel: "Medium",
    minInvestment: 5,
    tags: ["Tech Hub", "Innovation District", "High Growth"],
    propertyManager: "Rwanda Development Board",
    lastValuation: "2024-06-10",
  },
  {
    id: 6,
    title: "Traditional Sculpture Collection",
    location: "Benin City, Nigeria",
    image: "/placeholder.svg?height=300&width=400",
    totalValue: 120000,
    tokenPrice: 12,
    tokensAvailable: 8900,
    totalTokens: 10000,
    investors: 78,
    monthlyReturn: 15.2,
    annualReturn: 22.8,
    verified: true,
    featured: false,
    type: "art",
    category: "Traditional",
    description:
      "Rare collection of traditional Benin bronze sculptures and artifacts. Authenticated pieces with significant cultural and historical value.",
    documents: ["cultural_heritage_cert.pdf", "authenticity_docs.pdf", "museum_appraisal.pdf"],
    nftId: "0.0.678901",
    tokenId: "0.0.678902",
    artist: "Traditional Benin Artisans",
    exhibition: "National Museum of Nigeria",
    nextIncomePayout: "2024-08-22",
    riskLevel: "High",
    minInvestment: 5,
    tags: ["Cultural Heritage", "Museum Quality", "Rare Artifacts"],
    curator: "Benin Cultural Foundation",
    lastValuation: "2024-07-05",
  },
]

const mockUser = {
  id: "0.0.12345",
  name: "Amara Okafor",
  email: "amara.okafor@example.com",
  phone: "+234 803 123 4567",
  kycStatus: "verified",
  walletAddress: "0.0.12345",
  totalInvested: 3450,
  totalEarnings: 287.5,
  walletBalance: 1258.3,
  joinDate: "2024-06-15",
  riskProfile: "moderate",
  preferredCurrency: "USD",
  notifications: true,
  profileImage: "/placeholder.svg?height=100&width=100",
  assets: [
    { assetId: 1, tokens: 40, value: 1000, monthlyIncome: 34.5, purchaseDate: "2024-07-01", performance: 8.2 },
    { assetId: 2, tokens: 25, value: 375, monthlyIncome: 15.75, purchaseDate: "2024-07-10", performance: 12.1 },
    { assetId: 3, tokens: 60, value: 1080, monthlyIncome: 22.44, purchaseDate: "2024-07-15", performance: 6.8 },
    { assetId: 4, tokens: 15, value: 480, monthlyIncome: 8.8, purchaseDate: "2024-07-20", performance: 5.5 },
    { assetId: 5, tokens: 30, value: 600, monthlyIncome: 18.2, purchaseDate: "2024-07-25", performance: 7.2 },
  ],
  referralCode: "AMARA2024",
  referralEarnings: 45.5,
  achievements: ["First Investment", "Diversified Portfolio", "Top Investor"],
  investmentGoals: {
    target: 10000,
    current: 3450,
    timeline: "12 months",
  },
}

const mockTransactions = [
  {
    id: 1,
    type: "buy",
    asset: "Prime Lagos Apartment Complex",
    amount: 1000,
    tokens: 40,
    date: "2024-07-25",
    status: "completed",
    txHash: "0.0.1234567890",
    fee: 10,
  },
  {
    id: 2,
    type: "income",
    asset: "Contemporary Art Collection",
    amount: 15.75,
    date: "2024-07-20",
    status: "completed",
    txHash: "0.0.1234567891",
    fee: 0,
  },
  {
    id: 3,
    type: "buy",
    asset: "Nairobi Commercial Building",
    amount: 540,
    tokens: 30,
    date: "2024-07-15",
    status: "completed",
    txHash: "0.0.1234567892",
    fee: 5.4,
  },
  {
    id: 4,
    type: "income",
    asset: "Prime Lagos Apartment Complex",
    amount: 34.5,
    date: "2024-07-12",
    status: "completed",
    txHash: "0.0.1234567893",
    fee: 0,
  },
  {
    id: 5,
    type: "referral",
    asset: "Referral Bonus",
    amount: 25.5,
    date: "2024-07-08",
    status: "completed",
    txHash: "0.0.1234567894",
    fee: 0,
  },
  {
    id: 6,
    type: "buy",
    asset: "Cape Town Wine Estate",
    amount: 480,
    tokens: 15,
    date: "2024-07-05",
    status: "completed",
    txHash: "0.0.1234567895",
    fee: 4.8,
  },
]

// Main App Component
export default function AssetFractionApp() {
  const [currentPage, setCurrentPage] = useState("home")
  const [user, setUser] = useState(null)
  const [selectedAsset, setSelectedAsset] = useState(null)
  const [investmentAmount, setInvestmentAmount] = useState("")
  const [kycData, setKycData] = useState({ name: "", phone: "", document: null })
  const [searchTerm, setSearchTerm] = useState("")
  const [filterType, setFilterType] = useState("all")
  const [loading, setLoading] = useState(false)
  const [notifications, setNotifications] = useState([])
  const [showWalletModal, setShowWalletModal] = useState(false)
  const [showShareModal, setShowShareModal] = useState(false)
  const [sortBy, setSortBy] = useState("featured")
  const [showNotifications, setShowNotifications] = useState(false)
  const [showMobileMenu, setShowMobileMenu] = useState(false)
  const [favoriteAssets, setFavoriteAssets] = useState([])
  const [darkMode, setDarkMode] = useState(false)

  // Enhanced state management with localStorage persistence
  useEffect(() => {
    const savedUser = localStorage.getItem("assetfraction_user")
    const savedNotifications = localStorage.getItem("assetfraction_notifications")
    const savedFavorites = localStorage.getItem("assetfraction_favorites")
    const savedDarkMode = localStorage.getItem("assetfraction_darkmode")

    if (savedUser) {
      setUser(JSON.parse(savedUser))
    }
    if (savedNotifications) {
      setNotifications(JSON.parse(savedNotifications))
    }
    if (savedFavorites) {
      setFavoriteAssets(JSON.parse(savedFavorites))
    }
    if (savedDarkMode) {
      setDarkMode(JSON.parse(savedDarkMode))
    }

    // Add sample notifications
    if (!savedNotifications) {
      const sampleNotifications = [
        {
          id: 1,
          type: "income",
          message: "Income payment received: $34.50 from Lagos Apartment Complex",
          time: "2 hours ago",
          read: false,
        },
        {
          id: 2,
          type: "investment",
          message: "New investment opportunity: Kigali Tech Hub now available",
          time: "1 day ago",
          read: true,
        },
        { id: 3, type: "kyc", message: "KYC verification completed successfully", time: "3 days ago", read: true },
        {
          id: 4,
          type: "achievement",
          message: "Achievement unlocked: Diversified Portfolio!",
          time: "5 days ago",
          read: false,
        },
      ]
      setNotifications(sampleNotifications)
      localStorage.setItem("assetfraction_notifications", JSON.stringify(sampleNotifications))
    }
  }, [])

  // Enhanced wallet connection simulation
  const handleLogin = useCallback(() => {
    setLoading(true)
    setTimeout(() => {
      setUser(mockUser)
      localStorage.setItem("assetfraction_user", JSON.stringify(mockUser))
      setLoading(false)
      setCurrentPage("marketplace")
    }, 1500)
  }, [])

  // Enhanced KYC submission with file handling
  const handleKycSubmit = useCallback(() => {
    if (!kycData.name || !kycData.phone) {
      alert("Please fill in all required fields")
      return
    }

    setLoading(true)

    setTimeout(() => {
      const newUser = {
        ...mockUser,
        name: kycData.name,
        phone: kycData.phone,
        kycStatus: "pending",
      }
      setUser(newUser)
      localStorage.setItem("assetfraction_user", JSON.stringify(newUser))
      setLoading(false)

      const newNotification = {
        id: Date.now(),
        type: "kyc",
        message: "KYC submitted successfully. Verification in progress.",
        time: "Just now",
        read: false,
      }
      const updatedNotifications = [newNotification, ...notifications]
      setNotifications(updatedNotifications)
      localStorage.setItem("assetfraction_notifications", JSON.stringify(updatedNotifications))

      setCurrentPage("marketplace")
    }, 2000)
  }, [kycData, notifications])

  // Enhanced investment handling with validation
  const handleInvestment = useCallback(
    (assetId, amount) => {
      if (!user || !amount || amount < 5) {
        alert("Minimum investment is $5")
        return
      }

      if (amount > user.walletBalance) {
        alert("Insufficient wallet balance")
        return
      }

      setLoading(true)

      setTimeout(() => {
        const asset = mockAssets.find((a) => a.id === assetId)
        const tokens = Math.floor(amount / asset.tokenPrice)

        const updatedUser = {
          ...user,
          totalInvested: user.totalInvested + Number.parseFloat(amount),
          walletBalance: user.walletBalance - Number.parseFloat(amount),
          assets: [
            ...user.assets,
            {
              assetId: assetId,
              tokens: tokens,
              value: Number.parseFloat(amount),
              monthlyIncome: (Number.parseFloat(amount) * asset.monthlyReturn) / 100,
              purchaseDate: new Date().toISOString().split("T")[0],
              performance: asset.monthlyReturn,
            },
          ],
        }

        setUser(updatedUser)
        localStorage.setItem("assetfraction_user", JSON.stringify(updatedUser))

        const newNotification = {
          id: Date.now(),
          type: "investment",
          message: `Successfully invested $${amount} in ${asset.title}`,
          time: "Just now",
          read: false,
        }
        const updatedNotifications = [newNotification, ...notifications]
        setNotifications(updatedNotifications)
        localStorage.setItem("assetfraction_notifications", JSON.stringify(updatedNotifications))

        setInvestmentAmount("")
        setLoading(false)
        setCurrentPage("portfolio")
      }, 1500)
    },
    [user, notifications],
  )

  // Toggle favorite asset
  const toggleFavorite = (assetId) => {
    const updatedFavorites = favoriteAssets.includes(assetId)
      ? favoriteAssets.filter((id) => id !== assetId)
      : [...favoriteAssets, assetId]

    setFavoriteAssets(updatedFavorites)
    localStorage.setItem("assetfraction_favorites", JSON.stringify(updatedFavorites))
  }

  // Copy to clipboard functionality
  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      alert("Copied to clipboard!")
    })
  }

  // Enhanced asset filtering and sorting
  const filteredAssets = mockAssets
    .filter((asset) => {
      const matchesSearch =
        asset.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        asset.location.toLowerCase().includes(searchTerm.toLowerCase())
      const matchesFilter = filterType === "all" || asset.type === filterType
      return matchesSearch && matchesFilter
    })
    .sort((a, b) => {
      switch (sortBy) {
        case "return":
          return b.monthlyReturn - a.monthlyReturn
        case "price":
          return a.tokenPrice - b.tokenPrice
        case "funded":
          return (
            (b.totalTokens - b.tokensAvailable) / b.totalTokens - (a.totalTokens - a.tokensAvailable) / a.totalTokens
          )
        case "featured":
          return b.featured - a.featured
        default:
          return 0
      }
    })

  // Enhanced Header Component
  const Header = () => (
    <header className="bg-white dark:bg-gray-900 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div className="px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <Building2 className="text-white" size={20} />
              </div>
              <span className="font-bold text-xl text-gray-900 dark:text-white">AssetFraction</span>
            </div>
          </div>

          {!user ? (
            <div className="flex space-x-2">
              <Button
                onClick={() => setCurrentPage("onboard")}
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium"
              >
                Get Started
              </Button>
            </div>
          ) : (
            <div className="flex items-center space-x-3">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowNotifications(true)}
                className="relative p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg"
              >
                <Bell size={20} className="text-gray-600 dark:text-gray-300" />
                {notifications.some((n) => !n.read) && (
                  <div className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full"></div>
                )}
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowWalletModal(true)}
                className="flex items-center space-x-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg px-3 py-2"
              >
                <Avatar className="w-6 h-6">
                  <AvatarImage src={user.profileImage || "/placeholder.svg"} alt={user.name} />
                  <AvatarFallback className="text-xs">
                    {user.name
                      .split(" ")
                      .map((n) => n[0])
                      .join("")}
                  </AvatarFallback>
                </Avatar>
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300 hidden sm:block">
                  ${user.walletBalance.toFixed(2)}
                </span>
              </Button>
              <Button variant="ghost" size="sm" onClick={() => setShowMobileMenu(true)} className="sm:hidden">
                <Menu size={20} />
              </Button>
            </div>
          )}
        </div>
      </div>
    </header>
  )

  // Enhanced Navigation Component
  const Navigation = () => (
    <nav className="bg-white dark:bg-gray-900 shadow-lg border-t border-gray-200 dark:border-gray-700 fixed bottom-0 left-0 right-0 z-50">
      <div className="flex justify-around py-2">
        {[
          { id: "home", icon: Home, label: "Home" },
          { id: "marketplace", icon: Building2, label: "Market" },
          { id: "portfolio", icon: Wallet, label: "Portfolio" },
          { id: "history", icon: History, label: "History" },
        ].map(({ id, icon: Icon, label }) => (
          <Button
            key={id}
            variant="ghost"
            onClick={() => setCurrentPage(id)}
            className={`flex flex-col items-center p-2 ${
              currentPage === id ? "text-blue-600" : "text-gray-500 dark:text-gray-400"
            }`}
          >
            <Icon size={20} />
            <span className="text-xs mt-1">{label}</span>
          </Button>
        ))}
      </div>
    </nav>
  )

  // Loading Component
  const LoadingSpinner = () => (
    <div className="flex items-center justify-center p-8">
      <div className="flex flex-col items-center space-y-4">
        <Loader className="animate-spin text-blue-600" size={32} />
        <span className="text-gray-600 dark:text-gray-400">Loading...</span>
      </div>
    </div>
  )

  // Enhanced Notification Modal
  const NotificationModal = () => (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-end sm:items-center sm:justify-center">
      <div className="bg-white dark:bg-gray-800 w-full sm:w-96 sm:rounded-2xl rounded-t-2xl p-6 max-h-96 overflow-y-auto">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white">Notifications</h3>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setShowNotifications(false)}
            className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
          >
            <X size={20} />
          </Button>
        </div>
        <div className="space-y-4">
          {notifications.map((notification) => (
            <div
              key={notification.id}
              className={`p-4 rounded-xl border transition-colors ${
                notification.read
                  ? "bg-gray-50 dark:bg-gray-700 border-gray-200 dark:border-gray-600"
                  : "bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-700"
              }`}
            >
              <div className="flex items-start space-x-3">
                <div
                  className={`p-2 rounded-lg ${
                    notification.type === "income"
                      ? "bg-green-100 dark:bg-green-900/30"
                      : notification.type === "investment"
                        ? "bg-blue-100 dark:bg-blue-900/30"
                        : notification.type === "achievement"
                          ? "bg-purple-100 dark:bg-purple-900/30"
                          : "bg-yellow-100 dark:bg-yellow-900/30"
                  }`}
                >
                  {notification.type === "income" ? (
                    <DollarSign size={16} className="text-green-600" />
                  ) : notification.type === "investment" ? (
                    <TrendingUp size={16} className="text-blue-600" />
                  ) : notification.type === "achievement" ? (
                    <Award size={16} className="text-purple-600" />
                  ) : (
                    <CheckCircle size={16} className="text-yellow-600" />
                  )}
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900 dark:text-white">{notification.message}</p>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">{notification.time}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )

  // Enhanced Wallet Modal
  const WalletModal = () => (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 w-full max-w-sm">
        <div className="text-center mb-6">
          <Avatar className="w-16 h-16 mx-auto mb-4">
            <AvatarImage src={user?.profileImage || "/placeholder.svg"} alt={user?.name} />
            <AvatarFallback className="text-lg">
              {user?.name
                ?.split(" ")
                .map((n) => n[0])
                .join("")}
            </AvatarFallback>
          </Avatar>
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">{user?.name}</h3>
          <div className="bg-gray-100 dark:bg-gray-700 p-4 rounded-lg">
            <QrCode className="mx-auto mb-2 text-gray-600 dark:text-gray-400" size={48} />
            <p className="text-xs text-gray-600 dark:text-gray-400 mb-2">Wallet Address</p>
            <p className="font-mono text-sm text-gray-900 dark:text-white">{user?.walletAddress}</p>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => copyToClipboard(user?.walletAddress)}
              className="mt-2 flex items-center justify-center mx-auto text-blue-600 text-sm"
            >
              <Copy size={16} />
              <span className="ml-1">Copy</span>
            </Button>
          </div>
        </div>
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <span className="text-gray-600 dark:text-gray-400">Balance</span>
            <span className="font-semibold text-gray-900 dark:text-white">${user?.walletBalance?.toFixed(2)}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-gray-600 dark:text-gray-400">Total Invested</span>
            <span className="font-semibold text-gray-900 dark:text-white">
              ${user?.totalInvested?.toLocaleString()}
            </span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-gray-600 dark:text-gray-400">Total Earnings</span>
            <span className="font-semibold text-green-600">${user?.totalEarnings}</span>
          </div>
          <Separator />
          <div className="flex justify-between items-center">
            <span className="text-gray-600 dark:text-gray-400">KYC Status</span>
            <Badge variant={user?.kycStatus === "verified" ? "default" : "secondary"}>
              {user?.kycStatus === "verified" ? "Verified" : "Pending"}
            </Badge>
          </div>
        </div>
        <div className="flex space-x-3 mt-6">
          <Button variant="outline" onClick={() => setShowShareModal(true)} className="flex-1">
            <Share2 size={16} className="mr-2" />
            Refer
          </Button>
          <Button onClick={() => setShowWalletModal(false)} className="flex-1 bg-blue-600 hover:bg-blue-700 text-white">
            Close
          </Button>
        </div>
      </div>
    </div>
  )

  // Enhanced Share Modal
  const ShareModal = () => (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 w-full max-w-sm">
        <div className="text-center mb-6">
          <div className="w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
            <Share2 className="text-white" size={24} />
          </div>
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">Refer Friends</h3>
          <p className="text-gray-600 dark:text-gray-400">
            Share your referral code and earn 5% of their first investment
          </p>
        </div>
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 p-4 rounded-lg mb-4">
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">Your Referral Code</p>
          <div className="flex items-center justify-between">
            <span className="font-bold text-lg text-gray-900 dark:text-white">{user?.referralCode}</span>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => copyToClipboard(user?.referralCode)}
              className="text-blue-600"
            >
              <Copy size={20} />
            </Button>
          </div>
        </div>
        <div className="text-center mb-6">
          <p className="text-sm text-gray-600 dark:text-gray-400">Total Referral Earnings</p>
          <p className="text-2xl font-bold text-green-600">${user?.referralEarnings}</p>
        </div>
        <Button onClick={() => setShowShareModal(false)} className="w-full bg-blue-600 hover:bg-blue-700 text-white">
          Close
        </Button>
      </div>
    </div>
  )

  return (
    <div className={`max-w-md mx-auto bg-gray-50 dark:bg-gray-900 min-h-screen relative ${darkMode ? "dark" : ""}`}>
      <Header />

      {/* Main Content */}
      <main className="pb-20">
        {loading && <LoadingSpinner />}

        {/* Home Page */}
        {currentPage === "home" && (
          <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
            {/* Hero Section */}
            <div className="px-6 py-12">
              <div className="text-center mb-12">
                <div className="mb-6">
                  <div className="w-20 h-20 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
                    <Building2 className="text-white" size={32} />
                  </div>
                </div>
                <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
                  Own Real Estate & Art
                  <br />
                  <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                    From $5
                  </span>
                </h1>
                <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-2xl mx-auto leading-relaxed">
                  Invest in fractional ownership of premium African real estate and art. Built on Hedera for instant,
                  transparent, and secure transactions.
                </p>
              </div>

              {/* Stats */}
              <div className="grid grid-cols-3 gap-4 mb-12">
                <div className="text-center">
                  <div className="text-2xl font-bold text-gray-900 dark:text-white">$2.5M+</div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Assets Value</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-gray-900 dark:text-white">1,200+</div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Investors</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-gray-900 dark:text-white">12.4%</div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">Avg Return</div>
                </div>
              </div>

              {/* Feature Cards */}
              <div className="grid gap-6 mb-12">
                {[
                  {
                    icon: DollarSign,
                    title: "Start from $5",
                    description: "Minimum investment of just $5 makes wealth building accessible to everyone",
                    color: "from-green-500 to-emerald-500",
                  },
                  {
                    icon: Zap,
                    title: "Instant Liquidity",
                    description: "Trade your fractions anytime with built-in DeFi integration",
                    color: "from-yellow-500 to-orange-500",
                  },
                  {
                    icon: Shield,
                    title: "Fully Transparent",
                    description: "All transactions verified on Hedera blockchain with complete audit trail",
                    color: "from-blue-500 to-purple-500",
                  },
                ].map(({ icon: Icon, title, description, color }, index) => (
                  <Card
                    key={index}
                    className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border-0 shadow-lg hover:shadow-xl transition-all duration-300"
                  >
                    <CardContent className="p-6">
                      <div
                        className={`w-12 h-12 bg-gradient-to-r ${color} rounded-xl flex items-center justify-center mb-4`}
                      >
                        <Icon className="text-white" size={24} />
                      </div>
                      <h3 className="font-semibold text-lg mb-2 text-gray-900 dark:text-white">{title}</h3>
                      <p className="text-gray-600 dark:text-gray-300">{description}</p>
                    </CardContent>
                  </Card>
                ))}
              </div>

              {/* CTA */}
              <div className="text-center">
                <Button
                  onClick={() => (user ? setCurrentPage("marketplace") : setCurrentPage("onboard"))}
                  className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-8 py-4 rounded-xl text-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-200"
                  size="lg"
                >
                  {user ? "Explore Assets" : "Start Investing Today"}
                </Button>
              </div>
            </div>
          </div>
        )}

        {/* Onboarding Page */}
        {currentPage === "onboard" && (
          <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-4">
            <div className="max-w-md mx-auto">
              <Card className="bg-white dark:bg-gray-800 shadow-xl border-0">
                <CardHeader className="text-center pb-6">
                  <div className="w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
                    <Building2 className="text-white" size={24} />
                  </div>
                  <CardTitle className="text-2xl font-bold text-gray-900 dark:text-white">Join AssetFraction</CardTitle>
                  <CardDescription className="text-gray-600 dark:text-gray-400">
                    Complete KYC to start investing
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Full Name</label>
                    <Input
                      type="text"
                      required
                      value={kycData.name}
                      onChange={(e) => setKycData({ ...kycData, name: e.target.value })}
                      placeholder="Enter your full name"
                      className="w-full"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Phone Number
                    </label>
                    <Input
                      type="tel"
                      required
                      value={kycData.phone}
                      onChange={(e) => setKycData({ ...kycData, phone: e.target.value })}
                      placeholder="+234 XXX XXX XXXX"
                      className="w-full"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Identity Document
                    </label>
                    <div className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-6 text-center">
                      <Upload className="mx-auto text-gray-400 mb-2" size={32} />
                      <p className="text-sm text-gray-600 dark:text-gray-400">Upload your ID or passport</p>
                      <input
                        type="file"
                        accept="image/*,.pdf"
                        onChange={(e) => setKycData({ ...kycData, document: e.target.files[0] })}
                        className="hidden"
                        id="document-upload"
                      />
                      <label
                        htmlFor="document-upload"
                        className="mt-2 inline-block bg-blue-600 text-white px-4 py-2 rounded-lg cursor-pointer hover:bg-blue-700"
                      >
                        Choose File
                      </label>
                    </div>
                  </div>

                  <Button
                    onClick={handleKycSubmit}
                    className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 font-semibold"
                    disabled={loading}
                  >
                    {loading ? "Processing..." : "Submit KYC & Create Wallet"}
                  </Button>

                  <div className="text-center">
                    <Button variant="ghost" onClick={handleLogin} className="text-blue-600 hover:text-blue-700 text-sm">
                      Already have an account? Sign in
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        )}

        {/* Marketplace Page */}
        {currentPage === "marketplace" && (
          <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
            <div className="p-4">
              <div className="mb-6">
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Asset Marketplace</h1>
                <p className="text-gray-600 dark:text-gray-400">Discover fractional investment opportunities</p>
              </div>

              {/* Search and Filters */}
              <div className="mb-6 space-y-4">
                <div className="relative">
                  <Search className="absolute left-3 top-3 text-gray-400" size={20} />
                  <Input
                    type="text"
                    placeholder="Search assets..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10"
                  />
                </div>

                <div className="flex space-x-4">
                  <Select value={filterType} onValueChange={setFilterType}>
                    <SelectTrigger className="flex-1">
                      <SelectValue placeholder="Asset Type" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All Types</SelectItem>
                      <SelectItem value="real-estate">Real Estate</SelectItem>
                      <SelectItem value="art">Art</SelectItem>
                    </SelectContent>
                  </Select>

                  <Select value={sortBy} onValueChange={setSortBy}>
                    <SelectTrigger className="flex-1">
                      <SelectValue placeholder="Sort By" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="featured">Featured</SelectItem>
                      <SelectItem value="return">Highest Return</SelectItem>
                      <SelectItem value="price">Lowest Price</SelectItem>
                      <SelectItem value="funded">Most Funded</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              {/* Asset Grid */}
              <div className="space-y-6">
                {filteredAssets.map((asset) => (
                  <Card
                    key={asset.id}
                    className="bg-white dark:bg-gray-800 shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer border-0 overflow-hidden"
                    onClick={() => {
                      setSelectedAsset(asset)
                      setCurrentPage("asset-detail")
                    }}
                  >
                    <div className="relative">
                      <img
                        src={asset.image || "/placeholder.svg"}
                        alt={asset.title}
                        className="w-full h-48 object-cover"
                      />
                      <div className="absolute top-4 left-4 flex space-x-2">
                        {asset.featured && (
                          <Badge className="bg-gradient-to-r from-yellow-500 to-orange-500 text-white border-0">
                            <Star size={12} className="mr-1" />
                            Featured
                          </Badge>
                        )}
                        {asset.verified && (
                          <Badge className="bg-green-500 text-white border-0">
                            <Check size={12} className="mr-1" />
                            Verified
                          </Badge>
                        )}
                      </div>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={(e) => {
                          e.stopPropagation()
                          toggleFavorite(asset.id)
                        }}
                        className="absolute top-4 right-4 bg-white/80 hover:bg-white"
                      >
                        <Heart
                          size={16}
                          className={favoriteAssets.includes(asset.id) ? "text-red-500 fill-current" : "text-gray-600"}
                        />
                      </Button>
                    </div>

                    <CardContent className="p-6">
                      <div className="mb-4">
                        <h3 className="font-semibold text-lg text-gray-900 dark:text-white mb-2">{asset.title}</h3>
                        <div className="flex items-center text-gray-600 dark:text-gray-400 mb-3">
                          <MapPin size={16} />
                          <span className="ml-1 text-sm">{asset.location}</span>
                        </div>
                        <div className="flex flex-wrap gap-2 mb-4">
                          {asset.tags.slice(0, 2).map((tag, index) => (
                            <Badge key={index} variant="secondary" className="text-xs">
                              {tag}
                            </Badge>
                          ))}
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-4 mb-4">
                        <div className="text-center p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                          <p className="text-xs text-gray-600 dark:text-gray-400">Token Price</p>
                          <p className="font-semibold text-blue-600">${asset.tokenPrice}</p>
                        </div>
                        <div className="text-center p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
                          <p className="text-xs text-gray-600 dark:text-gray-400">Monthly Return</p>
                          <p className="font-semibold text-green-600">{asset.monthlyReturn}%</p>
                        </div>
                      </div>

                      <div className="mb-4">
                        <div className="flex justify-between text-sm text-gray-600 dark:text-gray-400 mb-2">
                          <span>Funding Progress</span>
                          <span>
                            {(((asset.totalTokens - asset.tokensAvailable) / asset.totalTokens) * 100).toFixed(1)}%
                          </span>
                        </div>
                        <Progress
                          value={((asset.totalTokens - asset.tokensAvailable) / asset.totalTokens) * 100}
                          className="h-2"
                        />
                      </div>

                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-4 text-sm text-gray-600 dark:text-gray-400">
                          <span className="flex items-center">
                            <Users size={16} />
                            <span className="ml-1">{asset.investors}</span>
                          </span>
                          <Badge
                            variant="outline"
                            className={`text-xs ${
                              asset.riskLevel === "Low"
                                ? "text-green-600 border-green-600"
                                : asset.riskLevel === "Medium"
                                  ? "text-yellow-600 border-yellow-600"
                                  : "text-red-600 border-red-600"
                            }`}
                          >
                            {asset.riskLevel} Risk
                          </Badge>
                        </div>
                        <ChevronRight className="text-gray-400" size={20} />
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Asset Detail Page */}
        {currentPage === "asset-detail" && selectedAsset && (
          <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
            <div className="relative">
              <img
                src={selectedAsset.image || "/placeholder.svg"}
                alt={selectedAsset.title}
                className="w-full h-64 object-cover"
              />
              <Button
                variant="ghost"
                onClick={() => setCurrentPage("marketplace")}
                className="absolute top-4 left-4 bg-white/80 hover:bg-white text-gray-900"
              >
                ← Back
              </Button>
              <Button
                variant="ghost"
                onClick={() => toggleFavorite(selectedAsset.id)}
                className="absolute top-4 right-4 bg-white/80 hover:bg-white"
              >
                <Heart
                  size={20}
                  className={favoriteAssets.includes(selectedAsset.id) ? "text-red-500 fill-current" : "text-gray-600"}
                />
              </Button>
            </div>

            <div className="p-6 space-y-6">
              <div>
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">{selectedAsset.title}</h1>
                    <div className="flex items-center text-gray-600 dark:text-gray-400 mb-3">
                      <MapPin size={20} />
                      <span className="ml-2">{selectedAsset.location}</span>
                    </div>
                  </div>
                  <div className="flex space-x-2">
                    {selectedAsset.verified && (
                      <Badge className="bg-green-500 text-white">
                        <Check size={12} className="mr-1" />
                        Verified
                      </Badge>
                    )}
                    <Badge
                      variant="outline"
                      className={`${
                        selectedAsset.riskLevel === "Low"
                          ? "text-green-600 border-green-600"
                          : selectedAsset.riskLevel === "Medium"
                            ? "text-yellow-600 border-yellow-600"
                            : "text-red-600 border-red-600"
                      }`}
                    >
                      {selectedAsset.riskLevel} Risk
                    </Badge>
                  </div>
                </div>

                <div className="flex flex-wrap gap-2 mb-6">
                  {selectedAsset.tags.map((tag, index) => (
                    <Badge key={index} variant="secondary">
                      {tag}
                    </Badge>
                  ))}
                </div>

                <p className="text-gray-600 dark:text-gray-400 leading-relaxed mb-6">{selectedAsset.description}</p>
              </div>

              {/* Key Metrics */}
              <div className="grid grid-cols-2 gap-4">
                <Card className="bg-gradient-to-r from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20 border-0">
                  <CardContent className="p-4 text-center">
                    <p className="text-sm text-gray-600 dark:text-gray-400">Total Value</p>
                    <p className="text-2xl font-bold text-blue-600">${selectedAsset.totalValue.toLocaleString()}</p>
                  </CardContent>
                </Card>
                <Card className="bg-gradient-to-r from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20 border-0">
                  <CardContent className="p-4 text-center">
                    <p className="text-sm text-gray-600 dark:text-gray-400">Monthly Return</p>
                    <p className="text-2xl font-bold text-green-600">{selectedAsset.monthlyReturn}%</p>
                  </CardContent>
                </Card>
              </div>

              {/* Detailed Stats */}
              <Card className="bg-white dark:bg-gray-800 border-0">
                <CardContent className="p-6 space-y-4">
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-400">Token Price</span>
                    <span className="font-semibold text-gray-900 dark:text-white">${selectedAsset.tokenPrice}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-400">Available Tokens</span>
                    <span className="font-semibold text-gray-900 dark:text-white">
                      {selectedAsset.tokensAvailable.toLocaleString()}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-400">Total Investors</span>
                    <span className="font-semibold text-gray-900 dark:text-white">{selectedAsset.investors}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-400">Annual Return</span>
                    <span className="font-semibold text-green-600">{selectedAsset.annualReturn}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-400">Min Investment</span>
                    <span className="font-semibold text-gray-900 dark:text-white">${selectedAsset.minInvestment}</span>
                  </div>
                </CardContent>
              </Card>

              {/* Investment Section */}
              {user && (
                <Card className="bg-white dark:bg-gray-800 border-0">
                  <CardHeader>
                    <CardTitle className="text-lg text-gray-900 dark:text-white">Invest Now</CardTitle>
                    <CardDescription>Start building wealth with fractional ownership</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex space-x-4">
                      <Input
                        type="number"
                        placeholder="Investment amount ($)"
                        value={investmentAmount}
                        onChange={(e) => setInvestmentAmount(e.target.value)}
                        min={selectedAsset.minInvestment}
                        className="flex-1"
                      />
                      <Button
                        onClick={() => handleInvestment(selectedAsset.id, Number.parseFloat(investmentAmount))}
                        disabled={
                          !investmentAmount ||
                          Number.parseFloat(investmentAmount) < selectedAsset.minInvestment ||
                          loading
                        }
                        className="bg-blue-600 hover:bg-blue-700 text-white px-6"
                      >
                        {loading ? "Processing..." : "Invest"}
                      </Button>
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-400">
                      <p>Minimum investment: ${selectedAsset.minInvestment}</p>
                      {investmentAmount && (
                        <p>
                          You'll get {Math.floor(Number.parseFloat(investmentAmount) / selectedAsset.tokenPrice)} tokens
                        </p>
                      )}
                    </div>
                  </CardContent>
                </Card>
              )}
            </div>
          </div>
        )}

        {/* Portfolio Page */}
        {currentPage === "portfolio" && (
          <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
            {!user ? (
              <div className="flex items-center justify-center min-h-screen p-4">
                <Card className="bg-white dark:bg-gray-800 border-0 shadow-xl">
                  <CardContent className="p-8 text-center">
                    <Wallet className="mx-auto text-gray-400 mb-4" size={64} />
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Connect Your Wallet</h2>
                    <p className="text-gray-600 dark:text-gray-400 mb-6">Sign in to view your portfolio</p>
                    <Button
                      onClick={() => setCurrentPage("onboard")}
                      className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3"
                    >
                      Get Started
                    </Button>
                  </CardContent>
                </Card>
              </div>
            ) : (
              <div className="p-4 space-y-6">
                <div className="text-center mb-6">
                  <Avatar className="w-20 h-20 mx-auto mb-4">
                    <AvatarImage src={user.profileImage || "/placeholder.svg"} alt={user.name} />
                    <AvatarFallback className="text-xl">
                      {user.name
                        .split(" ")
                        .map((n) => n[0])
                        .join("")}
                    </AvatarFallback>
                  </Avatar>
                  <h1 className="text-2xl font-bold text-gray-900 dark:text-white">{user.name}</h1>
                  <p className="text-gray-600 dark:text-gray-400">
                    Member since {new Date(user.joinDate).toLocaleDateString()}
                  </p>
                </div>

                {/* Summary Cards */}
                <div className="grid grid-cols-2 gap-4">
                  <Card className="bg-gradient-to-r from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20 border-0">
                    <CardContent className="p-4 text-center">
                      <TrendingUp className="mx-auto mb-2 text-blue-600" size={24} />
                      <p className="text-sm text-gray-600 dark:text-gray-400">Total Invested</p>
                      <p className="text-2xl font-bold text-gray-900 dark:text-white">
                        ${user.totalInvested.toLocaleString()}
                      </p>
                    </CardContent>
                  </Card>
                  <Card className="bg-gradient-to-r from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20 border-0">
                    <CardContent className="p-4 text-center">
                      <DollarSign className="mx-auto mb-2 text-green-600" size={24} />
                      <p className="text-sm text-gray-600 dark:text-gray-400">Total Earnings</p>
                      <p className="text-2xl font-bold text-green-600">${user.totalEarnings}</p>
                    </CardContent>
                  </Card>
                </div>

                <Card className="bg-gradient-to-r from-purple-50 to-purple-100 dark:from-purple-900/20 dark:to-purple-800/20 border-0">
                  <CardContent className="p-4 text-center">
                    <Wallet className="mx-auto mb-2 text-purple-600" size={24} />
                    <p className="text-sm text-gray-600 dark:text-gray-400">Wallet Balance</p>
                    <p className="text-2xl font-bold text-purple-600">${user.walletBalance.toFixed(2)}</p>
                  </CardContent>
                </Card>

                {/* Investment Goal Progress */}
                <Card className="bg-white dark:bg-gray-800 border-0">
                  <CardHeader>
                    <CardTitle className="flex items-center text-gray-900 dark:text-white">
                      <Target className="mr-2" size={20} />
                      Investment Goal
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600 dark:text-gray-400">Progress</span>
                      <span className="font-medium text-gray-900 dark:text-white">
                        ${user.investmentGoals.current.toLocaleString()} / $
                        {user.investmentGoals.target.toLocaleString()}
                      </span>
                    </div>
                    <Progress
                      value={(user.investmentGoals.current / user.investmentGoals.target) * 100}
                      className="h-3"
                    />
                    <p className="text-xs text-gray-600 dark:text-gray-400">
                      {((user.investmentGoals.current / user.investmentGoals.target) * 100).toFixed(1)}% complete •{" "}
                      {user.investmentGoals.timeline} timeline
                    </p>
                  </CardContent>
                </Card>

                {/* Achievements */}
                <Card className="bg-white dark:bg-gray-800 border-0">
                  <CardHeader>
                    <CardTitle className="flex items-center text-gray-900 dark:text-white">
                      <Award className="mr-2" size={20} />
                      Achievements
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="flex flex-wrap gap-2">
                      {user.achievements.map((achievement, index) => (
                        <Badge
                          key={index}
                          className="bg-gradient-to-r from-yellow-500 to-orange-500 text-white border-0"
                        >
                          <Star size={12} className="mr-1" />
                          {achievement}
                        </Badge>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                {/* Portfolio Tabs */}
                <Tabs defaultValue="assets" className="w-full">
                  <TabsList className="grid w-full grid-cols-3">
                    <TabsTrigger value="assets">My Assets</TabsTrigger>
                    <TabsTrigger value="performance">Performance</TabsTrigger>
                    <TabsTrigger value="income">Income</TabsTrigger>
                  </TabsList>

                  <TabsContent value="assets" className="space-y-4">
                    {user.assets.map((holding) => {
                      const asset = mockAssets.find((a) => a.id === holding.assetId)
                      return (
                        <Card key={holding.assetId} className="bg-white dark:bg-gray-800 border-0">
                          <CardContent className="p-4">
                            <div className="flex items-center space-x-4">
                              <img
                                src={asset?.image || "/placeholder.svg"}
                                alt={asset?.title}
                                className="w-16 h-16 rounded-lg object-cover"
                              />
                              <div className="flex-1">
                                <h4 className="font-medium text-gray-900 dark:text-white">{asset?.title}</h4>
                                <p className="text-sm text-gray-600 dark:text-gray-400">{holding.tokens} tokens</p>
                                <div className="flex items-center space-x-4 mt-2">
                                  <div>
                                    <p className="text-xs text-gray-500">Value</p>
                                    <p className="font-semibold text-gray-900 dark:text-white">${holding.value}</p>
                                  </div>
                                  <div>
                                    <p className="text-xs text-gray-500">Monthly Income</p>
                                    <p className="font-semibold text-green-600">${holding.monthlyIncome.toFixed(2)}</p>
                                  </div>
                                  <div>
                                    <p className="text-xs text-gray-500">Performance</p>
                                    <p className="font-semibold text-blue-600">{holding.performance}%</p>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </CardContent>
                        </Card>
                      )
                    })}
                  </TabsContent>

                  <TabsContent value="performance" className="space-y-4">
                    <Card className="bg-white dark:bg-gray-800 border-0">
                      <CardHeader>
                        <CardTitle className="flex items-center text-gray-900 dark:text-white">
                          <BarChart3 className="mr-2" size={20} />
                          Portfolio Performance
                        </CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-4">
                          <div className="flex justify-between items-center">
                            <span className="text-gray-600 dark:text-gray-400">Total Return</span>
                            <span className="font-semibold text-green-600">+8.3%</span>
                          </div>
                          <div className="flex justify-between items-center">
                            <span className="text-gray-600 dark:text-gray-400">Best Performer</span>
                            <span className="font-semibold text-gray-900 dark:text-white">
                              Contemporary Art Collection
                            </span>
                          </div>
                          <div className="flex justify-between items-center">
                            <span className="text-gray-600 dark:text-gray-400">Diversification Score</span>
                            <Badge className="bg-green-500 text-white">Excellent</Badge>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  </TabsContent>

                  <TabsContent value="income" className="space-y-4">
                    <Card className="bg-white dark:bg-gray-800 border-0">
                      <CardHeader>
                        <CardTitle className="flex items-center text-gray-900 dark:text-white">
                          <Activity className="mr-2" size={20} />
                          Income Summary
                        </CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-4">
                          <div className="flex justify-between items-center">
                            <span className="text-gray-600 dark:text-gray-400">This Month</span>
                            <span className="font-semibold text-green-600">
                              ${user.assets.reduce((sum, asset) => sum + asset.monthlyIncome, 0).toFixed(2)}
                            </span>
                          </div>
                          <div className="flex justify-between items-center">
                            <span className="text-gray-600 dark:text-gray-400">Next Payout</span>
                            <span className="font-semibold text-gray-900 dark:text-white">Aug 15, 2024</span>
                          </div>
                          <div className="flex justify-between items-center">
                            <span className="text-gray-600 dark:text-gray-400">Referral Earnings</span>
                            <span className="font-semibold text-purple-600">${user.referralEarnings}</span>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  </TabsContent>
                </Tabs>
              </div>
            )}
          </div>
        )}

        {/* History Page */}
        {currentPage === "history" && (
          <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
            <div className="p-4">
              <div className="mb-6">
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Transaction History</h1>
                <p className="text-gray-600 dark:text-gray-400">All your investment activities</p>
              </div>

              <Card className="bg-white dark:bg-gray-800 border-0 shadow-lg">
                <CardContent className="p-0">
                  {mockTransactions.map((tx, index) => (
                    <div
                      key={tx.id}
                      className={`p-4 ${index !== mockTransactions.length - 1 ? "border-b border-gray-200 dark:border-gray-700" : ""}`}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          <div
                            className={`p-2 rounded-lg ${
                              tx.type === "buy"
                                ? "bg-blue-100 dark:bg-blue-900/30"
                                : tx.type === "income"
                                  ? "bg-green-100 dark:bg-green-900/30"
                                  : "bg-purple-100 dark:bg-purple-900/30"
                            }`}
                          >
                            {tx.type === "buy" ? (
                              <ArrowUp className="text-blue-600" size={16} />
                            ) : tx.type === "income" ? (
                              <ArrowDown className="text-green-600" size={16} />
                            ) : (
                              <Share2 className="text-purple-600" size={16} />
                            )}
                          </div>
                          <div>
                            <p className="font-medium text-gray-900 dark:text-white">
                              {tx.type === "buy" ? "Investment" : tx.type === "income" ? "Income" : "Referral"}
                            </p>
                            <p className="text-sm text-gray-600 dark:text-gray-400">{tx.asset}</p>
                            {tx.tokens && <p className="text-xs text-gray-500">{tx.tokens} tokens</p>}
                          </div>
                        </div>
                        <div className="text-right">
                          <p className={`font-semibold ${tx.type === "buy" ? "text-red-600" : "text-green-600"}`}>
                            {tx.type === "buy" ? "-" : "+"}${tx.amount}
                          </p>
                          <p className="text-sm text-gray-600 dark:text-gray-400">{tx.date}</p>
                          <Badge variant="outline" className="text-xs mt-1">
                            {tx.status}
                          </Badge>
                        </div>
                      </div>
                      <div className="mt-2 flex items-center justify-between text-xs text-gray-500">
                        <span>
                          TX: {tx.txHash.slice(0, 10)}...{tx.txHash.slice(-6)}
                        </span>
                        {tx.fee > 0 && <span>Fee: ${tx.fee}</span>}
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>
            </div>
          </div>
        )}
      </main>

      {/* Navigation */}
      {currentPage !== "home" && currentPage !== "onboard" && currentPage !== "asset-detail" && <Navigation />}

      {/* Modals */}
      {showNotifications && <NotificationModal />}
      {showWalletModal && <WalletModal />}
      {showShareModal && <ShareModal />}
    </div>
  )
}
