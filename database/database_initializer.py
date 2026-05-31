import sqlite3
from pathlib import Path

class DatabaseInitializer:

    @staticmethod
    def initialize(db_path, schema_path):
        conn = sqlite3.connect(db_path)

        with open(schema_path, "r", encoding="utf-8") as f:
            conn.executescript(f.read())

        conn.commit()
        conn.close()