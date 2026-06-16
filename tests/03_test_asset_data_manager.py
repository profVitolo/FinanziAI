from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent

import sys
sys.path.insert(0, str(ROOT_DIR))

from data_manager.asset_data_manager import AssetDataManager
from database.database_manager import DatabaseManager

database = DatabaseManager()

adm = AssetDataManager(database)

print("=== TEST ASSET DATA MANAGER ===")

asset = adm.get_asset_by_symbol("AAPL")
print("AAPL:", dict(asset))

if asset:
    asset_id = asset[0]

    asset_by_id = adm.get_asset_by_id(asset_id)
    print("Asset by id:", dict(asset_by_id))

    last_date = adm.get_last_price_date(asset_id)
    print("Last date:", last_date)

    prices = adm.get_prices(asset_id)

    print("Records:", len(prices))

    if prices:
        print("First:", dict(prices[0]))
        print("Last:", dict(prices[-1]))