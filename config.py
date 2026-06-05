from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
DB_PATH = ( ROOT_DIR / "database" / "vault.db" )
SCHEMA_PATH = (ROOT_DIR / "database" / "init_db.sql" )