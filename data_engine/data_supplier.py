from data_manager.asset_data_manager import AssetDataManager
from data_manager.portfolio_data_manager import PortfolioDataManager
from database.database_manager import DatabaseManager
from data_engine.data_engine_models import AssetItem, PositionItem, PriceItem, WatchlistItem


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
        asset = self.asset_data_manager.get_asset_by_symbol(symbol)
        return self._build_asset(asset)

    def get_asset_by_id(self, asset_id):
        asset = self.asset_data_manager.get_asset_by_id(asset_id)
        return self._build_asset(asset)

    # ------------------------------------------------------------------
    # Prices
    # ------------------------------------------------------------------

    def get_prices(self, asset_id, start_date=None, end_date=None):
        prices = self.asset_data_manager.get_prices(asset_id, start_date, end_date)
        return [self._build_price(price) for price in prices]

    # ------------------------------------------------------------------
    # Portfolio
    # ------------------------------------------------------------------

    def get_portfolio_positions(self):
        positions = self.portfolio_data_manager.get_all_positions()
        return [self._build_position(position) for position in positions]

    # ------------------------------------------------------------------
    # Watchlist
    # ------------------------------------------------------------------

    def get_watchlist(self):
        watchlist = [
            WatchlistItem.from_dict(row)
            for row in self.portfolio_data_manager.get_watchlist()
        ]

        assets = []
        for item in watchlist:
            asset = self.get_asset_by_id(item.asset_id)
            if asset is not None:
                assets.append(asset)

        return assets
        
    # ------------------------------------------------------------------
    # Builders
    # ------------------------------------------------------------------

    def _build_asset(self, asset):
        if asset is None:
            return None

        return AssetItem.from_dict(asset)

    def _build_position(self, position):
        return PositionItem.from_dict(position)
    
    def _build_price(self, price):
        return PriceItem.from_dict(price)