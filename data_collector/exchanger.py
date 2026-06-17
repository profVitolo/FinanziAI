from datetime import date

from data_collector.yahoo_collector import YahooCollector
from data_manager.exchange_data_manager import ExchangeDataManager

from config import BASE_CURRENCY

class Exchanger:
    def __init__(self, exchange_data_manager, base_currency=BASE_CURRENCY):
        self.exchange_data_manager = exchange_data_manager
        self.collector = YahooCollector()
        self.base_currency = base_currency.upper()

    def set_base_currency(self, currency):
        self.base_currency = currency.upper()

    def update_rate(self, from_currency, rate_date=None):
        from_currency = from_currency.upper()

        if from_currency == self.base_currency:
            return

        if rate_date is None:
            rate_date = date.today().isoformat()

        existing = self.exchange_data_manager.get_latest_rate_before(from_currency, self.base_currency, rate_date)

        if existing:
            return

        if rate is None:
            raise ValueError(
                f"Exchange rate not available: " 
                f"{from_currency}/{self.base_currency} ({rate_date})"
            )

        self.exchange_data_manager.save_rate(from_currency, self.base_currency, rate, rate_date)

    def get_latest_rate(self, from_currency):
        from_currency = from_currency.upper()

        if from_currency == self.base_currency:
            return 1.0

        rate = self.exchange_data_manager.get_latest_rate(from_currency, self.base_currency)

        if rate is None:
            self.update_rate(from_currency)

            rate = self.exchange_data_manager.get_latest_rate(from_currency, self.base_currency)

        return rate["rate"]

    def convert(self, amount, from_currency):
        rate = self.get_latest_rate(from_currency.upper())

        if rate is None:
            raise ValueError(f"Exchange rate not available: {from_currency}")
        
        return amount * rate
        
        