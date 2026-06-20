from pathlib import Path
import sys
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from api_test_utils import *
from data_engine.data_engine import DataEngine
from database.database_manager import DatabaseManager

database = DatabaseManager()

engine = DataEngine(database)

print_title("\n=== PORTFOLIO ANALYSIS ===\n")

result = engine.analyze_portfolio()

if result is None:
    print("Nessuna posizione presente")
else:
    print_result("", result)