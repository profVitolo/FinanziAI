from data_manager.asset_data_manager import AssetDataManager
from data_manager.portfolio_data_manager import PortfolioDataManager
from database.database_manager import DatabaseManager


class DataSupplier:
    def __init__(self, database=None):
        self.database = database or DatabaseManager()

        self.asset_data_manager = AssetDataManager(self.database)
        self.portfolio_data_manager = PortfolioDataManager(self.database)

    def close(self):
        self.portfolio_data_manager.close()

    # ------------------------------------------------------------------
    # Asset
    # ------------------------------------------------------------------

    def get_asset(self, symbol):
        return self.get_asset_by_symbol(symbol)

    def get_asset_by_symbol(self, symbol):
        return self.asset_data_manager.get_asset_by_symbol(symbol)

    def get_asset_by_id(self, asset_id):
        return self.asset_data_manager.get_asset_by_id(asset_id)

    # ------------------------------------------------------------------
    # Prices
    # ------------------------------------------------------------------

    def get_prices(self, asset_id, start_date=None, end_date=None):
        return self.asset_data_manager.get_prices(asset_id, start_date, end_date)
        
    def get_last_close(self, prices):
        if not prices:
            return None

        for row in reversed(prices):
            if row["close"] is not None:
                return row["close"]

        return None

    # ------------------------------------------------------------------
    # Portfolio
    # ------------------------------------------------------------------

    def get_portfolio_positions(self):
        return self.portfolio_data_manager.get_all_positions()