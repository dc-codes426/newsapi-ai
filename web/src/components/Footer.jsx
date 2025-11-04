import React from 'react'
import { Link } from 'react-router-dom'
import './Footer.css'

function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-section">
            <h4 className="footer-title">NewsAPI AI</h4>
            <p className="footer-description">
              AI-powered news aggregation API for developers. Search worldwide news with ease.
            </p>
          </div>

          <div className="footer-section">
            <h4 className="footer-heading">Product</h4>
            <ul className="footer-links">
              <li><Link to="/documentation">Documentation</Link></li>
              <li><a href="https://github.com/dc-codes426/newsapi-ai" target="_blank" rel="noopener noreferrer">GitHub</a></li>
              <li><Link to="/examples">API Examples</Link></li>
            </ul>
          </div>

          <div className="footer-section">
            <h4 className="footer-heading">Resources</h4>
            <ul className="footer-links">
              <li><a href="https://github.com/dc-codes426/newsapi-ai/discussions" target="_blank" rel="noopener noreferrer">Community</a></li>
              <li><a href="https://github.com/dc-codes426/newsapi-ai/issues" target="_blank" rel="noopener noreferrer">Support</a></li>
              <li><Link to="/about">About</Link></li>
            </ul>
          </div>

          <div className="footer-section">
            <h4 className="footer-heading">Connect</h4>
            <ul className="footer-links">
              <li><Link to="/contact">Contact</Link></li>
              <li><a href="https://ko-fi.com/davidconnor" target="_blank" rel="noopener noreferrer">Support Us ☕</a></li>
              <li><a href="#privacy">Privacy Policy</a></li>
            </ul>
          </div>
        </div>

        <div className="footer-bottom">
          <p>&copy; {currentYear} NewsAPI AI. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
