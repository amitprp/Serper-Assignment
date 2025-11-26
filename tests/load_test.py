"""
Load test for the Brave Search Scraper API.

Sends 1000 queries to the API and reports statistics.

Usage:
    1. Start the API server:
       uvicorn serp_assignment.api:app --port 8000

    2. Run this test:
       python -m tests.load_test

    Options:
       --url URL        API base URL (default: http://localhost:8000)
       --queries N      Number of queries to send (default: 1000)
       --concurrency N  Concurrent requests (default: 10)
"""

import argparse
import time
import random
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Optional


# Sample queries for testing
SAMPLE_QUERIES = [
    "python web scraping",
    "machine learning tutorial",
    "best programming languages 2024",
    "how to learn coding",
    "javascript frameworks",
    "data science projects",
    "cloud computing basics",
    "cybersecurity tips",
    "artificial intelligence news",
    "software engineering jobs",
    "react vs vue",
    "docker tutorial",
    "kubernetes basics",
    "git commands",
    "linux terminal commands",
    "sql database design",
    "mongodb tutorial",
    "api design best practices",
    "microservices architecture",
    "devops tools",
    "python fastapi",
    "web development trends",
    "mobile app development",
    "blockchain explained",
    "quantum computing basics",
    "rust programming language",
    "golang tutorial",
    "typescript vs javascript",
    "css flexbox guide",
    "html5 features",
    "node.js best practices",
    "django vs flask",
    "aws services overview",
    "azure cloud platform",
    "google cloud tutorial",
    "redis caching",
    "elasticsearch basics",
    "graphql vs rest",
    "websocket tutorial",
    "oauth2 explained",
    "jwt authentication",
    "unit testing python",
    "integration testing",
    "ci cd pipeline",
    "agile methodology",
    "scrum framework",
    "product management",
    "ux design principles",
    "figma tutorial",
    "tech startup ideas",
]


@dataclass
class QueryResult:
    """Result of a single query."""
    query: str
    status: str
    result_count: int
    response_time_ms: float
    error_message: Optional[str] = None


@dataclass
class Statistics:
    """Aggregated statistics from the load test."""
    total_queries: int = 0
    successful: int = 0
    failed: int = 0
    blocked: int = 0
    parse_errors: int = 0
    request_errors: int = 0
    other_errors: int = 0
    total_results: int = 0
    response_times: list[float] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        if self.total_queries == 0:
            return 0.0
        return (self.successful / self.total_queries) * 100

    @property
    def avg_response_time(self) -> float:
        if not self.response_times:
            return 0.0
        return sum(self.response_times) / len(self.response_times)

    @property
    def min_response_time(self) -> float:
        return min(self.response_times) if self.response_times else 0.0

    @property
    def max_response_time(self) -> float:
        return max(self.response_times) if self.response_times else 0.0

    @property
    def avg_results_per_query(self) -> float:
        if self.successful == 0:
            return 0.0
        return self.total_results / self.successful


def send_query(api_url: str, query: str) -> QueryResult:
    """Send a single query to the API."""
    start_time = time.time()

    try:
        response = requests.post(
            f"{api_url}/search",
            json={"query": query},
            timeout=30,
        )
        response_time_ms = (time.time() - start_time) * 1000

        if response.status_code != 200:
            return QueryResult(
                query=query,
                status="http_error",
                result_count=0,
                response_time_ms=response_time_ms,
                error_message=f"HTTP {response.status_code}",
            )

        data = response.json()
        return QueryResult(
            query=query,
            status=data.get("status", "unknown"),
            result_count=len(data.get("results", [])),
            response_time_ms=response_time_ms,
            error_message=data.get("error_message"),
        )

    except requests.exceptions.Timeout:
        return QueryResult(
            query=query,
            status="timeout",
            result_count=0,
            response_time_ms=(time.time() - start_time) * 1000,
            error_message="Request timed out",
        )
    except requests.exceptions.ConnectionError:
        return QueryResult(
            query=query,
            status="connection_error",
            result_count=0,
            response_time_ms=(time.time() - start_time) * 1000,
            error_message="Connection failed - is the server running?",
        )
    except Exception as e:
        return QueryResult(
            query=query,
            status="error",
            result_count=0,
            response_time_ms=(time.time() - start_time) * 1000,
            error_message=str(e),
        )


