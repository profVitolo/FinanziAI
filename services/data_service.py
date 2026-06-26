from datetime import date, timedelta

from data_manager.asset_data_manager import AssetDataManager
from data_manager.portfolio_data_manager import PortfolioDataManager
from data_manager.transaction_data_manager import TransactionDataManager
from data_collector.yahoo_collector import YahooCollector
from database.database_manager import DatabaseManager
from config import BOOTSTRAP_DAYS 

class DataService:
    def __init__(self, database=None):
        database = database or DatabaseManager()
        self.asset_data_manager = AssetDataManager(database)
        self.portfolio_data_manager = PortfolioDataManager(database)
        self.transaction_data_manager = TransactionDataManager(database)
        self.collector = YahooCollector()
    
    def close(self):
        self.asset_data_manager.close()
    
    def update_asset(self, symbol, initial_days=365):
        asset = self.get_asset_by_symbol(symbol)

        if asset is None:
            return self._bootstrap_asset(symbol, initial_days)
        
        last_date = self._get_last_price_date(asset)

        if last_date is None:
            return self._bootstrap_asset(symbol, initial_days)
        
        if date.fromisoformat(last_date) >= date.today():
            return {
                "symbol": symbol,
                "prices_downloaded": 0
            }
            
        start_date = (date.fromisoformat(last_date) + timedelta(days=1)).isoformat()
        return self.sync_asset(symbol, start_date=start_date)

    def _bootstrap_asset(self, symbol, days=365):
        start = (date.today() - timedelta(days=days)).isoformat()
        return self.sync_asset(symbol, start)
    
    def sync_asset(self, symbol, start_date, end_date=None):
        asset_info = self._load_asset_info(symbol)
        start_date = self._normalize_date(start_date)
        end_date = self._normalize_date(end_date)

        self.asset_data_manager.begin_transaction()
        try:  
            asset = self.get_asset_by_symbol(symbol)
            asset_id, download_start = self._prepare_asset_for_sync(asset, asset_info, start_date)

            prices = self._download_prices(symbol, download_start, end_date)
            self.asset_data_manager.save_prices(asset_id, prices)
            self.asset_data_manager.commit()

            return {
                "symbol": symbol,
                "prices_downloaded": len(prices)
            }

        except Exception:
            self.asset_data_manager.rollback()
            raise
    
    @staticmethod
    def _normalize_date(value):
        if isinstance(value, str):
            return date.fromisoformat(value)
        return value
    
    def _download_prices(self, symbol, start_date, end_date):
        prices = self.collector.fetch_prices(symbol, start_date, end_date)

        if not prices:
            raise ValueError(f"No historical prices available for '{symbol}'")
        return prices
    
    def _create_asset(self, asset_info):
        return self.asset_data_manager.create_asset(
            symbol=asset_info["symbol"],
            name=asset_info["name"],
            type=asset_info["type"],
            currency=asset_info["currency"],
            exchange=asset_info["exchange"],
            sector=asset_info["sector"],
            industry=asset_info["industry"],
            country=asset_info["country"],
            market_cap=asset_info["market_cap"],
            beta=asset_info["beta"],
            website=asset_info["website"]
        )
    
    def _update_asset(self, asset_id, asset_info):
        self.asset_data_manager.update_asset_metadata(
                asset_id=asset_id,
                sector=asset_info["sector"],
                industry=asset_info["industry"],
                country=asset_info["country"],
                market_cap=asset_info["market_cap"],
                beta=asset_info["beta"],
                website=asset_info["website"]
            )
    
    def _prepare_asset_for_sync(self, asset, asset_info, start_date):
        needs_bootstrap = (asset is None or self._get_last_price_date(asset) is None)

        download_start = start_date
        if needs_bootstrap:
            download_start -= timedelta(days=BOOTSTRAP_DAYS)

        if asset is None:
            asset_id = self._create_asset(asset_info)
        else:
            asset_id = asset["id"]
            self._update_asset(asset_id, asset_info)

        return asset_id, download_start
    
    def _get_last_price_date(self, asset):
        return self.asset_data_manager.get_last_price_date(asset["id"])
    
    def _load_asset_info(self, symbol):
        asset_info = self.collector.fetch_asset_info(symbol)

        if asset_info is None:
            raise ValueError(f"Asset '{symbol}' not found")

        return asset_info
    
    def sync_tracked_assets(self, asset_ids):
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
        
    def get_all_assets(self):
        return self.asset_data_manager.get_all_assets()
    
    def get_asset_by_symbol(self, symbol):
        return self.asset_data_manager.get_asset_by_symbol(symbol)
    
    def ensure_asset_by_symbol(self, symbol):
        asset = self.get_asset_by_symbol(symbol)

        if asset is None:
            self._bootstrap_asset(symbol)
            asset = self.get_asset_by_symbol(symbol)

        return asset
            
    def get_asset_by_id(self, asset_id):
        return self.asset_data_manager.get_asset_by_id(asset_id)
    
    def get_asset_details(self, symbol, start_date=None, end_date=None):
        asset = self.ensure_asset_by_symbol(symbol)
        
        start_date = self._normalize_date(start_date)
        end_date = self._normalize_date(end_date)
            
        prices = self.asset_data_manager.get_prices(asset["id"], start_date, end_date)

        return {"asset": asset, "prices": prices}
        
    def delete_asset_by_symbol(self, symbol):
        asset = self.get_asset_by_symbol(symbol)

        if asset is None:
            return {
                "symbol": symbol,
                "deleted": False
            }

        self._ensure_asset_not_used(asset)

        self.asset_data_manager.begin_transaction()

        try:
            self._delete_asset(asset)
            self.asset_data_manager.commit()

            return {
                "symbol": symbol,
                "deleted": True
            }

        except Exception:
            self.asset_data_manager.rollback()
            raise
    
    def _ensure_asset_not_used(self, asset):
        transactions = (
            self.transaction_data_manager
            .get_transactions_by_asset(asset["id"])
        )

        if transactions:
            raise ValueError(
                f"Cannot delete asset '{asset['symbol']}': "
                "asset has transactions"
            )
    
    def _delete_asset(self, asset):
        asset_id = asset["id"]

        self.portfolio_data_manager.remove_from_watchlist(asset_id)
        self.asset_data_manager.delete_asset(asset_id)
    
