from pydantic_settings import BaseSettings , SettingsConfigDict
from dotenv import load_dotenv
load_dotenv(override=True)

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    OPENAI_API_KEY: str
    ALLOWED_TELEGRAM_USER_ID: int
    APP_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()