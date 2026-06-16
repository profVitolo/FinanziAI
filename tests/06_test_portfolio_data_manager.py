from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

import sys
sys.path.insert(0, str(ROOT_DIR))

from data_manager.asset_data_manager import AssetDataManager
from data_manager.portfolio_data_manager import PortfolioDataManager
from database.database_manager import DatabaseManager

database = DatabaseManager()

adm = AssetDataManager(database)
pdm = PortfolioDataManager(database)

asset = adm.get_asset_by_symbol("AAPL")

if asset:
    asset_id = asset["id"]

    print("=== UPDATE POSITION ===")
    pdm.update_portfolio_position(asset_id=asset_id, quantity=10, avg_price=100)

    print("\n=== POSITION ===")
    print(dict(pdm.get_position(asset_id)))

    print("\n=== ALL POSITIONS ===")
    positions = pdm.get_all_positions()

    for position in positions:
        print(dict(position))

    print("\n=== WATCHLIST ADD ===")
    pdm.add_to_watchlist(asset_id)
    print(dict(pdm.get_watchlist()))

    print("\n=== WATCHLIST REMOVE ===")
    pdm.remove_from_watchlist(asset_id)
    print(dict(pdm.get_watchlist()))

    print("\n=== DELETE POSITION ===")
    pdm.delete_portfolio_position(asset_id)
    print("Last deleted position [None]:", (pdm.get_position(asset_id)))