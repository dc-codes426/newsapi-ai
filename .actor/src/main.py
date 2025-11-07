"""Apify Actor entry point for NewsAPI AI."""

import asyncio
import os
from typing import Any, Dict

from apify import Actor
from anthropic import Anthropic

from src.intent.news_agent import NewsAgent
from src.api_client.news_client import NewsAPIClient


async def main() -> None:
    """Main entry point for the Apify Actor."""
    async with Actor:
        # Get input from Apify
        actor_input: Dict[str, Any] = await Actor.get_input() or {}

        # Extract parameters
        query = actor_input.get('query')
        if not query:
            await Actor.fail('Missing required parameter: query')
            return

        news_api_key = actor_input.get('newsApiKey') or os.getenv('NEWS_API_KEY')
        anthropic_api_key = actor_input.get('anthropicApiKey') or os.getenv('ANTHROPIC_API_KEY')
        response_format = actor_input.get('responseFormat', 'both')
        max_results = actor_input.get('maxResults', 10)

        # Validate required API keys
        if not news_api_key:
            await Actor.fail('Missing NEWS_API_KEY. Please provide it in input or environment variables.')
            return

        if not anthropic_api_key:
            await Actor.fail('Missing ANTHROPIC_API_KEY. Please provide it in input or environment variables.')
            return

        Actor.log.info(f'Processing query: {query}')
        Actor.log.info(f'Response format: {response_format}')
        Actor.log.info(f'Max results: {max_results}')

        try:
            # Initialize clients
            news_client = NewsAPIClient(api_key=news_api_key)
            anthropic_client = Anthropic(api_key=anthropic_api_key)
            news_agent = NewsAgent(
                anthropic_client=anthropic_client,
                news_api_client=news_client
            )

            # Process the query
            result = news_agent.process_request(
                user_prompt=query,
                session_id='apify-session'  # Single session for Apify runs
            )

            # Prepare output based on response format
            output = {
                'query': query,
                'response_format': response_format,
                'response': result.get('response', ''),
                'intermediate_responses': result.get('intermediate_responses', [])
            }

            # Push result to dataset
            await Actor.push_data(output)

            Actor.log.info(f'Successfully processed query.')

        except Exception as e:
            Actor.log.exception(f'Error processing query: {e}')
            await Actor.fail(f'Failed to process query: {str(e)}')
