from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

import sys
sys.path.insert(0, str(ROOT_DIR))

from data_manager.asset_data_manager import AssetDataManager
from data_manager.portfolio_data_manager import PortfolioDataManager
from services.portfolio_service import PortfolioService


if __name__ == "__main__":
    adm = AssetDataManager()
    pdm = PortfolioDataManager()
    service = PortfolioService()

    asset = adm.get_asset_by_symbol("AAPL")

    if asset is None:
        print("Asset AAPL non trovato")
        sys.exit(1)

    asset_id = asset[0]

    print("\n=== INITIAL POSITION ===\n")
    print(pdm.get_position(asset_id))

    print("\n=== BUY 10 @ 100 ===\n")

    service.register_transaction(asset_id=asset_id, operation_type="buy", quantity=10, price=100, fees=1)

    print(pdm.get_position(asset_id))

    print("\n=== BUY 5 @ 120 ===\n")

    service.register_transaction(asset_id=asset_id, operation_type="buy", quantity=5, price=120, fees=1)

    print(pdm.get_position(asset_id))

    print("\n=== SELL 3 ===\n")

    service.register_transaction(asset_id=asset_id, operation_type="sell", quantity=3, price=130, fees=1)

    print(pdm.get_position(asset_id))

    print("\n=== SELL ALL REMAINING ===\n")

    position = pdm.get_position(asset_id)

    if position is not None:
        remaining_quantity = position[2]

        service.register_transaction(asset_id=asset_id, operation_type="sell", quantity=remaining_quantity, price=130, fees=1)

    print(pdm.get_position(asset_id))

    print("\n=== INVALID SELL ===\n")

    try:
        service.register_transaction(asset_id=asset_id, operation_type="sell", quantity=999999, price=130, fees=1)

    except Exception as exc:
        print("Errore atteso:")
        print(exc)

    print("\n=== LAST TRANSACTIONS ===\n")

    transactions = pdm.get_transactions()

    for transaction in transactions[-10:]:
        print(transaction)