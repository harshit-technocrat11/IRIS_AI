import logging
from agents import Agent, Runner, set_default_openai_api
from app.core.settings import settings

logger = logging.getLogger("IRIS-Agent")

OPENAI_API_KEY = settings.OPENAI_API_KEY
set_default_openai_api(OPENAI_API_KEY)

# Initialize IRIS Agent using OpenAI Agents SDK
iris_agent = Agent(
    
    name="IRIS Executive Assistant",
    instructions=(
        "You are IRIS, an executive AI assistant. "
        "Keep your replies crisp, direct, professional, and well-structured."
    ),
    model="gpt-4o-mini",
)


async def run_iris_agent(user_prompt: str) -> str:
    """Executes prompt against IRIS Agent instance and returns text response."""
    try:
        result = await Runner.run(iris_agent, user_prompt)
        return result.final_output
    except Exception as e:
        logger.error(f"Error running IRIS agent: {e}")
        return "⚠️ I encountered an error processing your request."
