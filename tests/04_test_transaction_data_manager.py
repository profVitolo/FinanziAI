from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

import sys
sys.path.insert(0, str(ROOT_DIR))

from data_manager.asset_data_manager import AssetDataManager
from data_manager.transaction_data_manager import TransactionDataManager

adm = AssetDataManager()
tdm = TransactionDataManager()

print("=== ALL TRANSACTIONS ===")

transactions = tdm.get_transactions()

for transaction in transactions:
    print(transaction)

asset = adm.get_asset_by_symbol("AAPL")

if asset:
    asset_id = asset[0]

    transaction_id = tdm.add_transaction(
        asset_id=asset_id,
        date="2026-05-31",
        operation_type="buy",
        quantity=10,
        price=100,
        fees=1
    )

    print("\n=== CREATED TRANSACTION ===")
    print(tdm.get_transaction(transaction_id))

    print("\n=== TRANSACTIONS BY ASSET ===")

    transactions = tdm.get_transactions_by_asset(asset_id)

    for transaction in transactions:
        print(transaction)

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

    print(tdm.get_transaction(transaction_id))

    print("\n=== DELETE TRANSACTION ===")

    tdm.delete_transaction(transaction_id)

    print(tdm.get_transaction(transaction_id))
    
    