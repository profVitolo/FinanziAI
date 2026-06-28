from pathlib import Path
import sys
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from test_utils import *
from data_manager.asset_data_manager import AssetDataManager
from data_manager.portfolio_data_manager import PortfolioDataManager
from data_manager.transaction_data_manager import TransactionDataManager
from services.portfolio_service import PortfolioService
from database.database_manager import DatabaseManager

database = DatabaseManager()

adm = AssetDataManager(database)
pdm = PortfolioDataManager(database)
tdm = TransactionDataManager(database)
service = PortfolioService(database)

print_title("=== TEST PORTFOLIO SERVICE ===")

asset = adm.get_asset_by_symbol("AAPL")

if asset is None:
    print("Asset AAPL non trovato")
    sys.exit(1)
else:
    print_result("Asset found", asset)
    
asset_id = asset["id"]

print_result("INITIAL POSITION [empty]", pdm.get_position(asset_id))

print("\n=== INITIAL TRANSACTIONS ===\n")
transactions = tdm.get_transactions_by_asset(asset_id)

for transaction in transactions:
    print_result("", transaction)

print("\n=== BUY 10 @ 100 ===\n")

service.register_transaction(asset_id=asset_id, operation_type="buy", quantity=10, price=100, fees=1 )

print_result("AFTER BUY", pdm.get_position(asset_id))

print("\n=== BUY 5 @ 120 ===\n")

service.register_transaction(asset_id=asset_id, operation_type="buy", quantity=5, price=120, fees=1)

print_result("AFTER BUY", pdm.get_position(asset_id))

print("\n=== SELL 3 ===\n")

service.register_transaction(asset_id=asset_id, operation_type="sell", quantity=3, price=130, fees=1)

print_result("AFTER SELL", pdm.get_position(asset_id))

print("\n=== SELL ALL REMAINING ===\n")

position = pdm.get_position(asset_id)

if position is not None:
    remaining_quantity = position["quantity"]

    service.register_transaction(
        asset_id=asset_id,
        operation_type="sell",
        quantity=remaining_quantity,
        price=130,
        fees=1
    )
    print("- Transaction registered (sell it all)\n")

print_result("Position after sell [None]", pdm.get_position(asset_id))

print("\n=== INVALID SELL ===\n")

try:
    service.register_transaction(asset_id=asset_id, operation_type="sell", quantity=999999, price=130, fees=1)

except Exception as exc:
    print("Errore atteso:")
    print(exc)

print("\n=== ALL TRANSACTIONS FOR AAPL ===\n")
transactions = tdm.get_transactions_by_asset(asset_id)

for transaction in transactions:
    print_result("", transaction)

print("\n=== UPDATE LAST TRANSACTION ===\n")
transactions = tdm.get_transactions_by_asset(asset_id)

if transactions:
    transaction_id = transactions[-1]["id"]

    service.update_transaction(
        transaction_id=transaction_id,
        asset_id=asset_id,
        transaction_date="2026-06-15",
        operation_type="buy",
        quantity=20,
        price=150,
        fees=2
    )

    print_result("LAST TRANSACTION", tdm.get_transaction(transaction_id))
    print_result("POSITION AFTER UPDATE", pdm.get_position(asset_id))

print("\n=== DELETE LAST TRANSACTION ===\n")
transactions = tdm.get_transactions_by_asset(asset_id)

if transactions:
    transaction_id = transactions[-1]["id"]

    service.delete_transaction(transaction_id)

    print_result("Is still there an id for deleted trans?", tdm.get_transaction(transaction_id))
    print_result("POSITION AFTER DELETE", pdm.get_position(asset_id))
    
print("\n=== REBUILD PORTFOLIO ===\n")
service.rebuild_portfolio()

print_result("POSITION AFTER REBUILD", pdm.get_position(asset_id))

database.close()
    