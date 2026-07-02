from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from test_utils import *
from data_engine_test_utils import *

from data_engine.portfolio_calculator import PortfolioCalculator
from data_engine.data_engine_models import PortfolioItem

pc = PortfolioCalculator()

portfolio_item = PortfolioItem(
    position=make_position(
        asset_id=1,
        quantity=10,
        avg_price=100,
    ),
    asset=make_asset(
        id=1,
        symbol="AAPL",
        name="Apple Inc.",
    ),
    market_price=120,
)

print_title("=== TEST PORTFOLIO CALCULATOR ===")

position = pc.build_position(portfolio_item)
print_result("BUILD POSITION", position)

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

print_result("PORTFOLIO VALUE", pc.calculate_portfolio_value(positions))
exposure = PortfolioExposure(
    by_symbol=pc.calculate_symbol_exposure(positions),
    by_sector=pc.calculate_sector_exposure(positions),
    by_country=pc.calculate_country_exposure(positions),
    by_currency=pc.calculate_currency_exposure(positions),
)

print_result("EXPOSURE", exposure)
print_result("RISK", pc.calculate_risk(positions))