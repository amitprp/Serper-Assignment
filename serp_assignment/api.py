"""
FastAPI server for the Brave Search scraper.

Usage:
    uvicorn serp_assignment.api:app --reload

Then POST to http://localhost:8000/search with JSON body: {"query": "your search"}
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .scraper import search
from .models import ParsedSerp


app = FastAPI(
    title="Brave Search Scraper API",
    description="A simple API to scrape Brave Search results",
    version="1.0.0",
)


class SearchRequest(BaseModel):
    """Request body for the search endpoint."""
    query: str


@app.post("/search", response_model=ParsedSerp)
def search_endpoint(request: SearchRequest) -> ParsedSerp:
    """
    Search Brave and return parsed results.

    Args:
        request: JSON body with "query" field.

    Returns:
        ParsedSerp with search results or error info.
    """
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    result = search(request.query.strip())
    return result


@app.get("/health")
def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}
