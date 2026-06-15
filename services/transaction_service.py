from data_manager.transaction_data_manager import TransactionDataManager


class TransactionService:

    def __init__(self):
        self.transaction_data_manager = TransactionDataManager()

    def get_transaction(self, transaction_id):
        return self.transaction_data_manager.get_transaction(transaction_id)

    def get_transactions(self, asset_id=None, start_date=None, end_date=None):
        if asset_id is not None:
            return self.transaction_data_manager.get_transactions_by_asset(asset_id, start_date, end_date)

        return self.transaction_data_manager.get_transactions(start_date, end_date)
        
        