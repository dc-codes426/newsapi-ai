"""
News Agent module for AI-driven news search.

This module provides an intelligent agent that uses Anthropic's Claude
to process natural language queries and execute news searches.
"""

import json
from typing import Dict, Any
from dataclasses import asdict

from ..api_client.query_optimizer import QueryOptimizer
from ..api_client.models import UserQuery


class NewsAgent:
    """AI-driven news search agent using Anthropic tool use"""

    def __init__(self, anthropic_client, news_api_client):
        self.client = anthropic_client
        self.news_client = news_api_client
        self.conversation_history = {}
        # Define available tools
        self.tools = [
            {
                "name": "optimize_queries",
                "description": "Generate optimized search queries from natural language input. Use this when the user provides semantic/natural language requests that need to be converted into structured search parameters.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "user_input": {
                            "type": "string",
                            "description": "The natural language search request from the user"
                        }
                    },
                    "required": ["user_input"]
                }
            },
            {
                "name": "search_everything",
                "description": "Search historical news articles using the /everything endpoint. Supports full-text search with date ranges, language filters, domains, etc. Use this for your searches.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "q": {
                            "type": "string",
                            "description": "Search query (required)"
                        },
                        "searchIn": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Where to search: title, description, content"
                        },
                        "sources": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "News source IDs to include"
                        },
                        "domains": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Domains to include (e.g., bbc.co.uk)"
                        },
                        "excludeDomains": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Domains to exclude"
                        },
                        "from_date": {
                            "type": "string",
                            "description": "Start date in ISO format"
                        },
                        "to_date": {
                            "type": "string",
                            "description": "End date in ISO format"
                        },
                        "languages": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "ISO-639-1 language codes"
                        },
                        "sortBy": {
                            "type": "string",
                            "enum": ["relevancy", "popularity", "publishedAt"],
                            "description": "Sort order"
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of results to return"
                        }
                    },
                    "required": ["q"]
                }
            },
            {
                "name": "search_top_headlines",
                "description": "Get current top headlines using the /top-headlines endpoint. Use this for breaking news and current events.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "q": {
                            "type": "string",
                            "description": "Search query (optional)"
                        },
                        "countries": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "ISO 3166-1 alpha-2 country codes"
                        },
                        "categories": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Categories: business, entertainment, general, health, science, sports, technology"
                        },
                        "sources": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "News source IDs"
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of results"
                        }
                    }
                }
            },
            {
                "name": "get_sources",
                "description": "Get available news sources. Use this when users want to know what sources are available, or to filter sources by category/language/country.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "categories": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Filter by categories"
                        },
                        "languages": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Filter by languages"
                        },
                        "countries": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Filter by countries"
                        }
                    }
                }
            }
        ]

    def process_request(self, user_prompt: str, session_id: str = None) -> Dict[str, Any]:
        """
        Process a user request using AI-driven tool selection.
        The AI decides which tools to call and how to use them.

        Returns all intermediate responses from Claude, including:
        - Text responses (clarifying questions, explanations, etc.)
        - Tool usage and results
        - Final summary
        """
        if session_id:
            messages = self.conversation_history.get(session_id, [])
            messages.append({
                "role": "user",
                "content": user_prompt
            })
        else:
            messages = [{"role": "user", "content": user_prompt}]

        # Collect all intermediate responses
        intermediate_responses = []

        # Keep calling tools until AI is done
        while True:
            response = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=4096,
                tools=self.tools,
                messages=messages
            )

            # Extract any text from this response (even if it also uses tools)
            response_text = ""
            for block in response.content:
                if hasattr(block, "text"):
                    response_text += block.text

            # If there's text, save it as an intermediate response
            if response_text.strip():
                intermediate_responses.append(response_text)

            # Check if AI wants to use tools
            if response.stop_reason == "tool_use":
                # Process each tool call
                tool_results = []
                for content_block in response.content:
                    if content_block.type == "tool_use":
                        tool_name = content_block.name
                        tool_input = content_block.input

                        # Execute the tool
                        result = self._execute_tool(tool_name, tool_input)

                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": content_block.id,
                            "content": json.dumps(result)
                        })

                # Add assistant response and tool results to conversation
                messages.append({"role": "assistant", "content": response.content})
                messages.append({"role": "user", "content": tool_results})

                # Continue the loop to get Claude's response to the tool results

            # AI is done, return all responses
            elif response.stop_reason == "end_turn":
                # Combine all intermediate responses
                final_response = "\n\n".join(intermediate_responses) if intermediate_responses else ""

                # Update conversation history if session_id provided
                if session_id:
                    messages.append({"role": "assistant", "content": response.content})
                    self.conversation_history[session_id] = messages

                return {
                    "response": final_response,
                    "intermediate_responses": intermediate_responses,
                    "messages": messages  # Full conversation history
                }

    def _execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool and return results"""

        if tool_name == "optimize_queries":
            optimizer = QueryOptimizer()
            queries = optimizer.optimize_query(tool_input["user_input"])
            return {
                "queries": [asdict(q) for q in queries]
            }

        elif tool_name == "search_everything":
            # Create UserQuery from tool input
            query = UserQuery(**tool_input)
            result = self.news_client.search_everything(query)
            return {
                "status": result["status"],
                "total_results": result["totalResults"],
                "articles": result["articles"][:10]  # Limit for context
            }

        elif tool_name == "search_top_headlines":
            query = UserQuery(**tool_input)
            result = self.news_client.search_top_headlines(query)
            return {
                "status": result["status"],
                "total_results": result["totalResults"],
                "articles": result["articles"][:10]
            }

        elif tool_name == "get_sources":
            query = UserQuery(**tool_input)
            result = self.news_client.get_sources(query)
            return {
                "status": result["status"],
                "sources": result["sources"]
            }

        else:
            raise ValueError(f"Unknown tool: {tool_name}")

