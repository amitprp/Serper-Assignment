"""
Entry point for the Brave Search scraper.

Usage:
    python -m serp_assignment.main
    python -m serp_assignment.main "your query here"
"""

import sys
from .scraper import search
from .models import ParsedSerp


def print_results(result: ParsedSerp) -> None:
    """Pretty-print the search results."""
    print("=" * 60)
    print(f'Query: "{result.query}"')
    print(f"Status: {result.status}")

    if result.error_message:
        print(f"Error: {result.error_message}")
        return

    print(f"Results: {len(result.results)}")
    print()

    for r in result.results:
        print(f"  #{r.rank}: {r.title}")
        print(f"      {r.url}")
        if r.snippet:
            # Truncate long snippets for display
            snippet = r.snippet[:100] + "..." if len(r.snippet) > 100 else r.snippet
            print(f"      {snippet}")
        print()


def main() -> None:
    # Default query or take from command line
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "python web scraping"

    print(f"Searching Brave for: {query}\n")

    result = search(query)
    print_results(result)


if __name__ == "__main__":
    main()
