from datetime import date
from data_manager.portfolio_data_manager import PortfolioDataManager


class PortfolioService:

    def __init__(self):
        self.portfolio_data_manager = PortfolioDataManager()

    def register_transaction(
        self,
        asset_id: int,
        operation_type: str,
        quantity: float,
        price: float,
        fees: float = 0,
        transaction_date: date | None = None
    ):
        if transaction_date is None:
            transaction_date = date.today()

        operation_type = operation_type.lower()

        position = self.portfolio_data_manager.get_position(asset_id)

        if operation_type == "buy":
            self.portfolio_data_manager.add_transaction(
                asset_id=asset_id,
                date=transaction_date,
                operation_type=operation_type,
                quantity=quantity,
                price=price,
                fees=fees
            )

            if position is None:
                self.portfolio_data_manager.update_portfolio_position(
                    asset_id=asset_id,
                    quantity=quantity,
                    avg_price=price,
                    last_update=transaction_date
                )

                return

            current_quantity = position[2]
            current_avg_price = position[3]

            new_quantity = current_quantity + quantity

            new_avg_price = ((current_quantity * current_avg_price) + (quantity * price)) / new_quantity

            self.portfolio_data_manager.update_portfolio_position(
                asset_id=asset_id,
                quantity=new_quantity,
                avg_price=new_avg_price,
                last_update=transaction_date
            )

            return
        # SELL
        if position is None:
            raise ValueError("Impossibile vendere un asset non presente in portafoglio")

        current_quantity = position[2]
        current_avg_price = position[3]

        if quantity > current_quantity:
            raise ValueError(f"Quantità insufficiente. Disponibili: {current_quantity}")

        self.portfolio_data_manager.add_transaction(
            asset_id=asset_id,
            date=transaction_date,
            operation_type=operation_type,
            quantity=quantity,
            price=price,
            fees=fees
        )

        new_quantity = current_quantity - quantity

        if new_quantity == 0:
            self.portfolio_data_manager.delete_portfolio_position(asset_id)
            return

        self.portfolio_data_manager.update_portfolio_position(
            asset_id=asset_id,
            quantity=new_quantity,
            avg_price=current_avg_price,
            last_update=transaction_date
        )
    
    def get_tracked_assets(self):
        tracked_assets = set()

        positions = self.portfolio_data_manager.get_all_positions()
        for position in positions:
            tracked_assets.add(position[1])  # asset_id

        watchlist = self.portfolio_data_manager.get_watchlist()
        for item in watchlist:
            tracked_assets.add(item[1])  # asset_id

        return list(tracked_assets)
    