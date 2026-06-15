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

    print("=== UPDATE POSITION ===")
    pdm.update_portfolio_position(asset_id=asset_id, quantity=10, avg_price=100)

    print("\n=== POSITION ===")
    print(pdm.get_position(asset_id))

    print("\n=== ALL POSITIONS ===")
    positions = pdm.get_all_positions()

    for position in positions:
        print(position)

    print("\n=== WATCHLIST ADD ===")
    pdm.add_to_watchlist(asset_id)
    print(pdm.get_watchlist())

    print("\n=== WATCHLIST REMOVE ===")
    pdm.remove_from_watchlist(asset_id)
    print(pdm.get_watchlist())

    print("\n=== DELETE POSITION ===")
    pdm.delete_portfolio_position(asset_id)
    print(pdm.get_position(asset_id))