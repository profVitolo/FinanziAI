from datetime import date
from data_manager.portfolio_data_manager import PortfolioDataManager
from data_manager.transaction_data_manager import TransactionDataManager
from database.database_manager import DatabaseManager

## un solo DataManager → chiudo il DataManager; 
## più DataManager condivisi → chiudo il DatabaseManager (self.database)

class PortfolioService:

    def __init__(self, database=None):
        self.database = database or DatabaseManager()
        self.portfolio_data_manager = PortfolioDataManager(self.database)
        self.transaction_data_manager = TransactionDataManager(self.database)

    def register_transaction(self, asset_id, operation_type, quantity, price, fees=0, transaction_date=None):
        if transaction_date is None:
            transaction_date = date.today()

        operation_type = operation_type.lower()
        
        self.transaction_data_manager.begin_transaction()

        try:
            transaction_id = self.transaction_data_manager.add_transaction(
                asset_id=asset_id,
                date=transaction_date,
                operation_type=operation_type,
                quantity=quantity,
                price=price,
                fees=fees
            )

            self._validate_asset_transactions(asset_id)
            self._rebuild_asset_position(asset_id)

            self.transaction_data_manager.commit()

            return transaction_id

        except Exception:
            self.transaction_data_manager.rollback()
            raise
        finally:
            self.transaction_data_manager.close()
    
    def update_transaction(self,transaction_id, asset_id, operation_type, quantity, price, fees=0, transaction_date=None):
        old_transaction = self.transaction_data_manager.get_transaction(transaction_id)

        if old_transaction is None:
            raise ValueError("Transaction not found")

        old_asset_id = old_transaction["asset_id"]

        if transaction_date is None:
            transaction_date = date.today()

        self.transaction_data_manager.begin_transaction()

        try:
            self.transaction_data_manager.update_transaction(
                transaction_id=transaction_id,
                asset_id=asset_id,
                date=transaction_date,
                operation_type=operation_type.lower(),
                quantity=quantity,
                price=price,
                fees=fees
            )

            self._validate_asset_transactions(old_asset_id)

            if old_asset_id != asset_id:
                self._validate_asset_transactions(asset_id)

            self._rebuild_asset_position(old_asset_id)

            if old_asset_id != asset_id:
                self._rebuild_asset_position(asset_id)

            self.transaction_data_manager.commit()

        except Exception:
            self.transaction_data_manager.rollback()
            raise
        finally:
            self.transaction_data_manager.close()
            
    def delete_transaction(self, transaction_id):
        transaction = self.transaction_data_manager.get_transaction(transaction_id)

        if transaction is None:
            raise ValueError("Transaction not found")

        asset_id = transaction["asset_id"]
        self.transaction_data_manager.begin_transaction()

        try:
            self.transaction_data_manager.delete_transaction(transaction_id)
            self._validate_asset_transactions(asset_id)
            self._rebuild_asset_position(asset_id)
            self.transaction_data_manager.commit()

        except Exception:
            self.transaction_data_manager.rollback()
            raise
        finally:
            self.transaction_data_manager.close()
        
    def _validate_asset_transactions(self, asset_id):
        transactions = self.transaction_data_manager.get_transactions_by_asset(asset_id)

        quantity = 0

        for transaction in transactions:
            operation_type = transaction["type"].lower()
            t_quantity = transaction["quantity"]

            if operation_type == "buy":
                quantity += t_quantity

            elif operation_type == "sell":
                quantity -= t_quantity

            if quantity < 0:
                raise ValueError(f"Posizione negativa per asset {asset_id}")
    
    def _rebuild_asset_position(self, asset_id):
        transactions = self.transaction_data_manager.get_transactions_by_asset(asset_id)

        if not transactions:
            self.portfolio_data_manager.delete_portfolio_position(asset_id)
            return

        quantity = 0
        avg_price = 0
        last_update = None

        for transaction in transactions:
            operation_type = transaction["type"].lower()
            t_quantity = transaction["quantity"]
            t_price = transaction["price"]
            t_date = transaction["date"]

            if operation_type == "buy":
                new_quantity = quantity + t_quantity

                avg_price = ((quantity * avg_price) + (t_quantity * t_price)) / new_quantity
                quantity = new_quantity

            elif operation_type == "sell":
                quantity -= t_quantity

            last_update = t_date

        if quantity <= 0:
            self.portfolio_data_manager.delete_portfolio_position(asset_id)
            return

        self.portfolio_data_manager.update_portfolio_position(asset_id=asset_id, quantity=quantity, avg_price=avg_price, last_update=last_update)
        
    def rebuild_portfolio(self):
        self.transaction_data_manager.begin_transaction()

        try:
            positions = self.portfolio_data_manager.get_all_positions()

            for position in positions:
                self.portfolio_data_manager.delete_portfolio_position(position["asset_id"])

            transactions = self.transaction_data_manager.get_transactions()

            asset_ids = {transaction["asset_id"] for transaction in transactions}

            for asset_id in asset_ids:
                self._rebuild_asset_position(asset_id)
            
            self.transaction_data_manager.commit()

        except Exception:
            self.transaction_data_manager.rollback()
            raise

        finally:
            self.database.close()
    
    def get_tracked_assets(self):
        try:
            tracked_assets = set()

            positions = self.portfolio_data_manager.get_all_positions()
            for position in positions:
                tracked_assets.add(position["asset_id"])  # asset_id

            watchlist = self.portfolio_data_manager.get_watchlist()
            for item in watchlist:
                tracked_assets.add(item["asset_id"])  # asset_id

            return list(tracked_assets)
            
        finally:
            self.portfolio_data_manager.close()
    
    def get_all_positions(self):
        try:
            return self.portfolio_data_manager.get_all_positions()
        finally:
            self.portfolio_data_manager.close()
            
    def get_watchlist(self):
        try:
            return self.portfolio_data_manager.get_watchlist()
        finally:
            self.portfolio_data_manager.close()
            
    def remove_from_watchlist(self, asset_id):
        try:
            return self.portfolio_data_manager.remove_from_watchlist(asset_id)
        finally:
            self.portfolio_data_manager.close()
            
    def add_to_watchlist(self, asset_id):
        try:
            return self.portfolio_data_manager.add_to_watchlist(asset_id)
        finally:
            self.portfolio_data_manager.close()