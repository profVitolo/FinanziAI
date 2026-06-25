from pathlib import Path

TITLE = "FinanziAI",
DESCRIPTION = "AI-Assisted Investment Analysis",
VERSION = "0.1.2"
    
ROOT_DIR = Path(__file__).resolve().parent
DB_PATH = ( ROOT_DIR / "database" / "vault.db" )
SCHEMA_PATH = (ROOT_DIR / "database" / "init_db.sql" )

BASE_CURRENCY = "EUR"
BOOTSTRAP_DAYS = 90