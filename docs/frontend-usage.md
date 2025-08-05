# 📘 AssetFraction Frontend - Usage Guide & Examples

## 🎯 Component Examples

### Authentication

```tsx
// Using the Authentication Component
import { AuthProvider, useAuth } from '../components/auth-provider'

function MyComponent() {
  const { user, login, logout } = useAuth()
  
  return (
    <div>
      {user ? (
        <button onClick={logout}>Logout</button>
      ) : (
        <button onClick={login}>Connect Wallet</button>
      )}
    </div>
  )
}
```

### Asset Card

```tsx
// Displaying an Asset
import { AssetCard } from '../components/ui/asset-card'

const asset = {
  id: '1',
  name: 'Luxury Apartment Complex',
  location: 'Dubai Marina',
  price: 5000000,
  fractionPrice: 100,
  totalFractions: 5000,
  availableFractions: 3000,
  images: ['image1.jpg'],
  returns: '12%',
}

function AssetDisplay() {
  return <AssetCard asset={asset} />
}
```

### Transaction History

```tsx
// Implementing Transaction History
import { TransactionHistory } from '../components/transaction-history'

function PortfolioPage() {
  return (
    <TransactionHistory 
      filter={{
        startDate: new Date('2024-01-01'),
        endDate: new Date('2024-12-31'),
        type: 'all'
      }}
    />
  )
}
```

## 🎨 Theme Customization

### Colors

```tsx
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          // ... other shades
          900: '#0c4a6e',
        },
        // Add your custom colors
      }
    }
  }
}
```

### Typography

```tsx
// Using Custom Typography
<h1 className="text-4xl font-bold tracking-tight text-gray-900 dark:text-white">
  Welcome to AssetFraction
</h1>

<p className="text-base leading-7 text-gray-600 dark:text-gray-400">
  Start your real estate investment journey
</p>
```

## 📊 Charts & Data Visualization

```tsx
// Investment Performance Chart
import { LineChart } from '../components/ui/chart'

function PerformanceChart() {
  const data = [
    { date: '2024-01', value: 1000 },
    { date: '2024-02', value: 1200 },
    { date: '2024-03', value: 1150 },
    { date: '2024-04', value: 1400 },
  ]

  return (
    <LineChart
      data={data}
      xAxis="date"
      yAxis="value"
      title="Investment Performance"
    />
  )
}
```

## 🔐 Web3 Integration

```tsx
// Connecting to Web3 Wallet
import { useWeb3 } from '../hooks/use-web3'

function WalletConnection() {
  const { connect, disconnect, address, balance } = useWeb3()

  return (
    <div>
      {address ? (
        <div>
          <p>Connected: {address}</p>
          <p>Balance: {balance}</p>
          <button onClick={disconnect}>Disconnect</button>
        </div>
      ) : (
        <button onClick={connect}>Connect Wallet</button>
      )}
    </div>
  )
}
```

## 📱 Responsive Design

```tsx
// Responsive Component Example
function ResponsiveLayout() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div className="p-4 bg-white rounded-lg shadow">
        {/* Content */}
      </div>
      {/* More grid items */}
    </div>
  )
}
```

## 🎨 Component Props Reference

### AssetCard

| Prop | Type | Description |
|------|------|-------------|
| asset | Asset | Asset details object |
| onInvest | () => void | Investment callback |
| className | string | Additional CSS classes |

### TransactionHistory

| Prop | Type | Description |
|------|------|-------------|
| filter | Filter | Transaction filter options |
| pageSize | number | Items per page |
| onPageChange | (page: number) => void | Page change handler |

### Chart

| Prop | Type | Description |
|------|------|-------------|
| data | DataPoint[] | Chart data array |
| type | 'line' \| 'bar' \| 'pie' | Chart type |
| options | ChartOptions | Configuration options |

## 🔧 Configuration

### Environment Variables

```env
NEXT_PUBLIC_API_URL=your_api_url
NEXT_PUBLIC_WEB3_PROVIDER=your_web3_provider
NEXT_PUBLIC_CONTRACT_ADDRESS=your_contract_address
```

### Feature Flags

```typescript
// config/features.ts
export const FEATURES = {
  KYC_VERIFICATION: true,
  MULTI_WALLET: true,
  SECONDARY_MARKET: process.env.NEXT_PUBLIC_ENABLE_SECONDARY_MARKET === 'true',
}
```
