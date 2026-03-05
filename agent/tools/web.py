import requests
from bs4 import BeautifulSoup
from ddgs import DDGS

from langchain_core.tools import tool

from utils import get_logger

# Module logger
logger = get_logger(__name__)


@tool
def web_search(query: str) -> str:
    """Search the web and return the top result URLs.

    Args:
        query: The search query string.
    """
    logger.info("Web search: %s", query)
    try:
        # Query DuckDuckGo for results
        results = DDGS().text(query, max_results=5, region="wt-wt")
        # Extract URLs from results
        urls = [r["href"] for r in results]
        return "\n".join(urls) if urls else "No results found."
    except Exception as e:
        return f"Search error: {e}"


@tool
def web_fetch(url: str) -> str:
    """Fetch a webpage and return its main text content.

    Args:
        url: The URL to fetch.
    """
    logger.info("Web fetch: %s", url)
    try:
        # Fetch page with browser-like headers
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")
        # Strip non-content tags
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        # Extract plain text
        text = soup.get_text(separator="\n", strip=True)
        return text[:5000]
    except Exception as e:
        return f"Fetch error: {e}"
