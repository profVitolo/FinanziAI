from pathlib import Path
import sys
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from api_test_utils import *
from data_engine.portfolio_analysis import PortfolioAnalysis

pa = PortfolioAnalysis()

print_title("=== TEST PORTFOLIO ANALYSIS ===")

print_result("POSITION VALUE", pa.calculate_position_value(quantity=10, market_price=120))

print_result("PERFORMANCE", pa.calculate_performance(quantity=10, avg_price=100, market_price=120))

positions = [
    {
        "symbol": "AAPL",
        "market_value": 1200,
        "market_value_base": 1200
    },
    {
        "symbol": "MSFT",
        "market_value": 800,
        "market_value_base": 800
    }
]

print_result("PORTFOLIO VALUE", pa.calculate_portfolio_value(positions))
print_result("EXPOSURE", pa.calculate_exposure(positions))
print_result("RISK", pa.calculate_risk(positions))