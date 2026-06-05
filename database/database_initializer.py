import sqlite3
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
from config import DB_PATH, SCHEMA_PATH

class DatabaseInitializer:

    @staticmethod
    def initialize(db_path=DB_PATH, schema_path=SCHEMA_PATH):
        conn = sqlite3.connect(db_path)

        with open(schema_path, "r", encoding="utf-8") as f:
            conn.executescript(f.read())

        conn.commit()
        conn.close()