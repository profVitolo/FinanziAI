from pathlib import Path
import sys
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from api_test_utils import *
from data_manager.asset_data_manager import AssetDataManager
from data_manager.portfolio_data_manager import PortfolioDataManager
from database.database_manager import DatabaseManager

database = DatabaseManager()

adm = AssetDataManager(database)
pdm = PortfolioDataManager(database)

print_title("=== TEST PORTFOLIO DATA MANAGER ===")

asset = adm.get_asset_by_symbol("AAPL")

if asset:
    asset_id = asset["id"]

    print("=== UPDATE POSITION ===")
    pdm.update_portfolio_position(asset_id=asset_id, quantity=10, avg_price=100)

    print_result("POSITION", pdm.get_position(asset_id))


    positions = pdm.get_all_positions()

    print("\n=== ALL POSITIONS ===")
    for position in positions:
        print_result("", (position))
    else:
        print("None")

    print("\n=== WATCHLIST ADD ===")
    pdm.add_to_watchlist(asset_id)
    print_result("WatchList after ADD", (pdm.get_watchlist()))

    print("\n=== WATCHLIST REMOVE ===")
    pdm.remove_from_watchlist(asset_id)
    print_result("WatchList after REMOVE", pdm.get_watchlist())

    print("\n=== DELETE POSITION ===")
    pdm.delete_portfolio_position(asset_id)
    print_result("Last deleted position [None]", (pdm.get_position(asset_id)))