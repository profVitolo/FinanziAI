from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent

import sys
sys.path.insert(0, str(ROOT_DIR))

from services.data_service import DataService
from data_manager.asset_data_manager import AssetDataManager
from data_engine.data_engine import DataEngine

print("=== DATA PIPELINE TEST ===")

ds = DataService()

ds.sync_asset("AAPL", start_date="2025-01-01")
ds.sync_asset("^GSPC", start_date="2025-01-01")
ds.sync_asset("MSFT", start_date="2025-01-01")

print(ds.update_asset("AAPL", initial_days=365))
print(ds.update_asset("^GSPC", initial_days=365))
print(ds.update_asset("MSFT", initial_days=365))

adm = AssetDataManager()

asset = adm.get_asset_by_symbol("AAPL")

print("\n=== ASSET ===")
print(asset)

if asset:
    asset_id = asset[0]

    print("\n=== LAST DATE ===")
    print(adm.get_last_price_date(asset_id))

    prices = adm.get_prices(asset_id)

    print("\n=== PRICE COUNT ===")
    print(len(prices))

    print("\n=== FIRST 5 ===")
    for row in prices[:5]:
        print(row)

    print("\n=== LAST 5 ===")
    for row in prices[-5:]:
        print(row)

engine = DataEngine()

print("\n=== AAPL ANALYSIS ===")
print(engine.analyze_asset("AAPL"))

print("\n=== S&P500 ANALYSIS ===")
print(engine.analyze_asset("^GSPC"))

print("\n=== MSFT ANALYSIS ===")
print(engine.analyze_asset("MSFT"))