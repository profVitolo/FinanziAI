from pathlib import Path
import sys
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from test_utils import *
from services.data_service import DataService
from data_manager.asset_data_manager import AssetDataManager
from data_engine.data_engine import DataEngine
from database.database_manager import DatabaseManager

database = DatabaseManager()

print_title("=== DATA PIPELINE TEST ===")

ds = DataService(database)

ds.sync_asset("AAPL", start_date="2025-01-01")
ds.sync_asset("^GSPC", start_date="2025-01-01")
ds.sync_asset("MSFT", start_date="2025-01-01")

print(ds.update_asset("AAPL", initial_days=365))
print(ds.update_asset("^GSPC", initial_days=365))
print(ds.update_asset("MSFT", initial_days=365))

adm = AssetDataManager(database)

asset = adm.get_asset_by_symbol("AAPL")

print_result("ASSET", (asset))

print("\n=== SYNC AAPL (1-2026) ===")
ds.sync_asset("AAPL", start_date="2026-01-01", end_date="2026-01-31")

print_result("ASSET DETAILS", ds.get_asset_details("AAPL", "2026-01-01", "2026-01-31"))

if asset:
    asset_id = asset["id"]

    print_result("LAST DATE", adm.get_last_price_date(asset_id))

    prices = adm.get_prices(asset_id)

    print_result("PRICE COUNT", len(prices))

    print("\n=== FIRST 5 ===")
    for row in prices[:5]:
        print_result("", row)

    print("\n=== LAST 5 ===")
    for row in prices[-5:]:
        print_result("",row)

engine = DataEngine(database)

print_result("AAPL ANALYSIS", engine.analyze_asset("AAPL"))

print_result("S&P500 ANALYSIS", engine.analyze_asset("^GSPC"))

print_result("MSFT ANALYSIS", engine.analyze_asset("MSFT"))

database.close()