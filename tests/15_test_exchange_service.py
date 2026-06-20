from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from database.database_manager import DatabaseManager
from services.exchange_service import ExchangeService
from api_test_utils import *


database = DatabaseManager()
exchange_service = ExchangeService(database)

print_title("=== TEST EXCHANGE SERVIVE ===")
print("\n=== COLLECTOR FETCHES ===")

print_value(
    "USD/EUR 2026-06-12-FRI",
    exchange_service.collector.fetch_exchange_rate(
        "USD",
        "EUR",
        "2026-06-12"
    )
)

print_value(
    "USD/EUR 2026-06-13-SAT",
    exchange_service.collector.fetch_exchange_rate(
        "USD",
        "EUR",
        "2026-06-13"
    )
)

print_value(
    "USD/EUR 2026-06-14-SUN",
    exchange_service.collector.fetch_exchange_rate(
        "USD",
        "EUR",
        "2026-06-14"
    )
)

print("\n=== SERVICE TESTS - SYNC RATES ===")

exchange_service.sync_rate("USD", "EUR")
exchange_service.sync_rate("GBP", "EUR")

exchange_service.sync_rates("GBP", "EUR", "2026-06-01", "2026-06-12")

print_dict("USD LATEST RATE", exchange_service.get_latest_rate("USD", "EUR"))

print_dict("GBP LATEST RATE", exchange_service.get_latest_rate("GBP", "EUR"))

print_value("100 USD IN EUR", exchange_service.convert(100, "USD"))

print_value("100 GBP IN EUR", exchange_service.convert(100, "GBP"))

print_dict(
    "USD RATE 2025-01-01",
    exchange_service.get_latest_rate(
        "USD",
        "EUR",
        "2025-01-01"
    )
)

print_dict(
    "USD RATE 2025-06-01",
    exchange_service.get_latest_rate(
        "USD",
        "EUR",
        "2025-06-01"
    )
)

print_collection("STORED RATES", exchange_service.get_rates())

print_collection(
    "MISSING DATES",
    exchange_service.get_missing_dates(
        "USD",
        "EUR",
        "2026-06-01",
        "2026-06-30"
    )
)
