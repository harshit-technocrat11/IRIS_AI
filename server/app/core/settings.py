import sys
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from pydantic import ValidationError

load_dotenv(override=True)


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    OPENAI_API_KEY: str
    ALLOWED_TELEGRAM_USER_ID: int
    TELEGRAM_WEBHOOK_SECRET: str
    APP_URL: str
    LIVEKIT_URL: str
    LIVEKIT_API_SECRET: str
    LIVEKIT_API_KEY: str
    TAVILY_API_KEY:str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

try:
    settings = Settings()
except ValidationError as e:
    print("❌ Error: Missing required environment variables in .env file!\n")
    print(e)
    sys.exit(1)

print("Checking Environment Configuration...\n")

settings_dict = settings.model_dump()

for key, value in settings_dict.items():
  
    if value is not None and str(value).strip() != "":
        if key == "OPENAI_API_KEY":
            print("✅yes openai key exists")
        else:
            print(f"✅ {key} exists")
    else:
        print(f"❌ {key} is missing or empty!")
