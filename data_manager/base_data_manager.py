from database.database_manager import DatabaseManager

class BaseDataManager:

    def __init__(self, database=None):
        self.database = database or DatabaseManager()

    def _connect(self):
        return self.database.connect()

    def begin_transaction(self):
        self.database.begin_transaction()

    def commit(self):
        self.database.commit()

    def rollback(self):
        self.database.rollback()

    def close(self):
        self.database.close()