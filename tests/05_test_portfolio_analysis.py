from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent

import sys
sys.path.insert(0, str(ROOT_DIR))

from data_engine.portfolio_analysis import PortfolioAnalysis

pa = PortfolioAnalysis()

print("=== POSITION VALUE ===")
print(pa.calculate_position_value(quantity=10, market_price=120))

print("=== PERFORMANCE ===")
print(pa.calculate_performance(quantity=10, avg_price=100, market_price=120))

positions = [
    {
        "symbol": "AAPL",
        "market_value": 1200
    },
    {
        "symbol": "MSFT",
        "market_value": 800
    }
]

print("=== PORTFOLIO VALUE ===")
print(pa.calculate_portfolio_value(positions))

print("=== EXPOSURE ===")
print(pa.calculate_exposure(positions))

print("=== RISK ===")
print(pa.calculate_risk(positions))