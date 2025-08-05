"use client"

import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Sparkles, TrendingUp, Shield, Zap, Globe, Users, 
  ArrowRight, Play, Star, CheckCircle, BarChart3,
  Wallet, Building2, PieChart, Target, Award
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

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
    description: 'Built on Hedera Hashgraph for enterprise-grade security and transparency',
    color: 'from-blue-500 to-cyan-500'
  },
  {
    icon: Zap,
    title: 'Instant Transactions',
    description: 'Lightning-fast transactions with minimal fees powered by Hedera',
    color: 'from-purple-500 to-pink-500'
  },
  {
    icon: Globe,
    title: 'Global Access',
    description: 'Invest in premium African assets from anywhere in the world',
    color: 'from-green-500 to-emerald-500'
  },
  {
    icon: PieChart,
    title: 'Fractional Ownership',
    description: 'Own fractions of high-value assets starting from just $5',
    color: 'from-orange-500 to-red-500'
  }
]

const testimonials = [
  {
    name: 'Amara Okafor',
    role: 'Real Estate Investor',
    content: 'AssetFraction has revolutionized how I invest in African real estate. The platform is intuitive and the returns are impressive.',
    avatar: '/placeholder-avatar-1.jpg',
    rating: 5
  },
  {
    name: 'Kwame Asante',
    role: 'Art Collector',
    content: 'Finally, a platform that makes art investment accessible. I love the transparency and the cultural impact.',
    avatar: '/placeholder-avatar-2.jpg',
    rating: 5
  },
  {
    name: 'Fatima Al-Rashid',
    role: 'Tech Entrepreneur',
    content: 'The technology behind AssetFraction is impressive. Hedera integration makes everything seamless and secure.',
    avatar: '/placeholder-avatar-3.jpg',
    rating: 5
  }
]

export default function EnhancedLanding() {
  const [currentStat, setCurrentStat] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStat((prev) => (prev + 1) % stats.length)
    }, 3000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50 dark:from-gray-900 dark:via-blue-900/20 dark:to-purple-900/20">
      {/* Hero Section */}
      <section className="relative overflow-hidden particle-bg">
        <div className="container mx-auto px-6 py-20">
          <div className="text-center">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="mb-8"
            >
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
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="flex flex-col sm:flex-row gap-4 justify-center mb-12"
            >
              <Button 
                size="lg" 
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
            </motion.div>

            {/* Live Stats */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto"
            >
              {stats.map((stat, index) => (
                <motion.div
                  key={stat.label}
                  className={`glass-card p-6 text-center ${
                    currentStat === index ? 'pulse-glow' : ''
                  }`}
                  whileHover={{ scale: 1.05 }}
                  transition={{ type: "spring", stiffness: 300 }}
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
                </motion.div>
              ))}
            </motion.div>
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
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
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
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4 gradient-text">
              Trusted by Investors Worldwide
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300">
              Join thousands of satisfied investors who are building wealth through AssetFraction
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <motion.div
                key={testimonial.name}
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="glass-card p-6 card-hover"
              >
                <div className="flex items-center mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="w-5 h-5 text-yellow-400 fill-current" />
                  ))}
                </div>
                <p className="text-gray-600 dark:text-gray-300 mb-6 italic">
                  "{testimonial.content}"
                </p>
                <div className="flex items-center">
                  <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full flex items-center justify-center text-white font-bold mr-4">
                    {testimonial.name.charAt(0)}
                  </div>
                  <div>
                    <div className="font-bold text-gray-800 dark:text-white">
                      {testimonial.name}
                    </div>
                    <div className="text-sm text-gray-600 dark:text-gray-300">
                      {testimonial.role}
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-purple-600 to-blue-600">
        <div className="container mx-auto px-6 text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl font-bold text-white mb-4">
              Ready to Start Your Investment Journey?
            </h2>
            <p className="text-xl text-purple-100 mb-8 max-w-2xl mx-auto">
              Join the revolution in fractional ownership and start building your diversified portfolio today.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button 
                size="lg" 
                className="bg-white text-purple-600 hover:bg-gray-100 px-8 py-4 text-lg btn-glow"
              >
                <Wallet className="mr-2 w-5 h-5" />
                Connect Wallet
              </Button>
              <Button 
                size="lg" 
                variant="outline" 
                className="border-2 border-white text-white hover:bg-white hover:text-purple-600 px-8 py-4 text-lg"
              >
                Learn More
              </Button>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  )
}
