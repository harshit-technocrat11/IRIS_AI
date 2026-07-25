import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, status, Header, HTTPException
from telegram import Update
from app.core.settings import settings
from app.bot.handlers import telegram_app
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from livekit.api import AccessToken, VideoGrants
from pathlib import Path
from fastapi.staticfiles import StaticFiles
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("IRIS-FastAPI")

WEBHOOK_SECRET = settings.TELEGRAM_WEBHOOK_SECRET
WEBHOOK_PATH = f"/webhook/{WEBHOOK_SECRET}"
WEBHOOK_URL = f"{settings.APP_URL}{WEBHOOK_PATH}"


@asynccontextmanager
async def lifespan(app: FastAPI):

    await telegram_app.initialize()

    await telegram_app.bot.set_webhook(
        url=WEBHOOK_URL,
        allowed_updates=Update.ALL_TYPES,
        secret_token=WEBHOOK_SECRET,
        drop_pending_updates=True,
    )

    logger.info(f"🚀 Registered Telegram Webhook at: {WEBHOOK_URL}")

    yield

    await telegram_app.bot.delete_webhook()
    await telegram_app.shutdown()
    logger.info("🛑 Telegram Webhook removed cleanly.")


app = FastAPI(title="IRIS AI Engine", lifespan=lifespan)


@app.post(WEBHOOK_PATH)
async def telegram_webhook(
    request: Request, x_telegram_bot_api_secret_token: str | None = Header(default=None)
):
    """
    FastAPI webhook endpoint receiving push payloads from Telegram.
    🔒 Validates the secret token before processing.
    """

    if x_telegram_bot_api_secret_token != WEBHOOK_SECRET:
        logger.warning(f"⚠️ Invalid secret token from {request.client.host}")
        raise HTTPException(status_code=403, detail="Invalid secret token")

    try:
        data = await request.json()
        update = Update.de_json(data, telegram_app.bot)
        await telegram_app.process_update(update)
        return Response(status_code=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error handling webhook update: {e}", exc_info=True)

        return Response(status_code=status.HTTP_200_OK)


@app.get("/health")
async def health_check():
    return {"status": "ok", "mode": "webhook", "engine": "OpenAI Agents SDK"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=os.environ.get("PORT", 8000),
        reload=True,
    )
