import React, { useState } from 'react'
import './Header.css'

function Header() {
  const [menuOpen, setMenuOpen] = useState(false)

  return (
    <header className="header">
      <div className="container">
        <nav className="nav">
          <div className="logo">
            <span className="logo-text">NewsAPI AI</span>
          </div>

          <button
            className="menu-toggle"
            onClick={() => setMenuOpen(!menuOpen)}
            aria-label="Toggle menu"
          >
            <span></span>
            <span></span>
            <span></span>
          </button>

          <ul className={`nav-links ${menuOpen ? 'open' : ''}`}>
            <li><a href="#get-started">Get Started</a></li>
            <li><a href="#documentation">Documentation</a></li>
            <li><a href="#pricing">Pricing</a></li>
            <li><a href="#login" className="nav-link-secondary">Login</a></li>
            <li><a href="#api-key" className="nav-cta">Get API Key</a></li>
          </ul>
        </nav>
      </div>
    </header>
  )
}

export default Header
