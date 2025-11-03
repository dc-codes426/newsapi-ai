import React, { useState } from 'react'
import './Documentation.css'

const Documentation = () => {
  const [activeSection, setActiveSection] = useState('quickstart')

  const sections = {
    quickstart: {
      title: 'Quick Start',
      content: (
        <div className="doc-content">
          <h2>Get Started in 5 Minutes</h2>
          <p className="doc-intro">
            Welcome to NewsAPI AI! This guide will help you make your first API call and integrate
            news intelligence into your AI applications.
          </p>

          <div className="doc-section">
            <h3>1. Make Your First Request</h3>
            <p>No authentication required! Just make a request to our API:</p>
            <pre className="code-block">
{`curl -X POST https://api.newsapi-ai.com/v2/semantic-search \\
  -H "Content-Type: application/json" \\
  -d '{
    "query": "What are the latest AI developments?",
    "limit": 5
  }'`}
            </pre>
          </div>

          <div className="doc-section">
            <h3>2. Example Response</h3>
            <pre className="code-block">
{`{
  "status": "ok",
  "relevanceScore": 0.94,
  "totalResults": 127,
  "articles": [
    {
      "source": { "id": "techcrunch", "name": "TechCrunch" },
      "title": "OpenAI Announces GPT-5",
      "description": "Major advancement in AI capabilities...",
      "url": "https://techcrunch.com/gpt5-announcement",
      "relevance": 0.96,
      "sentiment": "positive",
      "publishedAt": "2025-11-02T10:00:00Z"
    }
  ]
}`}
            </pre>
          </div>

        </div>
      )
    },
    rateLimits: {
      title: 'Rate Limits & Usage',
      content: (
        <div className="doc-content">
          <h2>Rate Limits & Usage</h2>
          <p className="doc-intro">
            NewsAPI AI is completely free to use. We have fair-use rate limits to ensure the service
            remains available for everyone.
          </p>

          <div className="doc-section">
            <h3>Fair Use Policy</h3>
            <div className="info-box">
              <p><strong>Our API is 100% free with no authentication required.</strong></p>
              <p>To maintain service quality, we ask that you:</p>
              <ul>
                <li>Limit requests to <strong>reasonable usage</strong> for your application</li>
                <li>Implement <strong>caching</strong> where possible to reduce redundant requests</li>
                <li>Be considerate of other users sharing the service</li>
              </ul>
            </div>
          </div>

          <div className="doc-section">
            <h3>Current Limits</h3>
            <table className="doc-table">
              <thead>
                <tr>
                  <th>Limit Type</th>
                  <th>Value</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Rate Limit</td>
                  <td>100 requests/min</td>
                  <td>Maximum requests per minute per IP</td>
                </tr>
                <tr>
                  <td>Burst Limit</td>
                  <td>10 requests/sec</td>
                  <td>Short burst allowance</td>
                </tr>
                <tr>
                  <td>Daily Limit</td>
                  <td>10,000 requests/day</td>
                  <td>Maximum daily requests per IP</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="doc-section">
            <h3>Best Practices</h3>
            <ul>
              <li><strong>Cache responses</strong> - Store results locally to minimize repeated queries</li>
              <li><strong>Batch requests</strong> - Combine multiple queries when possible</li>
              <li><strong>Handle errors gracefully</strong> - Implement retry logic with exponential backoff</li>
              <li><strong>Respect rate limits</strong> - Monitor response headers for rate limit status</li>
            </ul>
          </div>
        </div>
      )
    },
    semanticSearch: {
      title: 'Semantic Search',
      content: (
        <div className="doc-content">
          <h2>Semantic Search</h2>
          <p className="doc-intro">
            Search news using natural language. Our AI understands context and intent, returning
            the most relevant articles based on meaning, not just keyword matching.
          </p>

          <div className="doc-section">
            <h3>Endpoint</h3>
            <div className="endpoint-box">
              <span className="method">POST</span>
              <code>/v2/semantic-search</code>
            </div>
          </div>

          <div className="doc-section">
            <h3>Request Parameters</h3>
            <table className="doc-table">
              <thead>
                <tr>
                  <th>Parameter</th>
                  <th>Type</th>
                  <th>Required</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><code>query</code></td>
                  <td>string</td>
                  <td>Yes</td>
                  <td>Natural language search query</td>
                </tr>
                <tr>
                  <td><code>language</code></td>
                  <td>string</td>
                  <td>No</td>
                  <td>Language code (e.g., 'en', 'es')</td>
                </tr>
                <tr>
                  <td><code>limit</code></td>
                  <td>integer</td>
                  <td>No</td>
                  <td>Number of results (default: 10, max: 100)</td>
                </tr>
                <tr>
                  <td><code>from_date</code></td>
                  <td>string</td>
                  <td>No</td>
                  <td>ISO 8601 date (e.g., '2025-11-01')</td>
                </tr>
                <tr>
                  <td><code>to_date</code></td>
                  <td>string</td>
                  <td>No</td>
                  <td>ISO 8601 date</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="doc-section">
            <h3>Example Request</h3>
            <pre className="code-block">
{`POST /v2/semantic-search
Content-Type: application/json

{
  "query": "What are the latest developments in renewable energy?",
  "language": "en",
  "limit": 10
}`}
            </pre>
          </div>

          <div className="doc-section">
            <h3>Response Format</h3>
            <pre className="code-block">
{`{
  "status": "ok",
  "relevanceScore": 0.94,
  "totalResults": 127,
  "articles": [
    {
      "source": {
        "id": "nature",
        "name": "Nature"
      },
      "title": "Breakthrough in Solar Panel Efficiency",
      "description": "New perovskite cells achieve 32% efficiency...",
      "url": "https://nature.com/solar-breakthrough",
      "relevance": 0.96,
      "sentiment": "positive",
      "topics": ["renewable energy", "solar power", "technology"],
      "publishedAt": "2025-11-02T09:15:00Z"
    }
  ]
}`}
            </pre>
          </div>
        </div>
      )
    },
    agentContext: {
      title: 'AI Agent Context',
      content: (
        <div className="doc-content">
          <h2>AI Agent Context</h2>
          <p className="doc-intro">
            Get context-aware news summaries optimized for RAG systems and AI agents.
            Perfect for feeding information to ChatGPT, Claude, or custom LLM applications.
          </p>

          <div className="doc-section">
            <h3>Endpoint</h3>
            <div className="endpoint-box">
              <span className="method">POST</span>
              <code>/v2/agent-context</code>
            </div>
          </div>

          <div className="doc-section">
            <h3>Request Parameters</h3>
            <table className="doc-table">
              <thead>
                <tr>
                  <th>Parameter</th>
                  <th>Type</th>
                  <th>Required</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><code>topic</code></td>
                  <td>string</td>
                  <td>Yes</td>
                  <td>Topic or subject area</td>
                </tr>
                <tr>
                  <td><code>context</code></td>
                  <td>string</td>
                  <td>No</td>
                  <td>Additional context for better results</td>
                </tr>
                <tr>
                  <td><code>timeframe</code></td>
                  <td>string</td>
                  <td>No</td>
                  <td>'last_24h', 'last_7_days', 'last_30_days'</td>
                </tr>
                <tr>
                  <td><code>summarize</code></td>
                  <td>boolean</td>
                  <td>No</td>
                  <td>Include AI-generated summary (default: true)</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="doc-section">
            <h3>Example Request</h3>
            <pre className="code-block">
{`POST /v2/agent-context
Content-Type: application/json

{
  "topic": "AI regulations",
  "context": "Preparing briefing for tech policy meeting",
  "timeframe": "last_7_days",
  "summarize": true
}`}
            </pre>
          </div>
        </div>
      )
    },
    topicMonitoring: {
      title: 'Topic Monitoring',
      content: (
        <div className="doc-content">
          <h2>Topic Monitoring</h2>
          <p className="doc-intro">
            Monitor specific topics, companies, or trends in real-time. Get alerts and summaries
            tailored for your AI agent's knowledge needs.
          </p>

          <div className="doc-section">
            <h3>Endpoint</h3>
            <div className="endpoint-box">
              <span className="method">POST</span>
              <code>/v2/monitor-topic</code>
            </div>
          </div>

          <div className="doc-section">
            <h3>Request Parameters</h3>
            <table className="doc-table">
              <thead>
                <tr>
                  <th>Parameter</th>
                  <th>Type</th>
                  <th>Required</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><code>topics</code></td>
                  <td>array</td>
                  <td>Yes</td>
                  <td>Array of topics to monitor</td>
                </tr>
                <tr>
                  <td><code>sentiment_filter</code></td>
                  <td>string</td>
                  <td>No</td>
                  <td>'positive', 'neutral', 'negative' (comma-separated)</td>
                </tr>
                <tr>
                  <td><code>min_relevance</code></td>
                  <td>float</td>
                  <td>No</td>
                  <td>Minimum relevance score (0.0 - 1.0)</td>
                </tr>
                <tr>
                  <td><code>limit</code></td>
                  <td>integer</td>
                  <td>No</td>
                  <td>Number of results (default: 20, max: 100)</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="doc-section">
            <h3>Example Request</h3>
            <pre className="code-block">
{`POST /v2/monitor-topic
Content-Type: application/json

{
  "topics": ["cryptocurrency", "blockchain", "DeFi"],
  "sentiment_filter": "neutral,positive",
  "min_relevance": 0.8,
  "limit": 20
}`}
            </pre>
          </div>
        </div>
      )
    },
    conversationalQuery: {
      title: 'Conversational Query',
      content: (
        <div className="doc-content">
          <h2>Conversational Query</h2>
          <p className="doc-intro">
            Ask questions in natural language and get direct answers with sources.
            Perfect for chatbots, virtual assistants, and conversational AI.
          </p>

          <div className="doc-section">
            <h3>Endpoint</h3>
            <div className="endpoint-box">
              <span className="method">POST</span>
              <code>/v2/ask</code>
            </div>
          </div>

          <div className="doc-section">
            <h3>Request Parameters</h3>
            <table className="doc-table">
              <thead>
                <tr>
                  <th>Parameter</th>
                  <th>Type</th>
                  <th>Required</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><code>question</code></td>
                  <td>string</td>
                  <td>Yes</td>
                  <td>Natural language question</td>
                </tr>
                <tr>
                  <td><code>include_quotes</code></td>
                  <td>boolean</td>
                  <td>No</td>
                  <td>Include relevant quotes from articles</td>
                </tr>
                <tr>
                  <td><code>max_articles</code></td>
                  <td>integer</td>
                  <td>No</td>
                  <td>Maximum source articles to use (default: 5)</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="doc-section">
            <h3>Example Request</h3>
            <pre className="code-block">
{`POST /v2/ask
Content-Type: application/json

{
  "question": "How are tech companies responding to the new privacy laws?",
  "include_quotes": true,
  "max_articles": 5
}`}
            </pre>
          </div>
        </div>
      )
    },
  }

  return (
    <div className="documentation-page">
      <div className="doc-container">
        <aside className="doc-sidebar">
          <h3 className="sidebar-title">Documentation</h3>
          <nav className="sidebar-nav">
            <button
              className={`nav-item ${activeSection === 'quickstart' ? 'active' : ''}`}
              onClick={() => setActiveSection('quickstart')}
            >
              Quick Start
            </button>
            <button
              className={`nav-item ${activeSection === 'rateLimits' ? 'active' : ''}`}
              onClick={() => setActiveSection('rateLimits')}
            >
              Rate Limits & Usage
            </button>

            <div className="nav-group">
              <div className="nav-group-title">API Reference</div>
              <button
                className={`nav-item ${activeSection === 'semanticSearch' ? 'active' : ''}`}
                onClick={() => setActiveSection('semanticSearch')}
              >
                Semantic Search
              </button>
              <button
                className={`nav-item ${activeSection === 'agentContext' ? 'active' : ''}`}
                onClick={() => setActiveSection('agentContext')}
              >
                AI Agent Context
              </button>
              <button
                className={`nav-item ${activeSection === 'topicMonitoring' ? 'active' : ''}`}
                onClick={() => setActiveSection('topicMonitoring')}
              >
                Topic Monitoring
              </button>
              <button
                className={`nav-item ${activeSection === 'conversationalQuery' ? 'active' : ''}`}
                onClick={() => setActiveSection('conversationalQuery')}
              >
                Conversational Query
              </button>
            </div>
          </nav>
        </aside>

        <main className="doc-main">
          {sections[activeSection].content}
        </main>
      </div>
    </div>
  )
}

export default Documentation
