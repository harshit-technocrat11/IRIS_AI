import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from app.core.settings import settings
from app.agents.iris_agent import run_iris_agent

logger = logging.getLogger("IRIS-Telegram")

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, Update
from telegram.ext import ContextTypes
from app.core.settings import settings


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends start greeting with Mini App voice call button."""
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📞 Call IRIS (Live Duplex)",
                    web_app=WebAppInfo(url=f"{settings.APP_URL}/call"),
                )
            ]
        ]
    )
    await update.message.reply_text(
        "⚡ *IRIS AI Engine Ready*\nTap below to start a live voice call or send a text message.",
        reply_markup=keyboard,
        parse_mode="Markdown",
    )


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command with user access control."""
    if update.effective_user.id != settings.ALLOWED_TELEGRAM_USER_ID:
        await update.message.reply_text("⛔ Access Denied.")
        return

    await update.message.reply_text(
        "👋 **IRIS Webhook Active!**\n"
        "Connected via OpenAI Agents SDK & FastAPI Webhooks. How can I assist you today?",
        parse_mode="Markdown",
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Processes incoming text, checks security allowlist, and executes agent."""
    user_id = update.effective_user.id
    if user_id != settings.ALLOWED_TELEGRAM_USER_ID:
        logger.warning(f"Blocked unauthorized access attempt from ID: {user_id}")
        await update.message.reply_text("⛔ Access Denied.")
        return

    user_text = update.message.text
    logger.info(f"Received message from User [{user_id}]: {user_text}")

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )

    agent_response = await run_iris_agent(user_text)

    await update.message.reply_text(agent_response)


def build_telegram_app() -> Application:
    """Constructs and returns the python-telegram-bot application."""
    app = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return app


telegram_app = build_telegram_app()
