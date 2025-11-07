"""
Apify Actor entry point for NewsAPI AI.

This module allows NewsAPI AI to run as an Apify Actor, making it discoverable
and usable by AI agents through Apify's MCP (Model Context Protocol) integration.

The same core logic from the FastAPI server is reused here.
"""

import asyncio
import logging
import os
from typing import Dict, Any, Optional

from apify import Actor
from anthropic import Anthropic

from .api_client import NewsAPIClient
from .intent.news_agent import NewsAgent
from .config import setup_logging


async def main() -> None:
    """
    Main Apify Actor function.

    Reads input from Apify, processes the query using NewsAgent,
    and saves results to the default dataset.
    """
    async with Actor:
        # Setup logging
        setup_logging(log_level="INFO", log_file=None)
        logger = logging.getLogger(__name__)

        # Get input from Apify
        actor_input = await Actor.get_input() or {}
        Actor.log.info(f'Received input: {actor_input}')

        # Extract parameters
        query = actor_input.get('query')
        if not query:
            Actor.log.error('Missing required parameter: query')
            raise ValueError("Missing required parameter: query")

        response_format = actor_input.get('responseFormat', 'both')
        max_results = actor_input.get('maxResults', 10)

        # Get API keys (from input or environment)
        anthropic_key = actor_input.get('anthropicApiKey') or os.getenv('ANTHROPIC_API_KEY')
        news_api_key = actor_input.get('newsApiKey') or os.getenv('NEWS_API_KEY')

        if not anthropic_key:
            Actor.log.error('Missing ANTHROPIC_API_KEY')
            await Actor.fail('Missing ANTHROPIC_API_KEY. Please provide it in input or environment.')
            return

        if not news_api_key:
            Actor.log.error('Missing NEWS_API_KEY')
            await Actor.fail('Missing NEWS_API_KEY. Please provide it in input or environment.')
            return

        try:
            # Initialize clients
            Actor.log.info('Initializing AI clients...')
            anthropic_client = Anthropic(api_key=anthropic_key)
            news_client = NewsAPIClient(api_key=news_api_key)

            # Initialize agent
            news_agent = NewsAgent(anthropic_client, news_client)
            Actor.log.info('NewsAgent initialized')

            # Process the query
            Actor.log.info(f'Processing query: {query[:100]}...')
            result = news_agent.process_request(
                user_prompt=query,
                session_id="actor-session"  # Single session for Actor runs
            )

            # Extract results
            natural_response = result.get("response", "")
            articles_data = _extract_articles_from_messages(result.get("messages", []))

            # Build output based on format
            output = {
                "query": query,
                "format": response_format
            }

            if response_format in ["natural", "both"]:
                output["response"] = natural_response

            if response_format in ["structured", "both"] and articles_data:
                output["articles"] = articles_data["articles"][:max_results]
                output["total_results"] = articles_data.get("total_results", 0)

            # Save to default dataset
            Actor.log.info(f'Saving results to dataset...')
            await Actor.push_data(output)

            Actor.log.info('Actor completed successfully')

        except Exception as e:
            Actor.log.exception(f'Error processing query: {e}')
            await Actor.fail(f'Error processing query: {str(e)}')

        finally:
            # Cleanup
            if news_client:
                news_client.close()


def _extract_articles_from_messages(messages: list) -> Optional[Dict[str, Any]]:
    """
    Extract article data from conversation messages.

    Looks for tool results in the conversation that contain article data.

    Args:
        messages: List of conversation messages

    Returns:
        Dictionary with articles and total_results, or None if no articles found
    """
    import json

    articles = []
    total_results = 0

    for message in messages:
        if message.get("role") != "user":
            continue

        content = message.get("content", [])
        if not isinstance(content, list):
            continue

        for item in content:
            if not isinstance(item, dict) or item.get("type") != "tool_result":
                continue

            # Parse the tool result content
            try:
                tool_content = item.get("content", "")
                if isinstance(tool_content, str):
                    tool_data = json.loads(tool_content)
                else:
                    tool_data = tool_content

                # Check if this result contains articles
                if "articles" in tool_data:
                    articles.extend(tool_data["articles"])
                    total_results = max(total_results, tool_data.get("total_results", 0))

            except (json.JSONDecodeError, Exception):
                continue

    if articles:
        return {
            "articles": articles,
            "total_results": total_results
        }

    return None


# Entry point when running as module
if __name__ == '__main__':
    asyncio.run(main())
