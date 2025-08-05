{!user ? (
            <div className="flex space-x-2">
              <button
                onClick={() => setCurrentPage('onboard')}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium"
              >
                Get Started
              </button>
            </div>
          ) : (
            <div className="flex items-center space-x-3">
              <button
                onClick={() => setShowNotifications(true)}
                className="relative p-2 hover:bg-gray-100 rounded-lg"
              >
                <Bell size={20} className="text-gray-600" />
                {notifications.some(n => !n.read) && (
                  <div className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full"></div>
                )}
              </button>
              <button
                onClick={() => setShowWalletModal(true)}
                className="flex items-center space-x-2   const handleKycSubmit = () => {
    ifimport React, { useState, useEffect, useCallback } from 'react';
import { 
  Home, 
  Building2, 
  Wallet, 
  TrendingUp, 
  User, 
  History, 
  Settings,
  ArrowUp,
  ArrowDown,
  Plus,
  Eye,
  MapPin,
  DollarSign,
  Users,
  Calendar,
  Check,
  Upload,
  Search,
  Filter,
  ChevronRight,
  Star,
  Shield,
  Zap,
  Globe,
  Bell,
  Download,
  Share2,
  TrendingDown,
  Info,
  CheckCircle,
  AlertCircle,
  Loader,
  RefreshCw,
  ExternalLink,
  Copy,
  QrCode
} from 'lucide-react';

// Mock data for demonstration
// Enhanced mock data with more realistic African assets
const mockAssets = [
  {
    id: 1,
    title: "Prime Lagos Apartment Complex",
    location: "Victoria Island, Lagos",
    image: "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=400&h=300&fit=crop",
    totalValue: 250000,
    tokenPrice: 25,
    tokensAvailable: 8500,
    totalTokens: 10000,
    investors: 156,
    monthlyReturn: 8.5,
    verified: true,
    type: "real-estate",
    description: "Modern 24-unit apartment complex in prime Victoria Island location. Fully occupied with stable rental income.",
    documents: ["title_deed.pdf", "valuation_report.pdf", "rental_agreement.pdf"],
    nftId: "0.0.123456",
    tokenId: "0.0.123457",
    yearBuilt: 2019,
    occupancy: 96,
    nextIncomePayout: "2024-08-15"
  },
  {
    id: 2,
    title: "Contemporary Art Collection",
    location: "Accra, Ghana",
    image: "https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=400&h=300&fit=crop",
    totalValue: 150000,
    tokenPrice: 15,
    tokensAvailable: 6200,
    totalTokens: 10000,
    investors: 89,
    monthlyReturn: 12.3,
    verified: true,
    type: "art",
    description: "Curated collection of 15 contemporary African artworks by emerging and established artists.",
    documents: ["authenticity_cert.pdf", "appraisal_report.pdf", "insurance_policy.pdf"],
    nftId: "0.0.234567",
    tokenId: "0.0.234568",
    artist: "Multiple Artists",
    exhibition: "Accra Art Gallery",
    nextIncomePayout: "2024-08-20"
  },
  {
    id: 3,
    title: "Nairobi Commercial Building",
    location: "Westlands, Nairobi",
    image: "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=400&h=300&fit=crop",
    totalValue: 180000,
    tokenPrice: 18,
    tokensAvailable: 7800,
    totalTokens: 10000,
    investors: 203,
    monthlyReturn: 6.8,
    verified: true,
    type: "real-estate",
    description: "5-story commercial building housing offices and retail spaces in Westlands business district.",
    documents: ["commercial_lease.pdf", "building_permit.pdf", "tax_clearance.pdf"],
    nftId: "0.0.345678",
    tokenId: "0.0.345679",
    yearBuilt: 2021,
    occupancy: 88,
    nextIncomePayout: "2024-08-10"
  },
  {
    id: 4,
    title: "Cape Town Wine Estate",
    location: "Stellenbosch, South Africa",
    image: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300&fit=crop",
    totalValue: 320000,
    tokenPrice: 32,
    tokensAvailable: 9100,
    totalTokens: 10000,
    investors: 67,
    monthlyReturn: 5.5,
    verified: true,
    type: "real-estate",
    description: "Historic wine estate with 50 hectares of vineyards and modern production facilities.",
    documents: ["land_title.pdf", "wine_license.pdf", "production_report.pdf"],
    nftId: "0.0.456789",
    tokenId: "0.0.456790",
    yearBuilt: 1890,
    occupancy: 100,
    nextIncomePayout: "2024-08-25"
  }
];

const mockUser = {
  id: "0.0.12345",
  name: "John Adebayo",
  email: "john.adebayo@example.com",
  phone: "+234 803 123 4567",
  kycStatus: "verified",
  walletAddress: "0.0.12345",
  totalInvested: 2450,
  totalEarnings: 187.50,
  walletBalance: 458.30,
  joinDate: "2024-06-15",
  riskProfile: "moderate",
  preferredCurrency: "USD",
  notifications: true,
  assets: [
    { assetId: 1, tokens: 40, value: 1000, monthlyIncome: 34.50, purchaseDate: "2024-07-01" },
    { assetId: 2, tokens: 25, value: 375, monthlyIncome: 15.75, purchaseDate: "2024-07-10" },
    { assetId: 3, tokens: 60, value: 1080, monthlyIncome: 22.44, purchaseDate: "2024-07-15" },
    { assetId: 4, tokens: 15, value: 480, monthlyIncome: 8.80, purchaseDate: "2024-07-20" }
  ],
  referralCode: "JOHN2024",
  referralEarnings: 25.50
};

const mockTransactions = [
  { id: 1, type: "buy", asset: "Prime Lagos Apartment Complex", amount: 1000, tokens: 40, date: "2024-07-25", status: "completed", txHash: "0.0.1234567890" },
  { id: 2, type: "income", asset: "Contemporary Art Collection", amount: 15.75, date: "2024-07-20", status: "completed", txHash: "0.0.1234567891" },
  { id: 3, type: "buy", asset: "Nairobi Commercial Building", amount: 540, tokens: 30, date: "2024-07-15", status: "completed", txHash: "0.0.1234567892" },
  { id: 4, type: "income", asset: "Prime Lagos Apartment Complex", amount: 34.50, date: "2024-07-12", status: "completed", txHash: "0.0.1234567893" },
  { id: 5, type: "referral", asset: "Referral Bonus", amount: 25.50, date: "2024-07-08", status: "completed", txHash: "0.0.1234567894" },
  { id: 6, type: "buy", asset: "Cape Town Wine Estate", amount: 480, tokens: 15, date: "2024-07-05", status: "completed", txHash: "0.0.1234567895" }
];

// Main App Component
function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [user, setUser] = useState(null);
  const [selectedAsset, setSelectedAsset] = useState(null);
  const [investmentAmount, setInvestmentAmount] = useState('');
  const [kycData, setKycData] = useState({ name: '', phone: '', document: null });
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [loading, setLoading] = useState(false);
  const [notifications, setNotifications] = useState([]);
  const [showWalletModal, setShowWalletModal] = useState(false);
  const [showShareModal, setShowShareModal] = useState(false);
  const [sortBy, setSortBy] = useState('featured');
  const [showNotifications, setShowNotifications] = useState(false);

  // Enhanced state management with localStorage persistence
  useEffect(() => {
    const savedUser = localStorage.getItem('assetfraction_user');
    const savedNotifications = localStorage.getItem('assetfraction_notifications');
    
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
    if (savedNotifications) {
      setNotifications(JSON.parse(savedNotifications));
    }

    // Add sample notifications
    if (!savedNotifications) {
      const sampleNotifications = [
        { id: 1, type: 'income', message: 'Income payment received: $34.50', time: '2 hours ago', read: false },
        { id: 2, type: 'investment', message: 'New investment opportunity available', time: '1 day ago', read: true },
        { id: 3, type: 'kyc', message: 'KYC verification completed', time: '3 days ago', read: true }
      ];
      setNotifications(sampleNotifications);
      localStorage.setItem('assetfraction_notifications', JSON.stringify(sampleNotifications));
    }
  }, []);

  // Enhanced wallet connection simulation
  const handleLogin = useCallback(() => {
    setLoading(true);
    setTimeout(() => {
      setUser(mockUser);
      localStorage.setItem('assetfraction_user', JSON.stringify(mockUser));
      setLoading(false);
      setCurrentPage('marketplace');
    }, 1500);
  }, []);

  // Enhanced KYC submission with file handling
  const handleKycSubmit = useCallback(() => {
    if (!kycData.name || !kycData.phone) {
      alert('Please fill in all required fields');
      return;
    }
    
    setLoading(true);
    
    // Simulate file upload and KYC processing
    setTimeout(() => {
      const newUser = {
        ...mockUser,
        name: kycData.name,
        phone: kycData.phone,
        kycStatus: 'pending'
      };
      setUser(newUser);
      localStorage.setItem('assetfraction_user', JSON.stringify(newUser));
      setLoading(false);
      
      // Add notification
      const newNotification = {
        id: Date.now(),
        type: 'kyc',
        message: 'KYC submitted successfully. Verification in progress.',
        time: 'Just now',
        read: false
      };
      const updatedNotifications = [newNotification, ...notifications];
      setNotifications(updatedNotifications);
      localStorage.setItem('assetfraction_notifications', JSON.stringify(updatedNotifications));
      
      setCurrentPage('marketplace');
    }, 2000);
  }, [kycData, notifications]);

  // Enhanced investment handling with validation
  const handleInvestment = useCallback((assetId, amount) => {
    if (!user || !amount || amount < 5) {
      alert('Minimum investment is $5');
      return;
    }
    
    if (amount > user.walletBalance) {
      alert('Insufficient wallet balance');
      return;
    }
    
    setLoading(true);
    
    setTimeout(() => {
      const asset = mockAssets.find(a => a.id === assetId);
      const tokens = Math.floor(amount / asset.tokenPrice);
      
      const updatedUser = { 
        ...user,
        totalInvested: user.totalInvested + parseFloat(amount),
        walletBalance: user.walletBalance - parseFloat(amount),
        assets: [
          ...user.assets,
          {
            assetId: assetId,
            tokens: tokens,
            value: parseFloat(amount),
            monthlyIncome: (parseFloat(amount) * asset.monthlyReturn / 100),
            purchaseDate: new Date().toISOString().split('T')[0]
          }
        ]
      };
      
      setUser(updatedUser);
      localStorage.setItem('assetfraction_user', JSON.stringify(updatedUser));
      
      // Add notification
      const newNotification = {
        id: Date.now(),
        type: 'investment',
        message: `Successfully invested ${amount} in ${asset.title}`,
        time: 'Just now',
        read: false
      };
      const updatedNotifications = [newNotification, ...notifications];
      setNotifications(updatedNotifications);
      localStorage.setItem('assetfraction_notifications', JSON.stringify(updatedNotifications));
      
      setInvestmentAmount('');
      setLoading(false);
      setCurrentPage('portfolio');
    }, 1500);
  }, [user, notifications]);

  // Copy to clipboard functionality
  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      alert('Copied to clipboard!');
    });
  };

  // Enhanced asset filtering and sorting
  const filteredAssets = mockAssets.filter(asset => {
    const matchesSearch = asset.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         asset.location.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterType === 'all' || asset.type === filterType;
    return matchesSearch && matchesFilter;
  }).sort((a, b) => {
    switch (sortBy) {
      case 'return':
        return b.monthlyReturn - a.monthlyReturn;
      case 'price':
        return a.tokenPrice - b.tokenPrice;
      case 'funded':
        return ((b.totalTokens - b.tokensAvailable) / b.totalTokens) - ((a.totalTokens - a.tokensAvailable) / a.totalTokens);
      default:
        return 0;
    }
  });

  // Enhanced Navigation Component with notifications
  const Navigation = () => (
    <nav className="bg-white shadow-lg border-t">
      <div className="flex justify-around py-2">
        {[
          { id: 'home', icon: Home, label: 'Home' },
          { id: 'marketplace', icon: Building2, label: 'Market' },
          { id: 'portfolio', icon: Wallet, label: 'Portfolio' },
          { id: 'history', icon: History, label: 'History' }
        ].map(({ id, icon: Icon, label }) => (
          <button
            key={id}
            onClick={() => setCurrentPage(id)}
            className={`flex flex-col items-center p-2 ${
              currentPage === id ? 'text-blue-600' : 'text-gray-500'
            }`}
          >
            <Icon size={20} />
            <span className="text-xs mt-1">{label}</span>
          </button>
        ))}
      </div>
    </nav>
  );

  // Loading Component
  const LoadingSpinner = () => (
    <div className="flex items-center justify-center p-4">
      <Loader className="animate-spin text-blue-600" size={24} />
      <span className="ml-2 text-gray-600">Loading...</span>
    </div>
  );

  // Notification Modal
  const NotificationModal = () => (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-end">
      <div className="bg-white w-full rounded-t-2xl p-4 max-h-96 overflow-y-auto">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">Notifications</h3>
          <button
            onClick={() => setShowNotifications(false)}
            className="text-gray-500 hover:text-gray-700"
          >
            ×
          </button>
        </div>
        <div className="space-y-3">
          {notifications.map((notification) => (
            <div
              key={notification.id}
              className={`p-3 rounded-lg border ${
                notification.read ? 'bg-gray-50' : 'bg-blue-50 border-blue-200'
              }`}
            >
              <div className="flex items-start space-x-3">
                <div className={`p-1 rounded-full ${
                  notification.type === 'income' ? 'bg-green-100' :
                  notification.type === 'investment' ? 'bg-blue-100' : 'bg-yellow-100'
                }`}>
                  {notification.type === 'income' ? <DollarSign size={16} className="text-green-600" /> :
                   notification.type === 'investment' ? <TrendingUp size={16} className="text-blue-600" /> :
                   <CheckCircle size={16} className="text-yellow-600" />}
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium">{notification.message}</p>
                  <p className="text-xs text-gray-500">{notification.time}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  // Wallet Modal
  const WalletModal = () => (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl p-6 w-full max-w-sm">
        <div className="text-center mb-6">
          <h3 className="text-xl font-semibold mb-2">Your Wallet</h3>
          <div className="bg-gray-100 p-4 rounded-lg">
            <QrCode className="mx-auto mb-2 text-gray-600" size={48} />
            <p className="text-xs text-gray-600 mb-2">Wallet Address</p>
            <p className="font-mono text-sm">{user?.walletAddress}</p>
            <button
              onClick={() => copyToClipboard(user?.walletAddress)}
              className="mt-2 flex items-center justify-center mx-auto text-blue-600 text-sm"
            >
              <Copy size={16} />
              <span className="ml-1">Copy</span>
            </button>
          </div>
        </div>
        <div className="space-y-3">
          <div className="flex justify-between">
            <span className="text-gray-600">Balance</span>
            <span className="font-semibold">${user?.walletBalance?.toFixed(2)}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Total Invested</span>
            <span className="font-semibold">${user?.totalInvested?.toLocaleString()}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Total Earnings</span>
            <span className="font-semibold text-green-600">${user?.totalEarnings}</span>
          </div>
        </div>
        <button
          onClick={() => setShowWalletModal(false)}
          className="w-full mt-6 bg-blue-600 text-white py-3 rounded-lg font-semibold"
        >
          Close
        </button>
      </div>
    </div>
  );

  // Share Modal
  const ShareModal = () => (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl p-6 w-full max-w-sm">
        <div className="text-center mb-6">
          <Share2 className="mx-auto mb-4 text-blue-600" size={48} />
          <h3 className="text-xl font-semibold mb-2">Refer Friends</h3>
          <p className="text-gray-600">Share your referral code and earn 5% of their first investment</p>
        </div>
        <div className="bg-blue-50 p-4 rounded-lg mb-4">
          <p className="text-sm text-gray-600 mb-2">Your Referral Code</p>
          <div className="flex items-center justify-between">
            <span className="font-bold text-lg">{user?.referralCode}</span>
            <button
              onClick={() => copyToClipboard(user?.referralCode)}
              className="text-blue-600"
            >
              <Copy size={20} />
            </button>
          </div>
        </div>
        <div className="text-center mb-4">
          <p className="text-sm text-gray-600">Total Referral Earnings</p>
          <p className="text-2xl font-bold text-green-600">${user?.referralEarnings}</p>
        </div>
        <button
          onClick={() => setShowShareModal(false)}
          className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold"
        >
          Close
        </button>
      </div>
    </div>
  );

  // Home Page
  const HomePage = () => (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Building2 className="text-blue-600" size={24} />
            <span className="font-bold text-xl text-gray-800">AssetFraction</span>
          </div>
          {!user ? (
            <button
              onClick={() => setCurrentPage('onboard')}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium"
            >
              Get Started
            </button>
          ) : (
            <div className="flex items-center space-x-2">
              <span className="text-sm text-gray-600">Welcome, {user.name}</span>
              <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                <User className="text-white" size={16} />
              </div>
            </div>
          )}
        </div>
      </header>

      {/* Hero Section */}
      <div className="px-4 py-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Own Real Estate & Art<br />
            <span className="text-blue-600">From $5</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Invest in fractional ownership of premium African real estate and art. 
            Built on Hedera for instant, transparent, and secure transactions.
          </p>
        </div>

        {/* Feature Cards */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          {[
            {
              icon: DollarSign,
              title: "Start from $5",
              description: "Minimum investment of just $5 makes wealth building accessible to everyone"
            },
            {
              icon: Zap,
              title: "Instant Liquidity",
              description: "Trade your fractions anytime with built-in DeFi integration"
            },
            {
              icon: Shield,
              title: "Fully Transparent",
              description: "All transactions verified on Hedera blockchain with complete audit trail"
            }
          ].map(({ icon: Icon, title, description }, index) => (
            <div key={index} className="bg-white p-6 rounded-xl shadow-lg">
              <Icon className="text-blue-600 mb-4" size={32} />
              <h3 className="font-semibold text-lg mb-2">{title}</h3>
              <p className="text-gray-600">{description}</p>
            </div>
          ))}
        </div>

        {/* CTA */}
        <div className="text-center">
          <button
            onClick={() => user ? setCurrentPage('marketplace') : setCurrentPage('onboard')}
            className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-8 py-4 rounded-xl text-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-200"
          >
            {user ? 'Explore Assets' : 'Start Investing Today'}
          </button>
        </div>
      </div>
    </div>
  );

  // Onboarding Page
  const OnboardPage = () => (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-md mx-auto bg-white rounded-xl shadow-lg p-6">
        <div className="text-center mb-6">
          <Building2 className="mx-auto text-blue-600 mb-4" size={48} />
          <h2 className="text-2xl font-bold text-gray-900">Join AssetFraction</h2>
          <p className="text-gray-600 mt-2">Complete KYC to start investing</p>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Full Name
            </label>
            <input
              type="text"
              required
              value={kycData.name}
              onChange={(e) => setKycData({ ...kycData, name: e.target.value })}
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Enter your full name"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Phone Number
            </label>
            <input
              type="tel"
              required
              value={kycData.phone}
              onChange={(e) => setKycData({ ...kycData, phone: e.target.value })}
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="+234 XXX XXX XXXX"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Identity Document
            </label>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
              <Upload className="mx-auto text-gray-400 mb-2" size={32} />
              <p className="text-sm text-gray-600">Upload your ID or passport</p>
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

          <button
            onClick={handleKycSubmit}
            className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
          >
            Submit KYC & Create Wallet
          </button>
        </div>

        <div className="mt-6 text-center">
          <button
            onClick={handleLogin}
            className="text-blue-600 hover:text-blue-700 text-sm"
          >
            Already have an account? Sign in
          </button>
        </div>
      </div>
    </div>
  );

  // Marketplace Page
  const MarketplacePage = () => (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm p-4">
        <h1 className="text-2xl font-bold text-gray-900">Asset Marketplace</h1>
        <p className="text-gray-600">Discover fractional investment opportunities</p>
      </header>

      {/* Search and Filters */}
      <div className="p-4 bg-white border-b">
        <div className="flex space-x-4 mb-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-3 text-gray-400" size={20} />
            <input
              type="text"
              placeholder="Search assets..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Types</option>
            <option value="real-estate">Real Estate</option>
            <option value="art">Art</option>
          </select>
        </div>
      </div>

      {/* Asset Grid */}
      <div className="p-4 space-y-4">
        {filteredAssets.map((asset) => (
          <div
            key={asset.id}
            className="bg-white rounded-xl shadow-lg overflow-hidden cursor-pointer hover:shadow-xl transition-shadow"
            onClick={() => {
              setSelectedAsset(asset);
              setCurrentPage('asset-detail');
            }}
          >
            <img
              src={asset.image}
              alt={asset.title}
              className="w-full h-48 object-cover"
            />
            <div className="p-4">
              <div className="flex items-start justify-between mb-2">
                <h3 className="font-semibold text-lg text-gray-900">{asset.title}</h3>
                {asset.verified && (
                  <Check className="text-green-500 flex-shrink-0" size={20} />
                )}
              </div>
              
              <div className="flex items-center text-gray-600 mb-3">
                <MapPin size={16} />
                <span className="ml-1 text-sm">{asset.location}</span>
              </div>

              <div className="grid grid-cols-2 gap-4 mb-4">
                <div>
                  <p className="text-sm text-gray-500">Token Price</p>
                  <p className="font-semibold">${asset.tokenPrice}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Monthly Return</p>
                  <p className="font-semibold text-green-600">{asset.monthlyReturn}%</p>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4 text-sm text-gray-600">
                  <span className="flex items-center">
                    <Users size={16} />
                    <span className="ml-1">{asset.investors}</span>
                  </span>
                  <span>{((asset.totalTokens - asset.tokensAvailable) / asset.totalTokens * 100).toFixed(1)}% funded</span>
                </div>
                <ChevronRight className="text-gray-400" size={20} />
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  // Asset Detail Page
  const AssetDetailPage = () => {
    if (!selectedAsset) return null;

    return (
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow-sm p-4 flex items-center">
          <button
            onClick={() => setCurrentPage('marketplace')}
            className="mr-4 p-2 hover:bg-gray-100 rounded-lg"
          >
            ←
          </button>
          <h1 className="text-xl font-bold text-gray-900">Asset Details</h1>
        </header>

        <div className="p-4">
          <img
            src={selectedAsset.image}
            alt={selectedAsset.title}
            className="w-full h-64 object-cover rounded-xl mb-4"
          />

          <div className="bg-white rounded-xl p-6 mb-4">
            <div className="flex items-start justify-between mb-4">
              <h2 className="text-2xl font-bold text-gray-900">{selectedAsset.title}</h2>
              {selectedAsset.verified && (
                <div className="flex items-center text-green-600">
                  <Check size={20} />
                  <span className="ml-1 text-sm">Verified</span>
                </div>
              )}
            </div>

            <div className="flex items-center text-gray-600 mb-6">
              <MapPin size={20} />
              <span className="ml-2">{selectedAsset.location}</span>
            </div>

            <div className="grid grid-cols-2 gap-4 mb-6">
              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <p className="text-sm text-gray-600">Total Value</p>
                <p className="text-2xl font-bold text-blue-600">${selectedAsset.totalValue.toLocaleString()}</p>
              </div>
              <div className="text-center p-4 bg-green-50 rounded-lg">
                <p className="text-sm text-gray-600">Monthly Return</p>
                <p className="text-2xl font-bold text-green-600">{selectedAsset.monthlyReturn}%</p>
              </div>
            </div>

            <div className="space-y-4 mb-6">
              <div className="flex justify-between">
                <span className="text-gray-600">Token Price</span>
                <span className="font-semibold">${selectedAsset.tokenPrice}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Available Tokens</span>
                <span className="font-semibold">{selectedAsset.tokensAvailable.toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Total Investors</span>
                <span className="font-semibold">{selectedAsset.investors}</span>
              </div>
            </div>

            {user && (
              <div className="border-t pt-6">
                <h3 className="font-semibold text-lg mb-4">Invest Now</h3>
                <div className="flex space-x-4">
                  <input
                    type="number"
                    placeholder="Investment amount ($)"
                    value={investmentAmount}
                    onChange={(e) => setInvestmentAmount(e.target.value)}
                    className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                    min="5"
                  />
                  <button
                    onClick={() => handleInvestment(selectedAsset.id, parseFloat(investmentAmount))}
                    disabled={!investmentAmount || parseFloat(investmentAmount) < 5}
                    className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
                  >
                    Invest
                  </button>
                </div>
                <p className="text-sm text-gray-600 mt-2">
                  Minimum investment: $5 • You'll get {investmentAmount ? Math.floor(parseFloat(investmentAmount) / selectedAsset.tokenPrice) : 0} tokens
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  // Portfolio Page
  const PortfolioPage = () => {
    if (!user) {
      return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
          <div className="text-center">
            <Wallet className="mx-auto text-gray-400 mb-4" size={64} />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Connect Your Wallet</h2>
            <p className="text-gray-600 mb-6">Sign in to view your portfolio</p>
            <button
              onClick={() => setCurrentPage('onboard')}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold"
            >
              Get Started
            </button>
          </div>
        </div>
      );
    }

    return (
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow-sm p-4">
          <h1 className="text-2xl font-bold text-gray-900">My Portfolio</h1>
          <p className="text-gray-600">Track your investments and earnings</p>
        </header>

        <div className="p-4 space-y-4">
          {/* Summary Cards */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-white p-4 rounded-xl shadow-lg">
              <p className="text-sm text-gray-600">Total Invested</p>
              <p className="text-2xl font-bold text-gray-900">${user.totalInvested.toLocaleString()}</p>
            </div>
            <div className="bg-white p-4 rounded-xl shadow-lg">
              <p className="text-sm text-gray-600">Total Earnings</p>
              <p className="text-2xl font-bold text-green-600">${user.totalEarnings}</p>
            </div>
          </div>

          <div className="bg-white p-4 rounded-xl shadow-lg">
            <p className="text-sm text-gray-600">Wallet Balance</p>
            <p className="text-2xl font-bold text-blue-600">${user.walletBalance.toFixed(2)}</p>
          </div>

          {/* Asset Holdings */}
          <div className="bg-white rounded-xl shadow-lg p-4">
            <h3 className="font-semibold text-lg mb-4">My Assets</h3>
            <div className="space-y-4">
              {user.assets.map((holding) => {
                const asset = mockAssets.find(a => a.id === holding.assetId);
                return (
                  <div key={holding.assetId} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-medium">{asset?.title}</h4>
                      <span className="text-sm text-gray-600">{holding.tokens} tokens</span>
                    </div>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <p className="text-gray-600">Value</p>
                        <p className="font-semibold">${holding.value}</p>
                      </div>
                      <div>
                        <p className="text-gray-600">Monthly Income</p>
                        <p className="font-semibold text-green-600">${holding.monthlyIncome}</p>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    );
  };

  // History Page
  const HistoryPage = () => (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm p-4">
        <h1 className="text-2xl font-bold text-gray-900">Transaction History</h1>
        <p className="text-gray-600">All your investment activities</p>
      </header>

      <div className="p-4">
        <div className="bg-white rounded-xl shadow-lg">
          {mockTransactions.map((tx) => (
            <div key={tx.id} className="p-4 border-b border-gray-200 last:border-b-0">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className={`p-2 rounded-lg ${
                    tx.type === 'buy' ? 'bg-blue-100' : 'bg-green-100'
                  }`}>
                    {tx.type === 'buy' ? (
                      <ArrowUp className={`${tx.type === 'buy' ? 'text-blue-600' : 'text-green-600'}`} size={16} />
                    ) : (
                      <ArrowDown className="text-green-600" size={16} />
                    )}
                  </div>
                  <div>
                    <p className="font-medium">{tx.type === 'buy' ? 'Investment' : 'Income'}</p>
                    <p className="text-sm text-gray-600">{tx.asset}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className={`font-semibold ${
                    tx.type === 'buy' ? 'text-red-600' : 'text-green-600'
                  }`}>
                    {tx.type === 'buy' ? '-' : '+'}${tx.amount}
                  </p>
                  <p className="text-sm text-gray-600">{tx.date}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  // Main render logic
  const renderPage = () => {
    switch (currentPage) {
      case 'home':
        return <HomePage />;
      case 'onboard':
        return <OnboardPage />;
      case 'marketplace':
        return <MarketplacePage />;
      case 'asset-detail':
        return <AssetDetailPage />;
      case 'portfolio':
        return <PortfolioPage />;
      case 'history':
        return <HistoryPage />;
      default:
        return <HomePage />;
    }
  };

  return (
    <div className="max-w-md mx-auto bg-white min-h-screen relative">
      {renderPage()}
      {currentPage !== 'home' && currentPage !== 'onboard' && currentPage !== 'asset-detail' && (
        <Navigation />
      )}
    </div>
  );
}

export default App;