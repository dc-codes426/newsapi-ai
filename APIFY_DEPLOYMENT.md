# Apify Actor Deployment Guide

This document explains how to deploy NewsAPI AI as an Apify Actor while maintaining the existing FastAPI web application functionality.

## Architecture Overview

The codebase now supports **two deployment modes** from the same source:

### 1. Web App Mode (Existing)
- Entry point: `src/api_server/main.py`
- Framework: FastAPI + React frontend
- Deployment: Railway, Render, Fly.io, etc.
- Usage: HTTP API endpoints

### 2. Apify Actor Mode (New)
- Entry point: `src/actor_main.py`
- Framework: Apify SDK
- Deployment: Apify platform
- Usage: MCP-discoverable tool for AI agents

**Both modes share the same core logic**: `NewsAgent`, `NewsAPIClient`, and configuration.

## Prerequisites

### 1. Install Apify CLI

```bash
npm install -g apify-cli
```

### 2. Create Apify Account

Sign up at https://apify.com/

### 3. Login to Apify CLI

```bash
apify login
```

This will open your browser for authentication.

## Local Testing

### 1. Install Dependencies

```bash
conda activate newsapi-ai
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create `.env` file with:

```bash
ANTHROPIC_API_KEY=your_anthropic_key
NEWS_API_KEY=your_newsapi_key
```

### 3. Run Actor Locally

```bash
apify run
```

Or test with custom input:

```bash
apify run -i '{"query": "Latest AI news", "responseFormat": "both", "maxResults": 5}'
```

### 4. Check Output

After the run completes, view the dataset:

```bash
cat ./apify_storage/datasets/default/000000001.json
```

## Deployment to Apify Platform

### Option 1: Deploy via CLI

```bash
# Initialize (first time only)
apify init

# Push to Apify
apify push
```

### Option 2: Deploy via GitHub Integration

1. Push your code to GitHub
2. Go to Apify Console → Actors → Create New
3. Select "Import from GitHub"
4. Connect your repository
5. Select branch and .actor directory
6. Click "Build"

## Configuration

### Environment Variables (Apify Platform)

In the Apify Console, go to your Actor → Settings → Environment Variables:

```
ANTHROPIC_API_KEY=your_anthropic_key
NEWS_API_KEY=your_newsapi_key
```

**Security Note**: These are fallback keys. Users can provide their own keys in the Actor input to avoid rate limits.

### Actor Settings

Recommended settings in Apify Console:

- **Memory**: 512 MB (minimum) to 2048 MB (maximum)
- **Timeout**: 300 seconds (5 minutes)
- **Build tag**: `latest`

## Usage

### Via Apify Console

1. Go to your Actor in Apify Console
2. Click "Try it"
3. Fill in the input:
   ```json
   {
     "query": "What are the latest developments in AI?",
     "responseFormat": "both",
     "maxResults": 10
   }
   ```
4. Click "Start"

### Via API

```bash
curl -X POST https://api.apify.com/v2/acts/YOUR_USERNAME~newsapi-ai/runs \
  -H "Authorization: Bearer YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Latest tech news",
    "responseFormat": "both"
  }'
```

### Via MCP (Model Context Protocol)

Once deployed, AI agents (Claude Desktop, VS Code Copilot, Cursor) can discover and use your Actor:

1. **Setup MCP connection** to Apify:
   ```json
   {
     "mcpServers": {
       "apify": {
         "url": "https://mcp.apify.com"
       }
     }
   }
   ```

2. **AI agents can now**:
   - Search for "newsapi-ai" Actor
   - Add it as a tool dynamically
   - Call it when users ask about news

Example conversation:
```
User: "What's the latest news about quantum computing?"
AI: [Discovers NewsAPI AI Actor via MCP]
AI: [Calls Actor with query]
AI: "Here are the latest developments in quantum computing..." [with results]
```

## File Structure

```
newsapi-ai/
├── .actor/                      # Apify Actor configuration
│   ├── actor.json              # Actor metadata
│   ├── INPUT_SCHEMA.json       # Input schema for Apify UI
│   ├── Dockerfile              # Actor runtime
│   └── README.md               # Apify Store listing
├── src/
│   ├── actor_main.py           # NEW: Apify entry point
│   ├── api_server/
│   │   └── main.py             # Existing: FastAPI entry point
│   ├── api_client/             # Shared: NewsAPI client
│   ├── intent/                 # Shared: NewsAgent
│   └── config/                 # Shared: Configuration
├── requirements.txt            # Updated with apify SDK
└── APIFY_DEPLOYMENT.md         # This file
```

## Dual Deployment Strategy

You can deploy **both** simultaneously:

### Web App Deployment (Railway/Render/Fly.io)
```bash
# Deploy FastAPI + React
# Uses: src/api_server/main.py
# Command: uvicorn src.api_server.main:app --host 0.0.0.0 --port 8500
```

### Apify Actor Deployment
```bash
# Deploy to Apify
apify push
# Uses: src/actor_main.py
# Command: python -m src.actor_main
```

## Benefits of Dual Deployment

1. **Web App**: Direct HTTP API access, React frontend, traditional web hosting
2. **Apify Actor**: MCP discoverability, AI agent integration, managed infrastructure
3. **Same Codebase**: Single source of truth, shared logic, easier maintenance

## API Keys & Rate Limits

### Shared Keys (Environment Variables)
- Set in Apify Console → Environment Variables
- Used as fallback when user doesn't provide keys
- Subject to rate limits shared across all Actor runs

### User-Provided Keys (Input Parameters)
- Users can provide their own API keys in Actor input
- Recommended for high-volume usage
- Avoids shared rate limits

```json
{
  "query": "Latest news",
  "newsApiKey": "user_newsapi_key",
  "anthropicApiKey": "user_anthropic_key"
}
```

## Monitoring & Debugging

### View Logs
In Apify Console → Runs → Select a run → Log

### Check Dataset
In Apify Console → Storage → Datasets → Default

### Local Debugging
```bash
# Run with verbose logging
apify run --verbose

# Check local storage
ls -la ./apify_storage/datasets/default/
```

## Publishing to Apify Store

Once tested and stable:

1. Go to Apify Console → Your Actor → Publication
2. Fill in:
   - Title: "NewsAPI AI"
   - Description: (from .actor/README.md)
   - Categories: AI, News, Search
   - SEO title and meta description
3. Add screenshots/demo video
4. Submit for review

## Troubleshooting

### "Missing API key" error
- Check environment variables in Apify Console
- Or provide keys in Actor input

### Memory errors
- Increase memory allocation in Actor settings
- Recommended: 512 MB minimum

### Timeout errors
- Increase timeout in Actor settings
- Reduce maxResults in input

### Build failures
- Check Dockerfile syntax
- Verify requirements.txt dependencies
- Review build logs in Apify Console

## Support

- GitHub Issues: [Your repo URL]
- Apify Discord: https://discord.com/invite/jyEM2PRvMU
- Documentation: https://docs.apify.com/

---

**Next Steps**: Deploy to Apify and test with MCP integration!
