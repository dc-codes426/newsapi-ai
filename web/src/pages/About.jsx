import React from 'react'
import './About.css'

function About() {
  return (
    <div className="about-page">
      <section className="about-hero">
        <div className="container">
          <h1 className="about-title">About NewsAPI AI</h1>
          <p className="about-subtitle">
            Building the bridge between AI agents and real-time news intelligence
          </p>
        </div>
      </section>

      <section className="about-content">
        <div className="container">
          <div className="about-section">
            <h2>Our Mission</h2>
            <p>
              NewsAPI AI was created to solve a fundamental challenge in the age of AI: keeping intelligent
              systems informed with current, relevant news. While large language models are incredibly powerful,
              their knowledge is frozen at their training cutoff date. We bridge that gap.
            </p>
            <p>
              Our mission is to democratize access to news intelligence for AI developers, researchers, and
              innovators worldwide. By providing a free, open API with semantic search capabilities, we empower
              anyone to build news-aware AI applications without barriers.
            </p>
          </div>

          <div className="about-section">
            <h2>Why We Built This</h2>
            <div className="reason-grid">
              <div className="reason-card">
                <div className="reason-icon">🤖</div>
                <h3>AI Agents Need Context</h3>
                <p>
                  Modern AI agents, chatbots, and RAG systems need access to current events to provide
                  accurate, timely responses. Traditional news APIs weren't designed for AI consumption.
                </p>
              </div>
              <div className="reason-card">
                <div className="reason-icon">🔍</div>
                <h3>Semantic Search Matters</h3>
                <p>
                  Keyword matching doesn't cut it for AI. Our semantic search understands intent and context,
                  returning truly relevant results that AI systems can actually use.
                </p>
              </div>
              <div className="reason-card">
                <div className="reason-icon">🌍</div>
                <h3>Free for Everyone</h3>
                <p>
                  We believe access to information should be free. No paywalls, no API keys, no registration.
                  Just instant access to news intelligence for your projects.
                </p>
              </div>
              <div className="reason-card">
                <div className="reason-icon">⚡</div>
                <h3>Built for Developers</h3>
                <p>
                  Clean REST API, structured JSON responses, semantic relevance scores, sentiment analysis—
                  everything developers need to integrate news into their applications quickly.
                </p>
              </div>
            </div>
          </div>

          <div className="about-section">
            <h2>How It Works</h2>
            <div className="how-it-works">
              <div className="step">
                <div className="step-number">1</div>
                <div className="step-content">
                  <h3>News Aggregation</h3>
                  <p>
                    We continuously aggregate news from thousands of sources worldwide, covering diverse
                    topics, languages, and perspectives.
                  </p>
                </div>
              </div>
              <div className="step">
                <div className="step-number">2</div>
                <div className="step-content">
                  <h3>AI Processing</h3>
                  <p>
                    Each article is processed through our AI pipeline: semantic embedding, topic extraction,
                    sentiment analysis, and relevance scoring.
                  </p>
                </div>
              </div>
              <div className="step">
                <div className="step-number">3</div>
                <div className="step-content">
                  <h3>Semantic Search</h3>
                  <p>
                    When you query our API, we use semantic similarity to find the most relevant articles
                    based on meaning, not just keyword matches.
                  </p>
                </div>
              </div>
              <div className="step">
                <div className="step-number">4</div>
                <div className="step-content">
                  <h3>Structured Response</h3>
                  <p>
                    Results are returned in a clean, structured format optimized for AI consumption, complete
                    with metadata, relevance scores, and context.
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div className="about-section">
            <h2>Technology Stack</h2>
            <div className="tech-grid">
              <div className="tech-item">
                <h4>🧠 AI & ML</h4>
                <p>State-of-the-art transformer models for semantic understanding and relevance scoring</p>
              </div>
              <div className="tech-item">
                <h4>🔄 Real-Time Processing</h4>
                <p>Continuous news aggregation and processing pipeline for up-to-the-minute updates</p>
              </div>
              <div className="tech-item">
                <h4>🗄️ Vector Database</h4>
                <p>High-performance vector search for lightning-fast semantic queries at scale</p>
              </div>
              <div className="tech-item">
                <h4>☁️ Cloud Infrastructure</h4>
                <p>Scalable, distributed architecture ensuring reliability and low latency worldwide</p>
              </div>
            </div>
          </div>

          <div className="about-section">
            <h2>Open Source & Community</h2>
            <p>
              We believe in building in the open. Our SDKs, examples, and integrations are all open source
              and available on GitHub. We welcome contributions, feedback, and collaboration from the community.
            </p>
            <div className="community-links">
              <a href="https://github.com/dc-codes426/newsapi-ai" className="community-link" target="_blank" rel="noopener noreferrer">
                <span className="link-icon">💻</span>
                <div>
                  <strong>GitHub</strong>
                  <p>Explore our code, SDKs, and examples</p>
                </div>
              </a>
              <a href="https://github.com/dc-codes426/newsapi-ai/discussions" className="community-link" target="_blank" rel="noopener noreferrer">
                <span className="link-icon">💬</span>
                <div>
                  <strong>Discussions</strong>
                  <p>Join the conversation and share ideas</p>
                </div>
              </a>
              <a href="https://github.com/dc-codes426/newsapi-ai/issues" className="community-link" target="_blank" rel="noopener noreferrer">
                <span className="link-icon">🐛</span>
                <div>
                  <strong>Issues</strong>
                  <p>Report bugs and request features</p>
                </div>
              </a>
            </div>
          </div>

          <div className="about-section">
            <h2>Our Commitment</h2>
            <div className="commitment-box">
              <ul>
                <li><strong>Always Free:</strong> NewsAPI AI will always have a free tier for developers and researchers</li>
                <li><strong>Privacy First:</strong> We don't track users, store personal data, or sell information</li>
                <li><strong>Transparent:</strong> Our methodologies, limitations, and data sources are openly documented</li>
                <li><strong>Community-Driven:</strong> We listen to and build for the needs of our developer community</li>
                <li><strong>Continuous Improvement:</strong> We're constantly enhancing our AI models and expanding coverage</li>
              </ul>
            </div>
          </div>

          <div className="about-section cta-section-about">
            <h2>Join Us</h2>
            <p>
              Whether you're building the next great AI assistant, conducting research, or just experimenting
              with news intelligence, we're excited to see what you create.
            </p>
            <div className="cta-buttons">
              <a href="/documentation" className="btn-about btn-primary-about">
                Start Building
              </a>
              <a href="https://github.com/dc-codes426/newsapi-ai" className="btn-about btn-secondary-about" target="_blank" rel="noopener noreferrer">
                View on GitHub
              </a>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

export default About
