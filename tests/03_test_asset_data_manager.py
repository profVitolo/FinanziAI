from pathlib import Path
import sys
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from api_test_utils import *
from data_manager.asset_data_manager import AssetDataManager
from database.database_manager import DatabaseManager

database = DatabaseManager()

adm = AssetDataManager(database)

print_title("=== TEST ASSET DATA MANAGER ===")

asset = adm.get_asset_by_symbol("AAPL")
print_result("AAPL:", asset)

if asset:
    asset_id = asset["id"]

    asset_by_id = adm.get_asset_by_id(asset_id)
    print_result("Asset by id:", asset_by_id)

    last_date = adm.get_last_price_date(asset_id)
    print_result("Last date:", last_date)

    prices = adm.get_prices(asset_id)

    print_result("Records:", len(prices))

    if prices:
        print_result("First:", (prices[0]))
        print_result("Last:", (prices[-1]))