import React from 'react'
import './Contact.css'

function Contact() {
  return (
    <div className="contact-page">
      <section className="contact-hero">
        <div className="container">
          <h1 className="contact-title">Get in Touch</h1>
          <p className="contact-subtitle">
            Questions, feedback, or just want to say hi? We'd love to hear from you.
          </p>
        </div>
      </section>

      <section className="contact-content">
        <div className="container">
          <div className="contact-grid">
            {/* Left Column - Contact Methods */}
            <div className="contact-methods">
              <h2>Connect With Us</h2>
              <p className="intro-text">
                We're building NewsAPI AI in the open and welcome all feedback, questions, and collaboration.
              </p>

              <div className="contact-cards">
                <a
                  href="https://github.com/dc-codes426/newsapi-ai/discussions"
                  className="contact-card"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <div className="card-icon">💬</div>
                  <div className="card-content">
                    <h3>Community Discussions</h3>
                    <p>Join our GitHub Discussions for questions, feature requests, and general chat about NewsAPI AI.</p>
                    <span className="card-link">Join the conversation →</span>
                  </div>
                </a>

                <a
                  href="https://github.com/dc-codes426/newsapi-ai/issues"
                  className="contact-card"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <div className="card-icon">🐛</div>
                  <div className="card-content">
                    <h3>Report Issues</h3>
                    <p>Found a bug or have a feature request? Open an issue on GitHub and we'll get back to you.</p>
                    <span className="card-link">Open an issue →</span>
                  </div>
                </a>

                <a
                  href="https://github.com/dc-codes426/newsapi-ai"
                  className="contact-card"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <div className="card-icon">💻</div>
                  <div className="card-content">
                    <h3>Contribute on GitHub</h3>
                    <p>Check out our repositories, contribute code, improve documentation, or share your projects.</p>
                    <span className="card-link">View repositories →</span>
                  </div>
                </a>
              </div>
            </div>

            {/* Right Column - Support Section */}
            <div className="support-section">
              <div className="support-box">
                <h2>Support the Project</h2>
                <p>
                  NewsAPI AI is free and will always remain free. If you find it useful and want to support
                  the ongoing development, hosting costs, and maintenance, consider buying me a coffee!
                </p>

                <div className="kofi-section">
                  <div className="kofi-icon">☕</div>
                  <h3>Buy Me a Coffee</h3>
                  <p>
                    Your support helps keep the servers running, the AI models trained, and the API free
                    for everyone. Every contribution is deeply appreciated!
                  </p>
                  <a
                    href="https://ko-fi.com/davidconnor"
                    className="kofi-button"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <span className="kofi-button-icon">☕</span>
                    Support on Ko-fi
                  </a>
                </div>

                <div className="appreciation-note">
                  <p>
                    <strong>Thank you!</strong> Whether you use the API, report bugs, contribute code, or
                    support financially, you're helping make news intelligence accessible to everyone.
                  </p>
                </div>
              </div>

              <div className="info-box">
                <h3>💡 Quick Tip</h3>
                <p>
                  Before reaching out, check our <a href="/documentation">Documentation</a> and
                  <a href="https://github.com/dc-codes426/newsapi-ai/discussions" target="_blank" rel="noopener noreferrer"> GitHub Discussions</a> -
                  your question might already be answered!
                </p>
              </div>

              <div className="faq-box">
                <h3>Common Questions</h3>
                <div className="faq-item">
                  <strong>Is there really no API key required?</strong>
                  <p>Correct! The API is completely open and free to use without any authentication.</p>
                </div>
                <div className="faq-item">
                  <strong>What are the rate limits?</strong>
                  <p>We have fair-use limits: 100 requests/min, 10 requests/sec, and 10,000 requests/day per IP.</p>
                </div>
                <div className="faq-item">
                  <strong>Can I use this commercially?</strong>
                  <p>Yes! NewsAPI AI is free for both personal and commercial use.</p>
                </div>
                <div className="faq-item">
                  <strong>How can I contribute?</strong>
                  <p>Check out our <a href="https://github.com/dc-codes426/newsapi-ai" target="_blank" rel="noopener noreferrer">GitHub</a> for ways to contribute code, documentation, or feedback.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

export default Contact
