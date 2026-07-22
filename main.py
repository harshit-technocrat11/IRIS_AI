import os
import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from openai import AsyncOpenAI

# Load environment variables
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALLOWED_USER_ID = os.getenv("ALLOWED_TELEGRAM_USER_ID")

if ALLOWED_USER_ID:
    ALLOWED_USER_ID = int(ALLOWED_USER_ID)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("IRIS")

openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)


async def run_agent(user_message: str) -> str:
    """Simple Agent call that processes user prompt and returns response."""
    try:
        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are IRIS, a concise and intelligent executive AI assistant. "
                        "Keep your replies crisp, accurate, and helpful."
                    ),
                },
                {"role": "user", "content": user_message},
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Agent Execution Error: {e}")
        return "⚠️ Sorry, I encountered an issue processing your request."


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command."""
    user_id = update.effective_user.id
    if ALLOWED_USER_ID and user_id != ALLOWED_USER_ID:
        await update.message.reply_text("⛔ Access Denied.")
        return

    await update.message.reply_text(
        "👋 Hello! IRIS is online and connected to FastAPI. How can I assist you?"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    incoming_id = update.effective_user.id
    """Receives message, validates user, executes Agent, and replies back."""

    print(f"DEBUG -> Incoming ID: {incoming_id} (Type: {type(incoming_id)})")
    print(f"DEBUG -> Allowed ID:  {ALLOWED_USER_ID} (Type: {type(ALLOWED_USER_ID)})")
    user_id = update.effective_user.id
    if ALLOWED_USER_ID and user_id != ALLOWED_USER_ID:
        await update.message.reply_text("⛔ Access Denied.")
        return

    user_text = update.message.text
    logger.info(f"Received message from User [{user_id}]: {user_text}")

    # Show typing action in Telegram while Agent thinks
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )

    # Run Agent
    agent_response = await run_agent(user_text)

    # Reply back to Telegram
    await update.message.reply_text(agent_response)


# 4. Build Telegram Application
def build_telegram_app() -> Application:
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return app


telegram_app = build_telegram_app()


# 5. FastAPI Lifespan Manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start Telegram long-polling event loop
    await telegram_app.initialize()
    await telegram_app.start()
    await telegram_app.updater.start_polling()
    logger.info("🚀 IRIS FastAPI Server & Telegram Long Polling Active!")

    yield

    # Shutdown: Stop Telegram long-polling cleanly
    await telegram_app.updater.stop()
    await telegram_app.stop()
    await telegram_app.shutdown()
    logger.info("🛑 Services stopped.")


# 6. Initialize FastAPI App
app = FastAPI(title="IRIS AI Engine", lifespan=lifespan)


@app.get("/health")
async def health_check():
    return {"status": "online", "service": "IRIS Agent Backend"}
