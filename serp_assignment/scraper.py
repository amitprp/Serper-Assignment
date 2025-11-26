"""
Brave Search Scraper

YOUR TASK: Implement the scrape() and parse() functions below.

See README.md for detailed instructions.
"""

import requests
from bs4 import BeautifulSoup

from .models import ParsedSerp, SerpResult
from .errors import RequestError, ParseError, BlockedError


def scrape(query: str) -> str:
    """
    Fetch search results from Brave Search for the given query.

    Args:
        query: The search query string.

    Returns:
        The raw HTML response content.

    Raises:
        RequestError: If the HTTP request fails.
        BlockedError: If the request is blocked (CAPTCHA, rate limit, etc.)

    TODO (your implementation):
        1. Investigate Brave Search using browser Developer Tools
        2. Identify the correct URL and required parameters
        3. Set appropriate headers (User-Agent, etc.)
        4. Make the HTTP request using the requests library
        5. Handle potential errors (connection, timeout, blocking)
        6. Return the raw HTML content
    """
    # ===== YOUR CODE HERE =====
    raise NotImplementedError("Implement the scrape() function")
    # ==========================


def parse(html: str, query: str = "") -> ParsedSerp:
    """
    Parse the raw HTML and extract search results.

    Args:
        html: The raw HTML content from Brave Search.
        query: The original search query (for reference).

    Returns:
        A ParsedSerp object containing the extracted results.

    Raises:
        ParseError: If parsing fails.

    TODO (your implementation):
        1. Use BeautifulSoup to parse the HTML
        2. Identify the HTML structure of search results (inspect in browser)
        3. Extract title, URL, and snippet for each result
        4. Create SerpResult objects with rank (1, 2, 3, ...)
        5. Return a ParsedSerp with all results
    """
    # ===== YOUR CODE HERE =====
    raise NotImplementedError("Implement the parse() function")
    # ==========================


def search(query: str) -> ParsedSerp:
    """
    High-level function that scrapes and parses in one call.

    This function is provided for convenience - it calls your
    scrape() and parse() implementations.

    Args:
        query: The search query string.

    Returns:
        A ParsedSerp object with the search results.
    """
    try:
        html = scrape(query)
        result = parse(html, query)
        result.status = "success"
        return result
    except BlockedError as e:
        return ParsedSerp(query=query, status="blocked", error_message=str(e))
    except RequestError as e:
        return ParsedSerp(query=query, status="request_error", error_message=str(e))
    except ParseError as e:
        return ParsedSerp(query=query, status="parse_error", error_message=str(e))
    except Exception as e:
        return ParsedSerp(query=query, status="error", error_message=str(e))
