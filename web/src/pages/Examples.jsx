import React, { useState } from 'react'
import './Examples.css'

const examples = [
  {
    id: 1,
    category: 'Basic Usage',
    title: 'Simple Semantic Search',
    description: 'Search for news using natural language. No complex query syntax needed—just ask naturally.',
    language: 'bash',
    request: `curl -X POST http://localhost:8500/query \\
  -H "Content-Type: application/json" \\
  -d '{
    "query": "What are the latest developments in renewable energy?",
    "response_format": "both"
  }'`,
    response: `{
  "session_id": "abc123",
  "format": "both",
  "response": "I found several recent articles about renewable energy developments...",
  "articles": [
    {
      "source": {
        "id": "techcrunch",
        "name": "TechCrunch"
      },
      "title": "Breakthrough in Solar Panel Efficiency",
      "description": "Scientists achieve 32% efficiency with new perovskite cells",
      "url": "https://techcrunch.com/solar-breakthrough",
      "publishedAt": "2025-11-02T09:15:00Z"
    }
  ],
  "total_results": 15
}`
  },
  {
    id: 2,
    category: 'Basic Usage',
    title: 'Natural Language Query',
    description: 'Get AI-powered answers with sources. Perfect for chatbots and conversational interfaces.',
    language: 'python',
    request: `import requests

response = requests.post(
    "http://localhost:8500/query",
    json={
        "query": "How are tech companies responding to AI regulations?",
        "response_format": "natural"
    }
)

result = response.json()
print(result["response"])`,
    response: `{
  "session_id": "xyz789",
  "format": "natural",
  "response": "Tech companies are taking several approaches to AI regulations. Meta announced comprehensive compliance updates, Google published new AI ethics guidelines, and OpenAI is working with regulators on safety frameworks. The industry generally supports reasonable regulation while advocating for innovation-friendly policies."
}`
  },
  {
    id: 3,
    category: 'Basic Usage',
    title: 'Using Your Own API Key',
    description: 'Provide your own NewsAPI key to avoid rate limits on the server\'s shared key.',
    language: 'bash',
    request: `curl -X POST http://localhost:8500/query \\
  -H "Content-Type: application/json" \\
  -d '{
    "query": "Latest news about electric vehicles",
    "news_api_key": "your_newsapi_key_here",
    "response_format": "both"
  }'`,
    response: `{
  "session_id": "def456",
  "format": "both",
  "response": "I found recent articles about electric vehicles using your API key...",
  "articles": [...],
  "total_results": 25
}

// Get your free NewsAPI key at https://newsapi.org/register`
  },
  {
    id: 4,
    category: 'Advanced Usage',
    title: 'Multi-Turn Conversation',
    description: 'Use session IDs to maintain context across multiple queries.',
    language: 'javascript',
    request: `// First query
const session1 = await fetch('http://localhost:8500/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: "Tell me about recent SpaceX launches",
    response_format: "natural"
  })
});
const result1 = await session1.json();
const sessionId = result1.session_id;

// Follow-up query with context
const session2 = await fetch('http://localhost:8500/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: "What were the mission objectives?",
    session_id: sessionId,  // Maintains context
    response_format: "natural"
  })
});
const result2 = await session2.json();`,
    response: `// Second response understands context from first query
{
  "session_id": "same-session-id",
  "format": "natural",
  "response": "The Starlink mission objectives were to deploy 23 satellites into low Earth orbit, test the new Falcon 9 booster recovery system, and demonstrate improved payload deployment mechanisms..."
}`
  },
  {
    id: 5,
    category: 'Advanced Usage',
    title: 'Structured Data Extraction',
    description: 'Get structured article data for RAG systems and knowledge bases.',
    language: 'python',
    request: `import requests

# Get structured data only
response = requests.post(
    "http://localhost:8500/query",
    json={
        "query": "Latest cryptocurrency news from the past week",
        "response_format": "structured"
    }
)

data = response.json()

# Process articles for your RAG system
for article in data["articles"]:
    print(f"Title: {article['title']}")
    print(f"Source: {article['source']['name']}")
    print(f"URL: {article['url']}")
    print(f"Published: {article['publishedAt']}")
    print("---")`,
    response: `{
  "session_id": "def456",
  "format": "structured",
  "articles": [
    {
      "source": {
        "id": "coindesk",
        "name": "CoinDesk"
      },
      "author": "Jane Smith",
      "title": "Bitcoin Reaches New All-Time High",
      "description": "BTC surpasses previous record amid institutional adoption",
      "url": "https://coindesk.com/bitcoin-ath-2025",
      "urlToImage": "https://coindesk.com/images/bitcoin-chart.jpg",
      "publishedAt": "2025-11-01T14:30:00Z",
      "content": "Bitcoin reached a new all-time high today..."
    }
  ],
  "total_results": 42
}`
  },
  {
    id: 6,
    category: 'AI Agent Integration',
    title: 'LangChain Integration',
    description: 'Integrate NewsAPI AI into your LangChain applications.',
    language: 'python',
    request: `from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI
import requests

def search_news(query: str) -> str:
    """Search news using NewsAPI AI"""
    response = requests.post(
        "http://localhost:8500/query",
        json={
            "query": query,
            "response_format": "natural"
        }
    )
    return response.json()["response"]

# Create LangChain tool
news_tool = Tool(
    name="NewsSearch",
    func=search_news,
    description="Search current news. Use this when you need recent information about events, companies, or topics."
)

# Initialize agent with news tool
llm = OpenAI(temperature=0)
agent = initialize_agent(
    [news_tool],
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Use the agent
result = agent.run("What's happening with AI regulation this week?")
print(result)`,
    response: `> Entering new AgentExecutor chain...
I need current information about AI regulation

Action: NewsSearch
Action Input: "AI regulation developments this week"

Observation: Recent AI regulation news includes the EU AI Act entering final stages, US proposing new safety frameworks, and major tech companies announcing compliance initiatives...

Final Answer: This week has seen significant AI regulation activity...`
  },
  {
    id: 7,
    category: 'AI Agent Integration',
    title: 'RAG System with Context',
    description: 'Build a Retrieval-Augmented Generation system with current news.',
    language: 'python',
    request: `import requests
from openai import OpenAI

def get_news_context(topic: str) -> str:
    """Fetch relevant news articles as context"""
    response = requests.post(
        "http://localhost:8500/query",
        json={
            "query": f"Recent news about {topic}",
            "response_format": "both"
        }
    )

    data = response.json()

    # Build context from articles
    context = f"AI Response: {data['response']}\\n\\n"
    context += "Source Articles:\\n"

    for article in data.get("articles", [])[:5]:
        context += f"- {article['title']} ({article['source']['name']})\\n"
        context += f"  {article['description']}\\n\\n"

    return context

# Use in RAG pipeline
client = OpenAI()
user_question = "What are the latest climate change initiatives?"

# Get current news context
news_context = get_news_context("climate change initiatives")

# Generate response with context
completion = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant. Use the provided news context to answer questions accurately."
        },
        {
            "role": "user",
            "content": f"Context:\\n{news_context}\\n\\nQuestion: {user_question}"
        }
    ]
)

print(completion.choices[0].message.content)`,
    response: `Based on recent news, several major climate initiatives are underway:

1. The UN Climate Summit announced new carbon reduction commitments from 50+ countries
2. The US launched a $10B green infrastructure program
3. Major corporations formed a climate tech consortium

These initiatives show growing momentum toward sustainable solutions...

Sources: Reuters, Bloomberg Green, The Guardian`
  },
  {
    id: 8,
    category: 'Real-World Use Cases',
    title: 'Slack Bot Integration',
    description: 'Create a Slack bot that answers questions with current news.',
    language: 'javascript',
    request: `const { App } = require('@slack/bolt');
const axios = require('axios');

const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  signingSecret: process.env.SLACK_SIGNING_SECRET
});

// Listen for mentions
app.event('app_mention', async ({ event, client, say }) => {
  const question = event.text.replace(/<@.*?>/, '').trim();

  try {
    // Query NewsAPI AI
    const response = await axios.post('http://localhost:8500/query', {
      query: question,
      response_format: 'both'
    });

    const { response: answer, articles, total_results } = response.data;

    // Format response for Slack
    let blocks = [
      {
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: answer
        }
      }
    ];

    // Add article links
    if (articles && articles.length > 0) {
      blocks.push({
        type: 'divider'
      });
      blocks.push({
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: '*Sources:*'
        }
      });

      articles.slice(0, 3).forEach(article => {
        blocks.push({
          type: 'section',
          text: {
            type: 'mrkdwn',
            text: \`• <\${article.url}|\${article.title}> - \${article.source.name}\`
          }
        });
      });
    }

    await say({ blocks });

  } catch (error) {
    await say(\`Sorry, I encountered an error: \${error.message}\`);
  }
});

app.start(process.env.PORT || 3000);
console.log('News bot is running!');`,
    response: `# In Slack:
User: @newsbot What's the latest on climate change?

NewsBot: Recent climate change news includes major developments at the UN Climate Summit, new carbon reduction commitments from 50+ countries, and the launch of a $10B green infrastructure program in the US. Scientists also reported concerning data about Arctic ice melt acceleration.

Sources:
• UN Climate Summit Reaches Historic Agreement - Reuters
• 50 Countries Commit to Net Zero by 2040 - Bloomberg
• US Announces $10B Green Infrastructure Fund - The Guardian`
  },
  {
    id: 9,
    category: 'Real-World Use Cases',
    title: 'Daily News Digest',
    description: 'Generate automated daily digests for specific topics.',
    language: 'python',
    request: `import requests
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def generate_daily_digest(topics):
    """Generate daily news digest for topics"""
    digest = f"# Daily News Digest - {datetime.now().strftime('%Y-%m-%d')}\\n\\n"

    for topic in topics:
        response = requests.post(
            "http://localhost:8500/query",
            json={
                "query": f"Top news about {topic} from the last 24 hours",
                "response_format": "both"
            }
        )

        data = response.json()

        digest += f"## {topic.title()}\\n\\n"
        digest += f"{data.get('response', 'No summary available.')}\\n\\n"

        articles = data.get('articles', [])[:5]
        if articles:
            digest += "### Top Articles:\\n"
            for article in articles:
                digest += f"- [{article['title']}]({article['url']})\\n"
                digest += f"  *{article['source']['name']}* - {article['publishedAt']}\\n\\n"

        digest += "---\\n\\n"

    return digest

# Generate digest
topics = ["artificial intelligence", "renewable energy", "cryptocurrency"]
digest_content = generate_daily_digest(topics)

# Send email (example)
msg = MIMEMultipart('alternative')
msg['Subject'] = f"Your Daily News Digest - {datetime.now().strftime('%Y-%m-%d')}"
msg['From'] = "newsbot@example.com"
msg['To'] = "you@example.com"

msg.attach(MIMEText(digest_content, 'plain'))

# Send via SMTP
# smtp_server.send_message(msg)

print(digest_content)`,
    response: `# Daily News Digest - 2025-11-03

## Artificial Intelligence

Recent AI developments include OpenAI's announcement of GPT-5, Google's new AI ethics guidelines, and major progress in AI regulation discussions...

### Top Articles:
- [OpenAI Unveils GPT-5 with Revolutionary Capabilities](https://techcrunch.com/gpt5)
  *TechCrunch* - 2025-11-03T08:00:00Z

- [Google Publishes Comprehensive AI Ethics Framework](https://reuters.com/google-ai)
  *Reuters* - 2025-11-02T16:30:00Z

---

## Renewable Energy

Major renewable energy news this week includes breakthrough solar panel efficiency, new offshore wind projects, and government clean energy incentives...

### Top Articles:
- [Scientists Achieve Record Solar Panel Efficiency](https://nature.com/solar)
  *Nature* - 2025-11-02T14:00:00Z`
  }
]

