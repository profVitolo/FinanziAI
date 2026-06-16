import sqlite3
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
from config import DB_PATH, SCHEMA_PATH

class DatabaseManager:

    def __init__(self, db_path=DB_PATH, schema_path=SCHEMA_PATH):
        self.db_path = db_path
        self.schema_path = schema_path
        self.conn = None
        
        if not Path(self.db_path).exists():
            self.initialize()

    def initialize(self):
        if self.schema_path is None:
            return

        conn = sqlite3.connect(self.db_path)

        with open(self.schema_path, "r", encoding="utf-8") as f:
            conn.executescript(f.read())

        conn.commit()
        conn.close()

    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row

        return self.conn

    def begin_transaction(self):
        self.connect()
        self.conn.execute("BEGIN")

    def commit(self):
        if self.conn:
            self.conn.commit()

    def rollback(self):
        if self.conn:
            self.conn.rollback()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None