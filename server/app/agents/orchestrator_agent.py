import logging
from agents import Agent, Runner, set_default_openai_key, trace
from app.core.settings import settings
from pathlib import Path
from agents.extensions.memory import AsyncSQLiteSession
from app.core.database import DB_PATH
from app.agents.search_specialist import search_specialist
from app.agents.email_agent import email_agent

logger = logging.getLogger("IRIS-Agent")


orchestrator_agent = Agent(
    name="Telegram Orchestrator",
    instructions=(
        "You are a helpful AI assistant for a Telegram bot. "
        "You are polite, concise, and helpful. "
        "Reason the user's query, and if required, you can use your tools"
    ),
    tools=[
        search_specialist.as_tool(
            tool_name="search_web",
            tool_description="Searches the internet for real-time news, facts, and current events.",
        ),
        email_agent.as_tool(
            tool_name="email_specialist",
            tool_description="functions:- search inboxes, read message threads, resolve contact names, and draft emails",
        ),
    ],
)


async def run_orchestrator_agent(user_prompt: str, session_id: str) -> str:

    """Executes prompt against IRIS Agent instance and returns text response.
    Args:
        user_prompt: The user's message text.
        session_id: Unique ID for the user (e.g., Telegram Chat ID).
    """ 

    session = AsyncSQLiteSession(session_id=session_id, db_path=DB_PATH)

    try:
        with trace("IRIS Agent Execution"): 
            result = await Runner.run(
                orchestrator_agent, 
                user_prompt, 
                session=session
            )

        print("orchestrator result: ",result.final_output)

        return result.final_output
    except Exception as e:
        logger.error(f"Error running IRIS agent: {e}")
        return "⚠️ I encountered an error processing your request."
