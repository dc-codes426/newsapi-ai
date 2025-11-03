import React from 'react'
import './Features.css'

const features = [
  {
    id: 1,
    icon: '🧠',
    title: 'Semantic Understanding',
    description: 'Search by meaning, not just keywords. Our AI understands context and intent, delivering truly relevant results for your agents.'
  },
  {
    id: 2,
    icon: '🤖',
    title: 'RAG-Optimized',
    description: 'Pre-processed and structured for Retrieval-Augmented Generation. Perfect for ChatGPT, Claude, and custom LLM applications.'
  },
  {
    id: 3,
    icon: '💬',
    title: 'Natural Language Queries',
    description: 'Ask questions in plain English. No complex query syntax - just conversational requests that your AI agents can easily generate.'
  },
  {
    id: 4,
    icon: '⚡',
    title: 'Real-Time Updates',
    description: 'Keep your AI agents informed with breaking news as it happens. Automatic updates ensure your agents always have current information.'
  },
  {
    id: 5,
    icon: '🎯',
    title: 'Topic Monitoring',
    description: 'Track specific topics, companies, or trends. Get alerts and summaries tailored for your AI agent\'s specific knowledge needs.'
  },
  {
    id: 6,
    icon: '📊',
    title: 'Sentiment & Analysis',
    description: 'Built-in sentiment analysis, topic extraction, and relevance scoring. Give your AI agents the context they need to respond intelligently.'
  }
]

function Features() {
  return (
    <section className="features">
      <div className="container">
        <h2 className="section-title">Designed for AI Agents</h2>
        <p className="section-subtitle">
          Everything your AI agents need to stay informed and respond intelligently
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
          <h3 className="cta-title">Ready to empower your AI agents?</h3>
          <p className="cta-description">
            Start building intelligent news-aware applications today. 100% free. No authentication required.
          </p>
          <a href="/documentation" className="btn btn-primary-large">
            Start Building Now
          </a>
        </div>
      </div>
    </section>
  )
}

export default Features
