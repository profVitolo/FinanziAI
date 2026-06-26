from pathlib import Path
import sys
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from api_test_utils import *
from data_engine.data_engine import DataEngine
from database.database_manager import DatabaseManager

database = DatabaseManager()
engine = DataEngine(database)

print_title("=== DATA ENGINE TEST ===")

print_result("AAPL ANALYSIS", engine.analyze_asset("AAPL"))

print_result("S&P500 ANALYSIS",engine.analyze_asset("^GSPC"))

print_result("PORTFOLIO ANALYSIS",engine.analyze_portfolio())

engine.close()