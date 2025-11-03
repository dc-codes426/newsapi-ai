import React from 'react'
import './UseCases.css'

const useCases = [
  {
    id: 1,
    icon: '💼',
    title: 'Business Intelligence Bots',
    description: 'Build AI assistants that monitor industry news, competitor activity, and market trends. Keep executives informed with automated daily briefings.',
    tags: ['Slack Bots', 'Email Digests', 'Dashboard Updates']
  },
  {
    id: 2,
    icon: '🎓',
    title: 'Research Assistants',
    description: 'Create AI agents that gather and summarize academic news, scientific breakthroughs, and research publications for students and professionals.',
    tags: ['Academic Research', 'Literature Review', 'Citation Tracking']
  },
  {
    id: 3,
    icon: '📱',
    title: 'Customer Support AI',
    description: 'Enhance chatbots with real-time knowledge about product launches, service updates, and industry developments to provide accurate support.',
    tags: ['ChatGPT Plugins', 'Support Bots', 'Knowledge Base']
  },
  {
    id: 4,
    icon: '📈',
    title: 'Trading & Finance Agents',
    description: 'Power algorithmic trading bots with breaking financial news, earnings reports, and market-moving events for informed decision-making.',
    tags: ['Market Analysis', 'Sentiment Trading', 'Risk Monitoring']
  },
  {
    id: 5,
    icon: '✍️',
    title: 'Content Generation',
    description: 'Feed your AI writing assistants with current events and trending topics to create timely, relevant, and engaging content automatically.',
    tags: ['Blog Posts', 'Social Media', 'Newsletters']
  },
  {
    id: 6,
    icon: '🔔',
    title: 'Alert & Monitoring Systems',
    description: 'Build intelligent notification systems that alert teams when specific topics, companies, or events appear in the news with contextual summaries.',
    tags: ['Crisis Detection', 'Brand Monitoring', 'Compliance Alerts']
  }
]

function UseCases() {
  return (
    <section className="use-cases">
      <div className="container">
        <h2 className="section-title">Use Cases</h2>
        <p className="section-subtitle">
          See how developers are using NewsAPI AI to build intelligent applications
        </p>

        <div className="use-cases-grid">
          {useCases.map(useCase => (
            <div key={useCase.id} className="use-case-card">
              <div className="use-case-icon">{useCase.icon}</div>
              <h3 className="use-case-title">{useCase.title}</h3>
              <p className="use-case-description">{useCase.description}</p>
              <div className="use-case-tags">
                {useCase.tags.map((tag, index) => (
                  <span key={index} className="use-case-tag">{tag}</span>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="use-case-highlight">
          <div className="highlight-content">
            <h3 className="highlight-title">Perfect for RAG Systems</h3>
            <p className="highlight-description">
              Our API is optimized for Retrieval-Augmented Generation. Responses include relevance scores,
              topic extraction, sentiment analysis, and structured data that integrates seamlessly with
              vector databases and embedding models.
            </p>
            <div className="highlight-features">
              <div className="highlight-feature">
                <span className="highlight-icon">✓</span>
                <span>Pre-chunked content ready for embeddings</span>
              </div>
              <div className="highlight-feature">
                <span className="highlight-icon">✓</span>
                <span>Semantic similarity scoring included</span>
              </div>
              <div className="highlight-feature">
                <span className="highlight-icon">✓</span>
                <span>Compatible with LangChain, LlamaIndex, and more</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default UseCases
