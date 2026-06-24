from datetime import datetime
from pathlib import Path
from database.database_manager import DatabaseManager
ROOT_DIR = Path(__file__).resolve().parent.parent


class DatabaseService:
    
    def __init__(self, db_path=None):
        self.database_manager = DatabaseManager(db_path)
        
    def close(self):
        self.database_manager.close()
        
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
    
    def delete_vault(self, db_name):
        if not db_name.endswith(".db"):
            db_name += ".db"

        db_path = ROOT_DIR / "database" / db_name

        if not db_path.exists():
            raise ValueError(f"Vault '{db_name}' not found")

        if db_name == self.get_current_vault():
            raise ValueError("Cannot delete current vault")

        if len(self.list_vaults()) <= 1:
            raise ValueError("Cannot delete last vault")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = db_path.with_name(f"{db_path.stem}_{timestamp}.bk")

        if backup_path.exists():
            backup_path.unlink()

        db_path.rename(backup_path)

        return db_name