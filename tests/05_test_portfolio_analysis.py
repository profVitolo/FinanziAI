from pathlib import Path
import sys
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from test_utils import *
from data_engine_test_utils import *
from data_engine.portfolio_calculator import PortfolioCalculator
from data_engine.data_engine_models import AssetItem, Performance, PortfolioPosition

pa = PortfolioCalculator()

print_title("=== TEST PORTFOLIO ANALYSIS ===")

print_result("POSITION VALUE", pa.calculate_position_value(quantity=10, market_price=120))
print_result("PERFORMANCE", pa.calculate_performance(quantity=10, avg_price=100, market_price=120))

positions = [
    make_portfolio_position(
        asset=make_asset(symbol="AAPL"),
        position=make_position(quantity=10, avg_price=100),
        market_price=120,
    ),
    make_portfolio_position(
        asset=make_asset(
            id=2,
            symbol="MSFT",
            name="Microsoft Corp.",
        ),
        position=make_position(
            asset_id=2,
            quantity=5,
            avg_price=160,
        ),
        market_price=160,
    ),
]

print_result("PORTFOLIO VALUE", pa.calculate_portfolio_value(positions))
print_result("EXPOSURE", pa.calculate_exposure(positions))
print_result("RISK", pa.calculate_risk(positions))