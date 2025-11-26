from typing import Optional
from pydantic import BaseModel, Field


class SerpResult(BaseModel):
    """A single search result."""

    title: str = Field(description="The title of the search result")
    url: str = Field(description="The URL of the search result")
    snippet: str = Field(default="", description="The snippet/description text")
    rank: int = Field(description="Position in search results (1-indexed)")


class ParsedSerp(BaseModel):
    """Parsed search engine results page."""

    query: str = Field(description="The original search query")
    results: list[SerpResult] = Field(default_factory=list, description="List of organic results")
    status: str = Field(default="unknown", description="Status: success, error, etc.")
    error_message: Optional[str] = Field(default=None, description="Error message if failed")
