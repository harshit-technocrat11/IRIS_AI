from agents import Agent
from app.tools.web_search_tools import perform_web_search
from app.schemas.web_search import WebSearchResponse
from app.guardrails.search_guards import search_guardrail


search_specialist = Agent(
    name="Web Search Specialist",
    instructions=(
        "You are an expert web researcher. "
        "1. Use the 'perform_web_search' tool to find up-to-date information. "
        "2. Synthesize the results into a clear, concise summary. "
        "3. Always cite sources by mentioning the domain (e.g., 'According to Reuters...'). "
        "4. If no results are found, state clearly that information is unavailable."
    ),
    tools=[perform_web_search],
    output_type=WebSearchResponse,  
    output_guardrails=[search_guardrail],  
)


