from pathlib import Path
from database.database_manager import DatabaseManager
ROOT_DIR = Path(__file__).resolve().parent.parent


class DatabaseService:
    
    def __init__(self, db_path=None):
        self.database_manager = DatabaseManager(db_path)
        
    def list_vaults(self):
        database_dir = ROOT_DIR / "database"
        return sorted([file.name for file in database_dir.glob("*.db")])

    def create_vault(self, db_name):
        if not db_name.endswith(".db"):
            db_name += ".db"

        db_name = db_name.strip()
        
        if "/" in db_name or "\\" in db_name:
            raise ValueError("Invalid vault name")
    
        db_path = ROOT_DIR / "database" / db_name

        if db_path.exists():
            raise ValueError(f"Vault '{db_name}' already exists")

        self.database_manager.initialize(db_path)

        return db_name

    def set_vault(self, db_name):
        if not db_name.endswith(".db"):
            db_name += ".db"

        db_path = ROOT_DIR / "database" / db_name

        if not db_path.exists():
            raise ValueError(f"Vault '{db_name}' not found")

        self.database_manager.set_database(db_path)

    def get_current_vault(self):
        return Path(self.database_manager.get_database()).name