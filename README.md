# Brave Search SERP Scraper Assignment

## Overview

In this assignment, you will build a **web scraper for Brave Search** that:
1. Takes a search query as input
2. Fetches search results from Brave Search
3. Parses the response and extracts organic results
4. Returns structured data (title, URL, snippet for each result)

This assignment tests your ability to:
- **Investigate** how a website works (network requests, HTML structure)
- **Implement** HTTP requests with proper headers
- **Parse** HTML/responses to extract structured data
- **Handle errors** gracefully

**Time estimate:** 2-3 hours

---

## Your Task

### 1. Implement `scrape()` in `scraper.py`

```python
def scrape(query: str) -> str:
    """
    Fetch search results from Brave Search for the given query.

    Returns the raw HTML/response content.
    """
```

**Your job:**
- Go to https://search.brave.com and perform a search
- Figure out how to get the html for a specific query
- Return the raw response content

### 2. Implement `parse()` in `scraper.py`

```python
def parse(html: str, query: str = "") -> ParsedSerp:
    """
    Parse the raw HTML and extract search results.

    Returns a ParsedSerp containing a list of SerpResult objects.
    """
```

**Your job:**
- Analyze the HTML structure of Brave Search results
- Use a parser to extract:
  - **Title** of each result
  - **URL** of each result
  - **Snippet/description** of each result
- Return the first page of results (typically ~10 results)

---

## Expected Output

When you run `python -m serp_assignment.main`, you should see something like:

```
Query: "python web scraping"
Status: success
Results: 10

  #1: Some Title Here
      https://example.com/some-url
      This is the snippet or description text...

  #2: Another Result Title
      https://another-example.com/page
      Another snippet describing this result...

  ...
```

---

## Bonus Features (Optional)

If you finish early, consider adding:

- **Freshness filter** - results from past day/week/month/year
- **Country/region** - localized results
- **Safe search** - filter adult content
- **Result count** - configurable number of results

These parameters can be discovered by using Brave Search's UI filters and observing the network requests.

---

## Project Structure

```
serp_assignment/
├── __init__.py
├── models.py      # Pydantic models (provided)
├── errors.py      # Custom exceptions (provided)
├── scraper.py     # YOUR IMPLEMENTATION GOES HERE
└── main.py        # Entry point (provided)
```

---

## Running the Project

```bash
# Install dependencies
pip install -r requirements.txt

# Run the scraper (CLI)
python -m serp_assignment.main

# Or with a custom query
python -m serp_assignment.main "your search query here"
```

---

## API Server

Your implementation must also work as an API. A FastAPI server is provided.

### Starting the Server

```bash
uvicorn serp_assignment.api:app --reload --port 8000
```

### API Endpoints

**POST /search**

Search Brave and return results.

```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "python web scraping"}'
```

Response:
```json
{
  "query": "python web scraping",
  "results": [
    {
      "title": "Some Title",
      "url": "https://example.com",
      "snippet": "Description text...",
      "rank": 1
    }
  ],
  "status": "success",
  "error_message": null
}
```

**GET /health**

Health check endpoint.

```bash
curl http://localhost:8000/health
```

---

## Load Testing

A load test script is provided in `tests/load_test.py` to verify your implementation handles multiple requests.

### Running the Load Test

```bash
# 1. Start the API server (in one terminal)
uvicorn serp_assignment.api:app --port 8000

# 2. Run the load test (in another terminal)
python -m tests.load_test
```

### Load Test Options

```bash
python -m tests.load_test --help

Options:
  --url URL         API base URL (default: http://localhost:8000)
  --queries N       Number of queries to send (default: 1000)
  --concurrency N   Concurrent requests (default: 10)
```

### Example Output

```
Starting load test...
  API URL: http://localhost:8000
  Queries: 1000
  Concurrency: 10

  Progress: 100/1000 (10%)
  Progress: 200/1000 (20%)
  ...

============================================================
LOAD TEST RESULTS
============================================================

Total queries:        1000
Total time:           45.23s
Queries per second:   22.11

STATUS BREAKDOWN:
  Successful:         950 (95.0%)
  Failed:             50 (5.0%)
    - Blocked:        30
    - Parse errors:   10
    - Request errors: 5
    - Other errors:   5

RESPONSE TIMES:
  Average:            450.23ms
  Min:                120.45ms
  Max:                2340.12ms

RESULTS:
  Total results:      9500
  Avg per query:      10.0
```

---

## Evaluation Criteria

- **Investigation skills** - Did you correctly identify how Brave Search works?
- **Code quality** - Is the code clean, readable, and well-structured?
- **Error handling** - Does it handle failures gracefully?
- **Completeness** - Does it extract all required fields?

---

## Notes

- You may use `requests` and `beautifulsoup4` (already in requirements.txt)
- Do not use Brave Search's official API - this is a scraping exercise
- If you get blocked, consider what headers a real browser sends
- Make reasonable assumptions and document them in comments
