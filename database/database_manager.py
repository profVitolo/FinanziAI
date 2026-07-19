import sqlite3
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
from config import DB_PATH, SCHEMA_PATH, LAST_USED

class DatabaseManager:
    
    if LAST_USED.exists() and LAST_USED.stat().st_size > 0:
        try:
            current_db_path = Path(LAST_USED.read_text(encoding="utf-8").strip())
        except Exception:
            current_db_path = DB_PATH
    else:
        current_db_path = DB_PATH

    def __init__(self, db_path=None, schema_path=SCHEMA_PATH):
        self.db_path = db_path or DatabaseManager.current_db_path
        self.schema_path = schema_path
        self.conn = None
        
        if not Path(self.db_path).exists():
            self.initialize()

    def initialize(self, db_path=None):
        if self.schema_path is None:
            return

        db_path = db_path or self.db_path
        
        conn = sqlite3.connect(db_path)

        with open(self.schema_path, "r", encoding="utf-8") as f:
            conn.executescript(f.read())

        conn.commit()
        conn.close()

    def connect(self):
        if self.conn is None:
            print(f"Opening database {self.db_path}")
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
            print(f"Closing database {self.db_path}")
            self.conn.close()
            self.conn = None
    
    @classmethod
    def set_database(cls, db_path):
        cls.current_db_path = Path(db_path)
        
        try:
            LAST_USED.parent.mkdir(parents=True, exist_ok=True)
            LAST_USED.write_text(str(cls.current_db_path.resolve()), encoding="utf-8")
        except Exception as e:
            print(f"Errore durante la scrittura di last_used.txt: {e}")
    
    @classmethod
    def get_database(cls):
        return cls.current_db_path
    
