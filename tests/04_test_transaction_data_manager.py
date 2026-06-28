from pathlib import Path
import sys
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from test_utils import *
from data_manager.asset_data_manager import AssetDataManager
from data_manager.transaction_data_manager import TransactionDataManager
from database.database_manager import DatabaseManager

database = DatabaseManager()

adm = AssetDataManager(database)
tdm = TransactionDataManager(database)

print_title("=== TEST TRANSACTION DATA MANAGER ===")

transactions = tdm.get_transactions()

print("=== ALL TRANSACTIONS ===")
for transaction in transactions:
    print_result("", (transaction))
else:
    print("None")

asset = adm.get_asset_by_symbol("AAPL")

if asset:
    asset_id = asset["id"]

    transaction_id = tdm.add_transaction(
        asset_id=asset_id,
        date="2026-05-31",
        operation_type="buy",
        quantity=10,
        price=100,
        fees=1
    )

    print("\n=== CREATED TRANSACTION ===")
    print_result("", (tdm.get_transaction(transaction_id)))

    print("\n=== TRANSACTIONS BY ASSET ===")

    transactions = tdm.get_transactions_by_asset(asset_id)

    for transaction in transactions:
        print_result("", (transaction))

    print("\n=== UPDATE TRANSACTION ===")

    tdm.update_transaction(
        transaction_id=transaction_id,
        asset_id=asset_id,
        date="2026-05-31",
        operation_type="buy",
        quantity=20,
        price=110,
        fees=2
    )

    print_result("", (tdm.get_transaction(transaction_id)))

    print("\n=== DELETE TRANSACTION ===")

    tdm.delete_transaction(transaction_id)

    print_result("Last deleted transaction id [None]", tdm.get_transaction(transaction_id))
    
database.close()