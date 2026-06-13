from datetime import date

from data.portfolio_data_manager import PortfolioDataManager


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

        self.portfolio_data_manager.add_transaction(
            asset_id=asset_id,
            date=transaction_date,
            operation_type=operation_type,
            quantity=quantity,
            price=price,
            fees=fees
        )

        position = self.portfolio_data_manager.get_position(asset_id)

        if position is None:
            self.portfolio_data_manager.update_portfolio_position(
                asset_id=asset_id,
                quantity=quantity,
                avg_price=price,
                last_update=transaction_date
            )
            return

        current_quantity = position["quantity"]
        current_avg_price = position["avg_price"]

        if operation_type.lower() == "buy":
            new_quantity = current_quantity + quantity

            new_avg_price = ((current_quantity * current_avg_price) + (quantity * price) ) / new_quantity
        else:
            new_quantity = current_quantity - quantity
            new_avg_price = current_avg_price

        self.portfolio_data_manager.update_portfolio_position(
            asset_id=asset_id,
            quantity=new_quantity,
            avg_price=new_avg_price,
            last_update=transaction_date
        )
        
        