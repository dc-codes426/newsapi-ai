# NewsAPI AI - Intelligent News Search Actor

An AI-powered news search Actor that combines Claude AI with NewsAPI.org to provide intelligent, natural language news queries. Simply ask for news in plain English, and the AI agent will automatically find the most relevant articles for you.

## What Does This Actor Do?

This Actor uses Claude AI (Anthropic) to intelligently search and retrieve news articles based on your natural language queries. Instead of manually crafting complex search parameters, you can simply ask questions like:

- "What are the latest developments in artificial intelligence?"
- "Show me tech news from yesterday"
- "Top headlines about climate change"
- "News about Tesla from the past week"

The AI agent automatically:
- Interprets your query and determines the best search strategy
- Decides whether to search everything, top headlines, or specific sources
- Optimizes search parameters for maximum relevance
- Returns curated results with intelligent summaries

## Key Features

- **Natural Language Interface**: Ask for news the way you'd ask a person
- **Intelligent Query Optimization**: Claude AI determines optimal search parameters
- **Multiple Response Formats**: Get natural language summaries, structured data, or both
- **Multi-turn Conversations**: The agent maintains context within a single run
- **Automatic Pagination**: Retrieves and deduplicates results across multiple pages
- **BYOK (Bring Your Own Key)**: Use your own API keys to avoid rate limits

## Input Parameters

### Required

- **Query** (string): Your natural language question or search request
  - Example: "Latest AI developments in healthcare"
  - Example: "What happened in tech news yesterday?"

### Optional

- **NewsAPI Key** (string, secret): Your NewsAPI.org API key
  - Get a free key at https://newsapi.org/register
  - Free tier: 100 requests/day, 1-month history
  - If not provided, uses the Actor's default key (subject to shared rate limits)

- **Anthropic API Key** (string, secret): Your Anthropic API key for Claude AI
  - Get one at https://console.anthropic.com/
  - If not provided, uses the Actor's default key (subject to shared rate limits)

- **Response Format** (select): How to format the response
  - `both` (default): Natural language summary + structured article data
  - `natural`: Only natural language summary
  - `structured`: Only structured article data

- **Max Results** (integer): Maximum number of articles to return
  - Default: 10
  - Range: 1-100

## Output Format

The Actor outputs a dataset with the following structure:

```json
{
  "query": "Your original query",
  "response_format": "both",
  "response": "Natural language summary or final answer",
  "intermediate_responses": [
    "Step-by-step responses from the AI as it processes your query"
  ]
}
```

### Understanding the Output

- **response**: The final answer from Claude AI, which may include:
  - A natural language summary of findings
  - Structured article data (if response_format includes structured)
  - Both summary and articles (if response_format is "both")

- **intermediate_responses**: A list of Claude's thought process, showing:
  - Which tools the AI decided to use
  - Search results as they were retrieved
  - How the AI reasoned about your query

## Usage Examples

### Example 1: Simple News Query

**Input:**
```json
{
  "query": "What are the latest developments in artificial intelligence?"
}
```

**What Happens:**
1. Claude AI analyzes your query
2. Decides to search NewsAPI for recent AI news
3. Retrieves and filters relevant articles
4. Returns a summary with the most important developments

### Example 2: Specific Time Range

**Input:**
```json
{
  "query": "Show me tech news from yesterday",
  "maxResults": 5,
  "responseFormat": "structured"
}
```

**What Happens:**
1. AI interprets "yesterday" and calculates the date range
2. Searches for technology news from that specific day
3. Returns top 5 articles in structured format

### Example 3: Using Your Own API Keys

**Input:**
```json
{
  "query": "Top headlines about climate change",
  "newsApiKey": "your_newsapi_key_here",
  "anthropicApiKey": "your_anthropic_key_here",
  "responseFormat": "both"
}
```

**Benefit:**
- No shared rate limits
- More control over API usage
- Better for production use cases

## How It Works

1. **Query Processing**: Claude AI receives your natural language query
2. **Tool Selection**: The AI decides which NewsAPI endpoints to use:
   - `/everything`: For comprehensive searches across all articles
   - `/top-headlines`: For breaking news and top stories
   - `/sources`: For finding specific news sources
3. **Search Execution**: Multiple optimized queries are executed with automatic pagination
4. **Deduplication**: Results are deduplicated based on article URLs
5. **Response Generation**: Claude AI synthesizes findings into a coherent response

## API Keys & Rate Limits

### NewsAPI.org

- **Free Tier**: 100 requests/day, articles up to 1 month old
- **Paid Tiers**: Higher limits and access to older articles
- **Get a Key**: https://newsapi.org/register

### Anthropic Claude

- **Pay-as-you-go**: Based on tokens used (input + output)
- **Model Used**: claude-sonnet-4-5-20250929
- **Cost**: ~$3 per million input tokens, ~$15 per million output tokens
- **Get a Key**: https://console.anthropic.com/

### Using the Actor's Default Keys

If you don't provide your own API keys:
- The Actor uses shared default keys (if configured)
- You may hit rate limits if many users are running the Actor
- Best for testing and light usage
- For production, we recommend using your own keys

## Tips for Best Results

1. **Be Specific**: Include time ranges, topics, or regions in your query
   - Good: "Tech news about Apple from the past week"
   - Less Good: "Apple news"

2. **Use Natural Language**: The AI understands context and nuance
   - "What's happening with electric vehicles?" works great
   - No need for Boolean operators or complex syntax

3. **Specify Response Format**: Choose based on your needs
   - `natural`: Best for quick summaries and human-readable output
   - `structured`: Best for programmatic processing and data analysis
   - `both`: Best when you want both summary and raw data

4. **Adjust Max Results**: Balance completeness with processing time
   - 10-20 articles: Quick overview
   - 50-100 articles: Comprehensive analysis

## Limitations

- **NewsAPI Free Tier**: Limited to articles from the past month
- **Rate Limits**: Shared keys may hit limits during peak usage
- **Search Scope**: Results depend on NewsAPI's indexed sources
- **AI Interpretation**: Claude's understanding, while sophisticated, may occasionally misinterpret complex queries

## Troubleshooting

**"Missing NEWS_API_KEY" error**
- Provide your own NewsAPI key in the input, or
- Ensure the Actor's environment variables are configured

**"Missing ANTHROPIC_API_KEY" error**
- Provide your own Anthropic API key in the input, or
- Ensure the Actor's environment variables are configured

**Few or no results**
- Try broadening your query
- Check if the topic has recent news coverage
- Verify your NewsAPI key has sufficient quota

**Actor times out**
- Reduce `maxResults` parameter
- Simplify your query to be more specific

## Use Cases

- **Research**: Gather recent news on specific topics for research papers
- **Market Intelligence**: Monitor news about companies, industries, or competitors
- **Content Curation**: Find relevant articles for newsletters or content creation
- **Trend Analysis**: Track how topics evolve over time
- **News Aggregation**: Build custom news feeds based on specific interests

## Development & Local Usage

For developers who want to run this locally or contribute:

See [CLAUDE.md](./CLAUDE.md) for detailed development instructions including:
- Local setup with FastAPI backend
- React/Vite frontend for interactive testing
- Running tests with pytest
- API server configuration

## Support

- **Issues**: Report bugs or request features on the GitHub repository
- **NewsAPI Docs**: https://newsapi.org/docs
- **Anthropic Docs**: https://docs.anthropic.com/

## License

See LICENSE file for details.
