from datetime import date, timedelta

from data_manager.asset_data_manager import AssetDataManager
from data_collector.yahoo_collector import YahooCollector
from database.database_initializer import DatabaseInitializer

from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
from config import DB_PATH, SCHEMA_PATH

class DataService:

    def __init__(self, db_path=DB_PATH):
        DatabaseInitializer.initialize(db_path, SCHEMA_PATH)
        self.asset_data_manager = AssetDataManager(db_path)
        self.collector = YahooCollector()

    def update_asset(self, symbol, initial_days=365):
        asset = self.asset_data_manager.get_asset_by_symbol(symbol)

        if asset is None:
            start_date = (date.today() - timedelta(days=initial_days)).isoformat()
            return self.sync_asset(symbol, start_date=start_date)

        asset_id = asset[0]
        last_date = self.asset_data_manager.get_last_price_date(asset_id)

        if last_date is None:
            start_date = (date.today() - timedelta(days=initial_days)).isoformat()
            return self.sync_asset(symbol, start_date=start_date)

        start_date = (date.fromisoformat(last_date) + timedelta(days=1)).isoformat()
        return self.sync_asset(symbol, start_date=start_date)

    def sync_asset(self, symbol, start_date, end_date=None):
        asset_info = self.collector.fetch_asset_info(symbol)
        
        if asset_info is None:
            return False

        asset = self.asset_data_manager.get_asset_by_symbol(symbol)

        if asset is None:
            asset_id = self.asset_data_manager.create_asset(
                symbol=symbol,
                name=asset_info["name"],
                type=asset_info["type"],
                currency=asset_info["currency"],
                exchange=asset_info["exchange"]
            )

        else:
            asset_id = asset[0]

        prices = self.collector.fetch_prices(symbol, start_date, end_date)

        self.asset_data_manager.save_prices(asset_id, prices)

        return {
            "symbol": symbol,
            "prices_downloaded": len(prices)
        }