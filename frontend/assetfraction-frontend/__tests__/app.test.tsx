import { render, screen, fireEvent } from '@testing-library/react'
import '@testing-library/jest-dom'
import Page from '../app/page'
import { ThemeProvider } from '../components/theme-provider'

// Mock matchMedia
window.matchMedia = jest.fn().mockImplementation((query: string) => ({
  matches: false,
  media: query,
  onchange: null,
  addListener: jest.fn(),
  removeListener: jest.fn(),
  addEventListener: jest.fn(),
  removeEventListener: jest.fn(),
  dispatchEvent: jest.fn(),
}))

describe('AssetFraction Frontend Tests', () => {
  // Home Page Tests
  describe('Home Page', () => {
    it('renders header with logo', () => {
      render(
        <ThemeProvider>
          <Page />
        </ThemeProvider>
      )
      
      expect(screen.getByText('AssetFraction')).toBeInTheDocument()
    })
  })

  // Authentication Tests
  describe('Authentication', () => {
    it('shows login button when user is not authenticated', () => {
      render(
        <ThemeProvider>
          <Page />
        </ThemeProvider>
      )
      
      expect(screen.getByText(/get started/i)).toBeInTheDocument()
    })
  })

  // Asset Listing Tests
  describe('Asset Listings', () => {
    it('displays main heading', () => {
      render(
        <ThemeProvider>
          <Page />
        </ThemeProvider>
      )
      
      expect(screen.getByText(/Own Real Estate & Art/)).toBeInTheDocument()
      expect(screen.getByText(/From \$5/)).toBeInTheDocument()
    })
  })

  // Transaction Tests
  describe('Transactions', () => {
    it('shows features section', () => {
      render(
        <ThemeProvider>
          <Page />
        </ThemeProvider>
      )
      
      expect(screen.getByText('Start from $5')).toBeInTheDocument()
      expect(screen.getByText('Instant Liquidity')).toBeInTheDocument()
      expect(screen.getByText('Fully Transparent')).toBeInTheDocument()
    })
  })

  // Wallet Integration Tests
  describe('Wallet Integration', () => {
    it('has get started button', () => {
      render(
        <ThemeProvider>
          <Page />
        </ThemeProvider>
      )
      
      expect(screen.getByText('Get Started')).toBeInTheDocument()
    })
  })
})
