import React, { useState } from 'react'
import './CodeExamples.css'

const examples = [
  {
    id: 1,
    title: 'Top Headlines',
    description: 'Get breaking news headlines for a country',
    request: `GET /v2/top-headlines?country=us&category=business
Authorization: Bearer YOUR_API_KEY`,
    response: `{
  "status": "ok",
  "totalResults": 38,
  "articles": [
    {
      "source": { "id": "techcrunch", "name": "TechCrunch" },
      "author": "Sarah Johnson",
      "title": "AI Startup Raises $100M in Series B",
      "description": "Leading AI company secures major funding...",
      "url": "https://techcrunch.com/article",
      "publishedAt": "2025-11-02T10:00:00Z"
    }
  ]
}`
  },
  {
    id: 2,
    title: 'Search Everything',
    description: 'Search through millions of articles',
    request: `GET /v2/everything?q=artificial+intelligence&sortBy=publishedAt
Authorization: Bearer YOUR_API_KEY`,
    response: `{
  "status": "ok",
  "totalResults": 1247,
  "articles": [
    {
      "source": { "id": "wired", "name": "Wired" },
      "author": "Alex Chen",
      "title": "The Future of AI in Healthcare",
      "description": "How artificial intelligence is transforming...",
      "url": "https://wired.com/ai-healthcare",
      "publishedAt": "2025-11-02T08:30:00Z"
    }
  ]
}`
  },
  {
    id: 3,
    title: 'Filter by Source',
    description: 'Get articles from specific news sources',
    request: `GET /v2/top-headlines?sources=bbc-news
Authorization: Bearer YOUR_API_KEY`,
    response: `{
  "status": "ok",
  "totalResults": 10,
  "articles": [
    {
      "source": { "id": "bbc-news", "name": "BBC News" },
      "author": "BBC News",
      "title": "Global Climate Summit Reaches Agreement",
      "description": "World leaders agree on new climate targets...",
      "url": "https://bbc.com/news/climate",
      "publishedAt": "2025-11-02T12:00:00Z"
    }
  ]
}`
  },
  {
    id: 4,
    title: 'Date Range Query',
    description: 'Search articles within a date range',
    request: `GET /v2/everything?q=technology&from=2025-10-01&to=2025-11-01
Authorization: Bearer YOUR_API_KEY`,
    response: `{
  "status": "ok",
  "totalResults": 856,
  "articles": [
    {
      "source": { "id": "the-verge", "name": "The Verge" },
      "author": "David Kim",
      "title": "New Smartphone Technology Unveiled",
      "description": "Latest mobile innovation promises...",
      "url": "https://theverge.com/tech-news",
      "publishedAt": "2025-10-28T15:20:00Z"
    }
  ]
}`
  }
]

function CodeExamples() {
  const [activeExample, setActiveExample] = useState(0)

  return (
    <section className="code-examples" id="get-started">
      <div className="container">
        <h2 className="section-title">See it in action</h2>
        <p className="section-subtitle">
          Simple REST API requests that return JSON responses
        </p>

        <div className="examples-nav">
          {examples.map((example, index) => (
            <button
              key={example.id}
              className={`example-tab ${activeExample === index ? 'active' : ''}`}
              onClick={() => setActiveExample(index)}
            >
              {example.title}
            </button>
          ))}
        </div>

        <div className="example-content">
          <div className="example-description">
            <p>{examples[activeExample].description}</p>
          </div>

          <div className="code-blocks">
            <div className="code-block">
              <div className="code-header">
                <span className="code-label">Request</span>
                <button className="copy-btn" onClick={() => navigator.clipboard.writeText(examples[activeExample].request)}>
                  Copy
                </button>
              </div>
              <pre className="code-content">
                <code>{examples[activeExample].request}</code>
              </pre>
            </div>

            <div className="code-block">
              <div className="code-header">
                <span className="code-label">Response</span>
                <button className="copy-btn" onClick={() => navigator.clipboard.writeText(examples[activeExample].response)}>
                  Copy
                </button>
              </div>
              <pre className="code-content">
                <code>{examples[activeExample].response}</code>
              </pre>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default CodeExamples
