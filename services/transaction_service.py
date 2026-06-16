from data_manager.transaction_data_manager import TransactionDataManager
from database.database_manager import DatabaseManager

class TransactionService:

    def __init__(self, database=None):
        database = database or DatabaseManager()
        self.transaction_data_manager = TransactionDataManager(database)

    def get_transaction(self, transaction_id):
        try:
            return self.transaction_data_manager.get_transaction(transaction_id)
        finally:
            self.transaction_data_manager.close()

    def get_transactions(self, asset_id=None, start_date=None, end_date=None):
        try:
            if asset_id is not None:
                return self.transaction_data_manager.get_transactions_by_asset(asset_id, start_date, end_date)

            return self.transaction_data_manager.get_transactions(start_date, end_date)
        finally:
            self.transaction_data_manager.close()
            