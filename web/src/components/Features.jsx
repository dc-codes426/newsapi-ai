import React from 'react'
import './Features.css'

const features = [
  {
    id: 1,
    icon: '🌍',
    title: 'Worldwide Coverage',
    description: 'Access news from over 150,000 sources across 14 languages. Get breaking news and articles from every corner of the globe.'
  },
  {
    id: 2,
    icon: '⚡',
    title: 'Simple REST API',
    description: 'Easy to integrate REST API with JSON responses. Get started in minutes with comprehensive documentation and examples.'
  },
  {
    id: 3,
    icon: '🎯',
    title: 'Powerful Filtering',
    description: 'Filter by keywords, dates, sources, languages, and more. Find exactly what you need with advanced search capabilities.'
  },
  {
    id: 4,
    icon: '🤖',
    title: 'AI-Powered Search',
    description: 'Leverage AI to find the most relevant articles and understand sentiment, topics, and trends in real-time.'
  },
  {
    id: 5,
    icon: '🔒',
    title: 'Secure & Reliable',
    description: 'Enterprise-grade security with 99.9% uptime SLA. Your data and API keys are always protected.'
  },
  {
    id: 6,
    icon: '📊',
    title: 'Real-time Analytics',
    description: 'Track your API usage, monitor performance, and get insights with our comprehensive analytics dashboard.'
  }
]

function Features() {
  return (
    <section className="features">
      <div className="container">
        <h2 className="section-title">Why choose NewsAPI AI?</h2>
        <p className="section-subtitle">
          Everything you need to build powerful news applications
        </p>

        <div className="features-grid">
          {features.map(feature => (
            <div key={feature.id} className="feature-card">
              <div className="feature-icon">{feature.icon}</div>
              <h3 className="feature-title">{feature.title}</h3>
              <p className="feature-description">{feature.description}</p>
            </div>
          ))}
        </div>

        <div className="cta-section">
          <h3 className="cta-title">Ready to get started?</h3>
          <p className="cta-description">
            Start building with 100 free requests per day. No credit card required.
          </p>
          <a href="#api-key" className="btn btn-primary-large">
            Get Your Free API Key
          </a>
        </div>
      </div>
    </section>
  )
}

export default Features
