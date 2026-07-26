from pathlib import Path
import os

CURRENT_FILE = Path(__file__).resolve()

SERVER_ROOT = CURRENT_FILE.parent.parent.parent

DB_PATH = SERVER_ROOT / "app" / "database" / "agent_memory.db"

DB_PATH.parent.mkdir(parents=True, exist_ok=True)

print(f"✅ Database path resolved to: {DB_PATH}")
