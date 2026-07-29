from agents import function_tool
from app.schemas.web_search import WebSearchResponse, SearchResultItem
from tavily import TavilyClient
from app.core.settings import settings
import logging

logger = logging.getLogger(__name__)

client = TavilyClient(api_key=settings.TAVILY_API_KEY)


def clean_text(text: str, max_length: int = 150) -> str:
    """Truncates text, removes newlines, and ensures safe length for LLM context."""
    if not text:
        return "No description available."

    clean = " ".join(text.split())

    if len(clean) > max_length:
        return clean[:max_length].rsplit(" ", 1)[0] + "..."
    return clean


@function_tool
def perform_web_search(query: str) -> WebSearchResponse:
    """
    Searches the web for real-time information.
    Use this for news, current events, or facts not in your training data.
    Returns a concise, cleaned summary of top 5 results.
    """
    logger.info(f"🔍 Searching web for: {query}")

    try:
       
        raw_data = client.search(
            query=query,
            search_depth="basic",
            max_results=5,
            include_answer=False,  
            include_raw_content=False,  
        )

        if not raw_data or "results" not in raw_data:
            return WebSearchResponse(
                query=query, results=[], summary="No results found."
            )

        items = []
        for r in raw_data["results"]:
            if not r.get("url") or not r.get("title"):
                continue

       
            clean_title = clean_text(r.get("title", ""), max_length=60)
            clean_snippet = clean_text(r.get("content", ""), max_length=150)

            items.append(
                SearchResultItem(title=clean_title, url=r["url"], snippet=clean_snippet)
            )

        count = len(items)
        if count == 0:
            summary = "No relevant results found."
        elif count == 1:
            summary = f"Found 1 result: {items[0].title}."
        else:
            top_sources = ", ".join([item.title for item in items[:2]])
            summary = f"Found {count} results. Top sources: {top_sources}."

            print(
                    "fetched results: ",
                    WebSearchResponse(
                        query=query,
                        results=items,
                        summary=summary,
                    ),
            )

        return WebSearchResponse(query=query, results=items, summary=summary)

    except Exception as e:
        logger.error(f"❌ Web Search Tool Failed: {str(e)}")
        return WebSearchResponse(
            query=query,
            results=[],
            summary=f"Search failed due to a technical error: {str(e)[:50]}...",
        )

