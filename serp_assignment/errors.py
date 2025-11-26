class ScraperError(Exception):
    """Base exception for scraper errors."""


class RequestError(ScraperError):
    """Failed to make the HTTP request."""


class ParseError(ScraperError):
    """Failed to parse the response."""


class BlockedError(ScraperError):
    """Request was blocked (CAPTCHA, rate limit, etc.)."""
