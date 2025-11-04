import React from 'react'
import './Hero.css'

function Hero() {
  return (
    <section className="hero">
      <div className="container">
        <div className="hero-content">
          <div className="hero-badge">AI-Powered News Intelligence</div>
          <h1 className="hero-title">Keep Your AI Agents Updated with Real-Time News</h1>
          <p className="hero-subtitle">
            The first news API built for AI agents. Search semantically, understand context,
            and retrieve relevant news using natural language. Perfect for RAG systems,
            chatbots, and intelligent automation.
          </p>
          <div className="hero-features-quick">
            <div className="hero-feature-item">
              <span className="hero-feature-icon">🧠</span>
              <span>Semantic Search</span>
            </div>
            <div className="hero-feature-item">
              <span className="hero-feature-icon">🤖</span>
              <span>AI Agent Ready</span>
            </div>
            <div className="hero-feature-item">
              <span className="hero-feature-icon">⚡</span>
              <span>Real-Time Updates</span>
            </div>
          </div>
          <div className="hero-cta">
            <a href="/documentation" className="btn btn-primary">View Documentation</a>
            <a href="#get-started" className="btn btn-secondary">See Examples</a>
          </div>
          <p className="hero-note">100% Free • Optional API Keys • Use Ours or Bring Your Own</p>
        </div>
      </div>
    </section>
  )
}

export default Hero
