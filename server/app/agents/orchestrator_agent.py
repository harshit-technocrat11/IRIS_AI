import logging
from agents import Agent, Runner, set_default_openai_key
from app.core.settings import settings
from pathlib import Path
from agents.extensions.memory import AsyncSQLiteSession
from app.core.database import DB_PATH

logger = logging.getLogger("IRIS-Agent")

OPENAI_API_KEY = settings.OPENAI_API_KEY
set_default_openai_key(OPENAI_API_KEY)

orchestrator_agent = Agent(
    name="Telegram Orchestrator",
    instructions=(
        "You are a helpful AI assistant for a Telegram bot. "
        "You are polite, concise, and helpful. "
        "You will soon have tools to help with tasks, but for now, just chat."
    ),
)


async def run_orchestrator_agent(user_prompt: str, session_id: str) -> str:

    """Executes prompt against IRIS Agent instance and returns text response.
    Args:
        user_prompt: The user's message text.
        session_id: Unique ID for the user (e.g., Telegram Chat ID).
    """ 

    session = AsyncSQLiteSession(session_id=session_id, db_path=DB_PATH)

    try:
        result = await Runner.run(orchestrator_agent, user_prompt, session=session)
        print("orchestrator result: ",result.final_output)

        return result.final_output
    except Exception as e:
        logger.error(f"Error running IRIS agent: {e}")
        return "⚠️ I encountered an error processing your request."
