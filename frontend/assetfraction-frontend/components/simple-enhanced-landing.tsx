"use client"

import React from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  Sparkles, TrendingUp, Shield, Zap, Globe, Users, 
  ArrowRight, Play, Star, Building2, BarChart3,
  Wallet, PieChart, Twitter, Github, Linkedin,
  Mail, MapPin, Phone, ExternalLink
} from 'lucide-react'

interface SimpleEnhancedLandingProps {
  onEnterApp: () => void
}

export default function SimpleEnhancedLanding({ onEnterApp }: SimpleEnhancedLandingProps) {
  const stats = [
    { label: 'Total Value Locked', value: '$12.5M', change: '+23%', icon: TrendingUp },
    { label: 'Active Investors', value: '2,847', change: '+156', icon: Users },
    { label: 'Assets Listed', value: '156', change: '+12', icon: Building2 },
    { label: 'Avg Returns', value: '18.7%', change: '+2.3%', icon: BarChart3 }
  ]

  const features = [
    {
      icon: Shield,
      title: 'Blockchain Security',
      description: 'Built on Hedera Hashgraph for enterprise-grade security',
      color: 'from-blue-500 to-cyan-500'
    },
    {
      icon: Zap,
      title: 'Instant Transactions',
      description: 'Lightning-fast transactions with minimal fees',
      color: 'from-purple-500 to-pink-500'
    },
    {
      icon: Globe,
      title: 'Global Access',
      description: 'Invest in premium African assets from anywhere',
      color: 'from-green-500 to-emerald-500'
    },
    {
      icon: PieChart,
      title: 'Fractional Ownership',
      description: 'Own fractions of high-value assets starting from $5',
      color: 'from-orange-500 to-red-500'
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50 dark:from-gray-900 dark:via-blue-900/20 dark:to-purple-900/20">
      {/* Hero Section */}
      <section className="relative overflow-hidden particle-bg">
        <div className="container mx-auto px-6 py-20">
          <div className="text-center">
            <div className="mb-8">
              <Badge className="mb-4 bg-gradient-to-r from-purple-500 to-blue-500 text-white px-4 py-2">
                <Sparkles className="w-4 h-4 mr-2" />
                Powered by Hedera Hashgraph
              </Badge>
              <h1 className="text-5xl md:text-7xl font-bold mb-6">
                <span className="gradient-text">Fractional Ownership</span>
                <br />
                <span className="text-gray-800 dark:text-white">Redefined</span>
              </h1>
              <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto mb-8">
                Invest in premium African real estate and art through blockchain-powered fractional ownership. 
                Start building your diversified portfolio today with as little as $5.
              </p>
            </div>

            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
              <Button 
                size="lg" 
                onClick={onEnterApp}
                className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white px-8 py-4 text-lg btn-glow"
              >
                Start Investing
                <ArrowRight className="ml-2 w-5 h-5" />
              </Button>
              <Button 
                size="lg" 
                variant="outline" 
                className="border-2 border-purple-200 hover:bg-purple-50 px-8 py-4 text-lg"
              >
                <Play className="mr-2 w-5 h-5" />
                Watch Demo
              </Button>
            </div>

            {/* Live Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
              {stats.map((stat, index) => (
                <div
                  key={stat.label}
                  className="glass-card p-6 text-center card-hover"
                >
                  <stat.icon className="w-8 h-8 mx-auto mb-2 text-purple-600" />
                  <div className="text-2xl font-bold text-gray-800 dark:text-white">
                    {stat.value}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-300">
                    {stat.label}
                  </div>
                  <div className="text-sm text-green-600 font-medium">
                    {stat.change}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white/50 dark:bg-gray-800/50">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4 gradient-text">
              Why Choose AssetFraction?
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
              Experience the future of investment with cutting-edge technology and unparalleled opportunities.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div
                key={feature.title}
                className="glass-card p-6 text-center card-hover"
              >
                <div className={`w-16 h-16 mx-auto mb-4 rounded-2xl bg-gradient-to-br ${feature.color} flex items-center justify-center float-animation`}>
                  <feature.icon className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-xl font-bold mb-2 text-gray-800 dark:text-white">
                  {feature.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-300">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-purple-600 to-blue-600">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-4xl font-bold text-white mb-4">
            Ready to Start Your Investment Journey?
          </h2>
          <p className="text-xl text-purple-100 mb-8 max-w-2xl mx-auto">
            Join the revolution in fractional ownership and start building your diversified portfolio today.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button 
              size="lg" 
              onClick={onEnterApp}
              className="bg-white text-purple-600 hover:bg-gray-100 px-8 py-4 text-lg btn-glow"
            >
              <Wallet className="mr-2 w-5 h-5" />
              Enter App
            </Button>
            <Button 
              size="lg" 
              variant="outline" 
              className="border-2 border-white text-white hover:bg-white hover:text-purple-600 px-8 py-4 text-lg"
            >
              Learn More
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white">
        <div className="container mx-auto px-6 py-16">
          <div className="grid md:grid-cols-4 gap-8">
            {/* Company Info */}
            <div className="md:col-span-1">
              <div className="flex items-center mb-4">
                <div className="w-10 h-10 bg-gradient-to-r from-purple-600 to-blue-600 rounded-xl flex items-center justify-center mr-3">
                  <Building2 className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-2xl font-bold gradient-text">AssetFraction</h3>
              </div>
              <p className="text-gray-400 mb-6">
                Democratizing access to premium African real estate and art through blockchain-powered fractional ownership.
              </p>
              <div className="flex space-x-4">
                <a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">
                  <Twitter className="w-5 h-5" />
                </a>
                <a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">
                  <Github className="w-5 h-5" />
                </a>
                <a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">
                  <Linkedin className="w-5 h-5" />
                </a>
                <a href="#" className="text-gray-400 hover:text-purple-400 transition-colors">
                  <Mail className="w-5 h-5" />
                </a>
              </div>
            </div>

            {/* Platform */}
            <div>
              <h4 className="text-lg font-semibold mb-4">Platform</h4>
              <ul className="space-y-2">
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Browse Assets</a></li>
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Portfolio</a></li>
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Marketplace</a></li>
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Analytics</a></li>
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Wallet</a></li>
              </ul>
            </div>

            {/* Resources */}
            <div>
              <h4 className="text-lg font-semibold mb-4">Resources</h4>
              <ul className="space-y-2">
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Documentation</a></li>
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">API Reference</a></li>
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Whitepaper</a></li>
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Blog</a></li>
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Help Center</a></li>
              </ul>
            </div>

            {/* Contact */}
            <div>
              <h4 className="text-lg font-semibold mb-4">Contact</h4>
              <div className="space-y-3">
                <div className="flex items-center text-gray-400">
                  <Mail className="w-4 h-4 mr-2" />
                  <span>hello@assetfraction.com</span>
                </div>
                <div className="flex items-center text-gray-400">
                  <Phone className="w-4 h-4 mr-2" />
                  <span>+234 (0) 123 456 7890</span>
                </div>
                <div className="flex items-start text-gray-400">
                  <MapPin className="w-4 h-4 mr-2 mt-1" />
                  <span>Lagos, Nigeria<br />Nairobi, Kenya</span>
                </div>
              </div>
              
              {/* Newsletter Signup */}
              <div className="mt-6">
                <h5 className="text-sm font-semibold mb-2">Stay Updated</h5>
                <div className="flex">
                  <input 
                    type="email" 
                    placeholder="Enter your email"
                    className="flex-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-l-lg text-sm focus:outline-none focus:border-purple-500"
                  />
                  <button className="px-4 py-2 bg-gradient-to-r from-purple-600 to-blue-600 rounded-r-lg hover:from-purple-700 hover:to-blue-700 transition-colors">
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Bottom Section */}
          <div className="border-t border-gray-800 mt-12 pt-8">
            <div className="flex flex-col md:flex-row justify-between items-center">
              <div className="text-gray-400 text-sm mb-4 md:mb-0">
                © 2024 AssetFraction. All rights reserved. Built on Hedera Hashgraph.
              </div>
              <div className="flex space-x-6 text-sm">
                <a href="#" className="text-gray-400 hover:text-white transition-colors">Privacy Policy</a>
                <a href="#" className="text-gray-400 hover:text-white transition-colors">Terms of Service</a>
                <a href="#" className="text-gray-400 hover:text-white transition-colors">Cookie Policy</a>
                <a href="#" className="text-gray-400 hover:text-white transition-colors flex items-center">
                  Hedera Network
                  <ExternalLink className="w-3 h-3 ml-1" />
                </a>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