function Examples() {
  const [activeCategory, setActiveCategory] = useState('Basic Usage')
  const [activeExample, setActiveExample] = useState(examples[0])

  const categories = [...new Set(examples.map(ex => ex.category))]

  const filteredExamples = examples.filter(ex => ex.category === activeCategory)

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
  }

  return (
    <div className="examples-page">
      <section className="examples-hero">
        <div className="container">
          <h1 className="examples-title">API Examples</h1>
          <p className="examples-subtitle">
            Learn how to integrate NewsAPI AI into your applications with practical examples
          </p>
        </div>
      </section>

      <section className="examples-content">
        <div className="container">
          <div className="examples-layout">
            <aside className="examples-sidebar">
              <h3 className="sidebar-title">Categories</h3>
              <nav className="category-nav">
                {categories.map(category => (
                  <button
                    key={category}
                    className={`category-item ${activeCategory === category ? 'active' : ''}`}
                    onClick={() => {
                      setActiveCategory(category)
                      setActiveExample(examples.find(ex => ex.category === category))
                    }}
                  >
                    {category}
                  </button>
                ))}
              </nav>

              <div className="example-list">
                <h4 className="list-title">Examples</h4>
                {filteredExamples.map(example => (
                  <button
                    key={example.id}
                    className={`example-item ${activeExample.id === example.id ? 'active' : ''}`}
                    onClick={() => setActiveExample(example)}
                  >
                    {example.title}
                  </button>
                ))}
              </div>
            </aside>

            <main className="examples-main">
              <div className="example-header">
                <span className="example-category">{activeExample.category}</span>
                <h2 className="example-title">{activeExample.title}</h2>
                <p className="example-description">{activeExample.description}</p>
              </div>

              <div className="code-section">
                <div className="code-header">
                  <span className="code-label">
                    {activeExample.language === 'bash' ? 'cURL' :
                     activeExample.language === 'python' ? 'Python' :
                     activeExample.language === 'javascript' ? 'JavaScript' :
                     activeExample.language}
                  </span>
                  <button
                    className="copy-button"
                    onClick={() => copyToClipboard(activeExample.request)}
                  >
                    Copy
                  </button>
                </div>
                <pre className="code-block">
                  <code className={`language-${activeExample.language}`}>
                    {activeExample.request}
                  </code>
                </pre>
              </div>

              <div className="response-section">
                <div className="response-header">
                  <span className="response-label">Response</span>
                  <button
                    className="copy-button"
                    onClick={() => copyToClipboard(activeExample.response)}
                  >
                    Copy
                  </button>
                </div>
                <pre className="response-block">
                  <code className="language-json">
                    {activeExample.response}
                  </code>
                </pre>
              </div>
            </main>
          </div>
        </div>
      </section>

      <section className="quick-tips">
        <div className="container">
          <h2>Quick Tips</h2>
          <div className="tips-grid">
            <div className="tip-card">
              <h3>Session Management</h3>
              <p>Use session IDs to maintain conversation context across multiple queries. The AI will remember previous questions and provide more relevant answers.</p>
            </div>
            <div className="tip-card">
              <h3>Response Formats</h3>
              <p>Choose "natural" for conversational responses, "structured" for article data, or "both" for complete information with AI analysis.</p>
            </div>
            <div className="tip-card">
              <h3>Error Handling</h3>
              <p>Always implement proper error handling and retry logic. Check the health endpoint before making requests in production.</p>
            </div>
            <div className="tip-card">
              <h3>Performance</h3>
              <p>Cache responses when possible and batch similar queries together to optimize API usage and improve response times.</p>
            </div>
            <div className="tip-card">
              <h3>Using Your Own API Key</h3>
              <p>Avoid rate limits by providing your own NewsAPI key in the request. Get a free key at newsapi.org/register and include it in the "news_api_key" parameter.</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

export default Examples
