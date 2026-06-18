from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent

import sys
sys.path.insert(0, str(ROOT_DIR))

from database.database_manager import DatabaseManager
from data_manager.exchange_data_manager import ExchangeDataManager
from data_collector.exchanger import Exchanger
from api_test_utils import print_dict, print_value, print_collection

database = DatabaseManager()

try:
    database.begin_transaction()

    exchange_data_manager = ExchangeDataManager(database)
    exchanger = Exchanger(exchange_data_manager)

    print("\n=== UPDATE RATES ===")

    exchanger.update_rate("USD")
    exchanger.update_rate("GBP")

    print_value("USD LATEST RATE", exchanger.get_rate("USD"))
    print_value("GBP LATEST RATE", exchanger.get_rate("GBP"))

    print_value("100 USD IN EUR", exchanger.convert(100, "USD"))
    print_value("100 GBP IN EUR", exchanger.convert(100, "GBP"))

    print_dict(
        "USD RATE 2025-01-01",
        exchange_data_manager.get_latest_rate_before("USD", "EUR", "2025-01-01")
    )

    print_dict(
        "USD RATE 2025-06-01",
        exchange_data_manager.get_latest_rate_before("USD", "EUR", "2025-06-01")
    )

    print_collection(
        "STORED RATES",
        exchange_data_manager.get_all_rates()
    )

    database.commit()

except Exception:
    database.rollback()
    raise

finally:
    database.close()

print_value(
    "USD/EUR 2026-06-12-FRI",
    exchanger.collector.fetch_exchange_rate("USD", "EUR", "2026-06-12")
)

print_value(
    "USD/EUR 2026-06-13-SAT",
    exchanger.collector.fetch_exchange_rate("USD", "EUR", "2026-06-13")
)

print_value(
    "USD/EUR 2026-06-14-SUN",
    exchanger.collector.fetch_exchange_rate("USD", "EUR", "2026-06-14")
)