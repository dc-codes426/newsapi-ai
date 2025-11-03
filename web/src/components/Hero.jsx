import React from 'react'
import './Hero.css'

function Hero() {
  return (
    <section className="hero">
      <div className="container">
        <div className="hero-content">
          <h1 className="hero-title">Search worldwide news with AI</h1>
          <p className="hero-subtitle">
            Locate articles and breaking news headlines from news sources and blogs
            across the web with our AI-powered news API
          </p>
          <div className="hero-cta">
            <a href="#api-key" className="btn btn-primary">Get API Key</a>
            <a href="#documentation" className="btn btn-secondary">View Documentation</a>
          </div>
          <p className="hero-note">Get started with 100 free requests per day</p>
        </div>
      </div>
    </section>
  )
}

export default Hero
