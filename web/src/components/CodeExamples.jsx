import React, { useState } from 'react'
import './CodeExamples.css'

const examples = [
  {
    id: 1,
    title: 'Semantic Search',
    description: 'Query using natural language - no keyword matching needed',
    request: `POST /v2/semantic-search
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "query": "What are the latest developments in renewable energy?",
  "language": "en",
  "limit": 10
}`,
    response: `{
  "status": "ok",
  "relevanceScore": 0.94,
  "totalResults": 127,
  "articles": [
    {
      "source": { "id": "nature", "name": "Nature" },
      "title": "Breakthrough in Solar Panel Efficiency",
      "description": "New perovskite cells achieve 32% efficiency...",
      "url": "https://nature.com/solar-breakthrough",
      "relevance": 0.96,
      "sentiment": "positive",
      "topics": ["renewable energy", "solar power", "technology"],
      "publishedAt": "2025-11-02T09:15:00Z"
    }
  ]
}`
  },
  {
    id: 2,
    title: 'AI Agent Context',
    description: 'Perfect for RAG systems - get context-aware news for your AI',
    request: `POST /v2/agent-context
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "topic": "AI regulations",
  "context": "Preparing briefing for tech policy meeting",
  "timeframe": "last_7_days",
  "summarize": true
}`,
    response: `{
  "status": "ok",
  "summary": "Recent AI regulation developments focus on...",
  "keyPoints": [
    "EU AI Act enters final approval stage",
    "US proposes new AI safety framework",
    "Tech companies respond to compliance requirements"
  ],
  "articles": [
    {
      "source": { "id": "reuters", "name": "Reuters" },
      "title": "EU Parliament Approves AI Act",
      "summary": "Landmark legislation sets global precedent...",
      "relevance": 0.98,
      "publishedAt": "2025-10-30T14:20:00Z"
    }
  ]
}`
  },
  {
    id: 3,
    title: 'Topic Monitoring',
    description: 'Keep your AI agents updated on specific topics',
    request: `POST /v2/monitor-topic
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "topics": ["cryptocurrency", "blockchain", "DeFi"],
  "sentiment_filter": "neutral,positive",
  "min_relevance": 0.8,
  "limit": 20
}`,
    response: `{
  "status": "ok",
  "monitoring": {
    "topics": ["cryptocurrency", "blockchain", "DeFi"],
    "trending": "Bitcoin ETF approval"
  },
  "articles": [
    {
      "source": { "id": "coindesk", "name": "CoinDesk" },
      "title": "SEC Approves First Bitcoin ETF",
      "topics": ["cryptocurrency", "regulation", "investment"],
      "sentiment": "positive",
      "confidence": 0.89,
      "publishedAt": "2025-11-01T16:45:00Z"
    }
  ]
}`
  },
  {
    id: 4,
    title: 'Conversational Query',
    description: 'Ask questions naturally - ideal for chatbots and assistants',
    request: `POST /v2/ask
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "question": "How are tech companies responding to the new privacy laws?",
  "include_quotes": true,
  "max_articles": 5
}`,
    response: `{
  "status": "ok",
  "answer": "Tech companies are adapting to new privacy laws by...",
  "confidence": 0.91,
  "sources": [
    {
      "source": { "id": "techcrunch", "name": "TechCrunch" },
      "title": "Meta Announces Privacy Compliance Updates",
      "quote": "We're implementing comprehensive changes...",
      "relevance": 0.94,
      "publishedAt": "2025-11-01T11:30:00Z"
    }
  ],
  "relatedTopics": ["GDPR", "data privacy", "tech regulation"]
}`
  }
]

function CodeExamples() {
  const [activeExample, setActiveExample] = useState(0)

  return (
    <section className="code-examples" id="get-started">
      <div className="container">
        <h2 className="section-title">Built for AI Agents</h2>
        <p className="section-subtitle">
          Semantic search, natural language queries, and context-aware responses designed for modern AI applications
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
