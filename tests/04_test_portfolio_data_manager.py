from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent

import sys
sys.path.insert(0, str(ROOT_DIR))

from data_manager.asset_data_manager import AssetDataManager
from data_manager.portfolio_data_manager import PortfolioDataManager

adm = AssetDataManager()
pdm = PortfolioDataManager()

asset = adm.get_asset_by_symbol("AAPL")

if asset:

    asset_id = asset[0]

    pdm.add_transaction(
        asset_id=asset_id, 
        date="2026-05-31", 
        operation_type="buy", 
        quantity=10, 
        price=100, 
        fees=1
    )

    transactions = pdm.get_transactions_by_asset(asset_id)

    print("Transactions:")
    for t in transactions:
        print(t)

    pdm.update_portfolio_position(asset_id=asset_id, quantity=10, avg_price=100)

    print("Position:")
    print(pdm.get_position(asset_id))

    print("All positions:")
    print(pdm.get_all_positions())

    pdm.add_to_watchlist(asset_id)

    print("Watchlist:")
    print(pdm.get_watchlist())