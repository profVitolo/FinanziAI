from pathlib import Path
from pprint import pprint
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from data_engine.data_engine import DataEngine

if __name__ == "__main__":

    engine = DataEngine("vault.db")

    print("\n=== PORTFOLIO ANALYSIS ===\n")

    result = engine.analyze_portfolio()

    if result is None:
        print("Nessuna posizione presente")
    else:
        pprint(result)