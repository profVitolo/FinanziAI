from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from data_engine.data_engine import DataEngine

DB_PATH = "vault.db"

engine = DataEngine(DB_PATH)

print("=== AAPL ANALYSIS ===")
print(engine.analyze_asset("AAPL"))

print("\n=== S&P500 ANALYSIS ===")
print(engine.analyze_asset("^GSPC"))

print("\n=== PORTFOLIO ANALYSIS ===")
print(engine.analyze_portfolio())