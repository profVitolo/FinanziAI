from datetime import date
from data_manager.portfolio_data_manager import PortfolioDataManager
from data_manager.transaction_data_manager import TransactionDataManager


class PortfolioService:

    def __init__(self):
        self.portfolio_data_manager = PortfolioDataManager()
        self.transaction_data_manager = TransactionDataManager()

    def register_transaction(self, asset_id, operation_type, quantity, price, fees=0, transaction_date=None):
        if transaction_date is None:
            transaction_date = date.today()

        operation_type = operation_type.lower()

        if operation_type == "sell":
            position = self.portfolio_data_manager.get_position(asset_id)

            if position is None:
                raise ValueError("Impossibile vendere un asset non presente in portafoglio")

            current_quantity = position[2]

            if quantity > current_quantity:
                raise ValueError(f"Quantità insufficiente. Disponibili: {current_quantity}")

        transaction_id = self.transaction_data_manager.add_transaction(
            asset_id=asset_id,
            date=transaction_date,
            operation_type=operation_type,
            quantity=quantity,
            price=price,
            fees=fees
        )

        self._recalculate_asset_position(asset_id)
        
        return transaction_id
    
    def get_tracked_assets(self):
        tracked_assets = set()

        positions = self.portfolio_data_manager.get_all_positions()
        for position in positions:
            tracked_assets.add(position[1])  # asset_id

        watchlist = self.portfolio_data_manager.get_watchlist()
        for item in watchlist:
            tracked_assets.add(item[1])  # asset_id

        return list(tracked_assets)
    
    def update_transaction(self, transaction_id, asset_id, operation_type, quantity, price, fees=0, transaction_date=None):
        old_transaction = self.transaction_data_manager.get_transaction(transaction_id)

        if old_transaction is None:
            raise ValueError("Transaction not found")

        old_asset_id = old_transaction[1]

        if transaction_date is None:
            transaction_date = date.today()

        self.transaction_data_manager.update_transaction(
            transaction_id=transaction_id,
            asset_id=asset_id,
            date=transaction_date,
            operation_type=operation_type.lower(),
            quantity=quantity,
            price=price,
            fees=fees
        )

        self._recalculate_asset_position(old_asset_id)

        if old_asset_id != asset_id:
            self._recalculate_asset_position(asset_id)
            
    def delete_transaction(self, transaction_id):
        transaction = self.transaction_data_manager.get_transaction(transaction_id)

        if transaction is None:
            raise ValueError("Transaction not found")

        asset_id = transaction[1]

        self.transaction_data_manager.delete_transaction(transaction_id)

        self._recalculate_asset_position(asset_id)
        
    def _recalculate_asset_position(self, asset_id):
        transactions = (self.transaction_data_manager.get_transactions_by_asset(asset_id))

        if not transactions:
            self.portfolio_data_manager.delete_portfolio_position(asset_id)
            return

        quantity = 0
        avg_price = 0
        last_update = None

        for transaction in transactions:
            operation_type = transaction[3].lower()
            t_quantity = transaction[4]
            t_price = transaction[5]
            t_date = transaction[2]

            if operation_type == "buy":
                new_quantity = quantity + t_quantity
                
                if new_quantity <= 0:
                    raise ValueError(f"Posizione non valida per asset {asset_id}")
                    
                avg_price = ((quantity * avg_price) + (t_quantity * t_price)) / new_quantity
                quantity = new_quantity

            elif operation_type == "sell":
                quantity -= t_quantity
                if quantity < 0:
                    raise ValueError(f"Posizione negativa per asset {asset_id}")

            last_update = t_date

        if quantity <= 0:
            self.portfolio_data_manager.delete_portfolio_position(asset_id)
            return

        self.portfolio_data_manager.update_portfolio_position(asset_id=asset_id, quantity=quantity, avg_price=avg_price, last_update=last_update)
        
    def rebuild_portfolio(self):
        positions = self.portfolio_data_manager.get_all_positions()

        for position in positions:
            self.portfolio_data_manager.delete_portfolio_position(position[1])

        transactions = (self.transaction_data_manager.get_transactions())

        asset_ids = {transaction[1] for transaction in transactions}

        for asset_id in asset_ids:
            self._recalculate_asset_position(asset_id)   
            