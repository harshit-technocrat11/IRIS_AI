from pathlib import Path
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
import os


DATABASE_URL = "sqlite+aiosqlite:////app/database/agent_memory.db"

engine = create_async_engine(DATABASE_URL, echo=False)
async_sessionmaker = async_sessionmaker(engine, class_=AsyncSession,expire_on_commit=False)

# intialize DB connection
async def init_db():
    """Call this during FastAPI lifespan startup to ensure pending_approvals exists."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


CURRENT_FILE = Path(__file__).resolve()

SERVER_ROOT = CURRENT_FILE.parent.parent.parent

DB_PATH = SERVER_ROOT / "app" / "database" / "agent_memory.db"

DB_PATH.parent.mkdir(parents=True, exist_ok=True)

print(f"✅ Database path resolved to: {DB_PATH}")