def generate_queries(n: int) -> list[str]:
    """Generate n queries by cycling through sample queries with variations."""
    queries = []
    for i in range(n):
        base_query = SAMPLE_QUERIES[i % len(SAMPLE_QUERIES)]
        # Add some variation to avoid caching
        if i >= len(SAMPLE_QUERIES):
            variation = i // len(SAMPLE_QUERIES)
            base_query = f"{base_query} {variation}"
        queries.append(base_query)
    return queries


def run_load_test(
    api_url: str,
    num_queries: int,
    concurrency: int,
) -> Statistics:
    """Run the load test and return statistics."""
    queries = generate_queries(num_queries)
    stats = Statistics()
    results: list[QueryResult] = []

    print(f"Starting load test...")
    print(f"  API URL: {api_url}")
    print(f"  Queries: {num_queries}")
    print(f"  Concurrency: {concurrency}")
    print()

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = {
            executor.submit(send_query, api_url, query): query
            for query in queries
        }

        completed = 0
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            completed += 1

            # Progress indicator
            if completed % 100 == 0 or completed == num_queries:
                print(f"  Progress: {completed}/{num_queries} ({completed*100//num_queries}%)")

    total_time = time.time() - start_time

    # Aggregate statistics
    for result in results:
        stats.total_queries += 1
        stats.response_times.append(result.response_time_ms)

        if result.status == "success":
            stats.successful += 1
            stats.total_results += result.result_count
        elif result.status == "blocked":
            stats.blocked += 1
            stats.failed += 1
        elif result.status == "parse_error":
            stats.parse_errors += 1
            stats.failed += 1
        elif result.status == "request_error":
            stats.request_errors += 1
            stats.failed += 1
        else:
            stats.other_errors += 1
            stats.failed += 1

    # Print results
    print()
    print("=" * 60)
    print("LOAD TEST RESULTS")
    print("=" * 60)
    print()
    print(f"Total queries:        {stats.total_queries}")
    print(f"Total time:           {total_time:.2f}s")
    print(f"Queries per second:   {stats.total_queries / total_time:.2f}")
    print()
    print("STATUS BREAKDOWN:")
    print(f"  Successful:         {stats.successful} ({stats.success_rate:.1f}%)")
    print(f"  Failed:             {stats.failed} ({100 - stats.success_rate:.1f}%)")
    print(f"    - Blocked:        {stats.blocked}")
    print(f"    - Parse errors:   {stats.parse_errors}")
    print(f"    - Request errors: {stats.request_errors}")
    print(f"    - Other errors:   {stats.other_errors}")
    print()
    print("RESPONSE TIMES:")
    print(f"  Average:            {stats.avg_response_time:.2f}ms")
    print(f"  Min:                {stats.min_response_time:.2f}ms")
    print(f"  Max:                {stats.max_response_time:.2f}ms")
    print()
    print("RESULTS:")
    print(f"  Total results:      {stats.total_results}")
    print(f"  Avg per query:      {stats.avg_results_per_query:.1f}")
    print()

    # Show some failed queries if any
    failed_results = [r for r in results if r.status != "success"]
    if failed_results:
        print("SAMPLE FAILURES (up to 5):")
        for r in failed_results[:5]:
            print(f"  [{r.status}] \"{r.query[:30]}...\" - {r.error_message}")
        print()

    return stats


def main():
    parser = argparse.ArgumentParser(description="Load test for Brave Search Scraper API")
    parser.add_argument("--url", default="http://localhost:8000", help="API base URL")
    parser.add_argument("--queries", type=int, default=1000, help="Number of queries")
    parser.add_argument("--concurrency", type=int, default=10, help="Concurrent requests")

    args = parser.parse_args()

    # Check if server is running
    try:
        response = requests.get(f"{args.url}/health", timeout=5)
        if response.status_code != 200:
            print(f"Error: Server at {args.url} is not healthy")
            return
    except requests.exceptions.ConnectionError:
        print(f"Error: Cannot connect to {args.url}")
        print("Make sure the server is running:")
        print("  uvicorn serp_assignment.api:app --port 8000")
        return

    run_load_test(args.url, args.queries, args.concurrency)


if __name__ == "__main__":
    main()
