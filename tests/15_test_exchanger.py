from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

import sys
sys.path.insert(0, str(ROOT_DIR))

from database.database_manager import DatabaseManager
from data_manager.exchange_data_manager import ExchangeDataManager
from data_collector.exchanger import Exchanger

database = DatabaseManager()

exchange_data_manager = ExchangeDataManager(database)
exchanger = Exchanger(exchange_data_manager)

print("=== EUR -> EUR ===")
print(exchanger.convert(100, "EUR"))

print("\n=== USD RATE ===")
print(exchanger.get_latest_rate("USD"))

print("\n=== 100 USD IN EUR ===")
print(exchanger.convert(100, "USD"))

print("\n=== GBP RATE ===")
print(exchanger.get_latest_rate("GBP"))

print("\n=== 100 GBP IN EUR ===")
print(exchanger.convert(100, "GBP"))

print("\n=== STORED RATES ===")
for rate in exchange_data_manager.get_all_rates():
    print(rate)