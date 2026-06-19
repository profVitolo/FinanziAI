from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent

import sys
sys.path.insert(0, str(ROOT_DIR))

from pprint import pprint
from data_engine.data_engine import DataEngine
from database.database_manager import DatabaseManager

database = DatabaseManager()

engine = DataEngine(database)

print("\n=== PORTFOLIO ANALYSIS ===\n")

result = engine.analyze_portfolio()

if result is None:
    print("Nessuna posizione presente")
else:
    pprint(result)