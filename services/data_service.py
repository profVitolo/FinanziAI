from datetime import date, timedelta

from data_manager.asset_data_manager import AssetDataManager
from data_collector.yahoo_collector import YahooCollector
from database.database_manager import DatabaseManager


class DataService:

    def __init__(self, database=None):
        database = database or DatabaseManager()
        self.asset_data_manager = AssetDataManager(database)
        self.collector = YahooCollector()

    def update_asset(self, symbol, initial_days=365):
        asset = self.asset_data_manager.get_asset_by_symbol(symbol)

        if asset is None:
            start_date = (date.today() - timedelta(days=initial_days)).isoformat()
            return self.sync_asset(symbol, start_date=start_date)

        asset_id = asset["id"]
        last_date = self.asset_data_manager.get_last_price_date(asset_id)

        if last_date is None:
            start_date = (date.today() - timedelta(days=initial_days)).isoformat()
            return self.sync_asset(symbol, start_date=start_date)
        
        if date.fromisoformat(last_date) >= date.today():
            return {
                "symbol": symbol,
                "prices_downloaded": 0
            }
            
        start_date = (date.fromisoformat(last_date) + timedelta(days=1)).isoformat()
        return self.sync_asset(symbol, start_date=start_date)

    def sync_asset(self, symbol, start_date, end_date=None):
        asset_info = self.collector.fetch_asset_info(symbol)
        
        if asset_info is None:
            return False
            
        self.asset_data_manager.begin_transaction()
        try:
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
                asset_id = asset["id"]

            prices = self.collector.fetch_prices(symbol, start_date, end_date)

            self.asset_data_manager.save_prices(asset_id, prices)

            self.asset_data_manager.commit()
            
            return {
                "symbol": symbol,
                "prices_downloaded": len(prices)
            }
        except Exception:
            self.asset_data_manager.rollback()
            raise
        finally:
            self.asset_data_manager.close()
    
    def sync_assets(self, asset_ids):
        results = []

        for asset_id in asset_ids:
            asset = self.asset_data_manager.get_asset_by_id(asset_id)

            if asset is None:
                continue

            symbol = asset["symbol"]

            try:
                result = self.update_asset(symbol)

                results.append({
                    "asset_id": asset_id,
                    "symbol": symbol,
                    "status": "success",
                    "result": result
                })

            except Exception as exc:
                results.append({
                    "asset_id": asset_id,
                    "symbol": symbol,
                    "status": "error",
                    "error": str(exc)
                })

        return results