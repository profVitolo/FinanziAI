from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from test_utils import *

from services.data_service import DataService
from database.database_manager import DatabaseManager

database = DatabaseManager()
service = DataService(database)

print_title("=== TEST DATA SERVICE ===")

SYMBOL = "MSFT"

print("\n=== GET ASSET ===\n")
asset = service.get_asset_by_symbol(SYMBOL)
print_result("Asset", asset)

print("\n=== ENSURE ASSET ===\n")
asset = service.ensure_asset_by_symbol(SYMBOL)
print_result("Asset", asset)

print("\n=== ASSET DETAILS ===\n")
details = service.get_asset_details(SYMBOL)
print_result("Asset", details["asset"])
print_result("Prices", len(details["prices"]))

print("\n=== UPDATE ASSET ===\n")
result = service.update_asset(SYMBOL)
print_result("Update", result)

print("\n=== SYNC ASSET (LAST 30 DAYS) ===\n")
result = service.sync_asset(
    SYMBOL,
    start_date="2026-05-01"
)
print_result("Sync", result)

print("\n=== ALL ASSETS ===\n")
assets = service.get_all_assets()
print_result("Assets count", len(assets))

print("\n=== GET BY ID ===\n")
asset = service.get_asset_by_symbol(SYMBOL)
asset_by_id = service.get_asset_by_id(asset["id"])
print_result("Asset by id", asset_by_id)

print("\n=== DELETE UNKNOWN ASSET ===\n")
result = service.delete_asset_by_symbol("THIS_SYMBOL_DOES_NOT_EXIST")
print_result("Delete", result)

print("\n=== DELETE USED ASSET ===\n")
try:
    result = service.delete_asset_by_symbol(SYMBOL)
    print_result("Delete", result)
except Exception as exc:
    print("Expected error:")
    print(exc)

print("\n=== ENSURE UNKNOWN ASSET ===\n")

asset = service.ensure_asset_by_symbol("AMD")
print_result("AMD", asset)

print("\n=== UPDATE AGAIN ===\n")

result = service.update_asset(SYMBOL)
print_result("Second update", result)

service.close()
