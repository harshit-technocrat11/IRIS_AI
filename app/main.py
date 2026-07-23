import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, status
from telegram import Update
from app.core.settings import settings
from app.bot.handlers import telegram_app
import uvicorn
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("IRIS-FastAPI")

WEBHOOK_PATH = f"/webhook/{settings.TELEGRAM_BOT_TOKEN}"
WEBHOOK_URL = f"{settings.APP_URL}{WEBHOOK_PATH}"


@asynccontextmanager
async def lifespan(app: FastAPI):

    await telegram_app.initialize()
    await telegram_app.bot.set_webhook(
        url=WEBHOOK_URL,
        allowed_updates=Update.ALL_TYPES,
    )
    logger.info(f"🚀 Registered Telegram Webhook at: {WEBHOOK_URL}")

    yield

    await telegram_app.bot.delete_webhook()
    await telegram_app.shutdown()
    logger.info("🛑 Telegram Webhook removed cleanly.")


app = FastAPI(title="IRIS AI Engine", lifespan=lifespan)


@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    """FastAPI webhook endpoint receiving push payloads from Telegram."""
    try:
        print("req: ", request)
        data = await request.json()
        
        print("data: ", data)
        update = Update.de_json(data, telegram_app.bot)
        await telegram_app.process_update(update)
        return Response(status_code=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error handling webhook update: {e}")
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
