from datetime import date

from data_collector.yahoo_collector import YahooCollector
from data_manager.exchange_data_manager import ExchangeDataManager


class Exchanger:
    def __init__(self, exchange_data_manager, base_currency="EUR"):
        self.exchange_data_manager = exchange_data_manager
        self.collector = YahooCollector()
        self.base_currency = base_currency

    def set_base_currency(self, currency):
        self.base_currency = currency.upper()

    def update_rate(self, from_currency):
        from_currency = from_currency.upper()

        if from_currency == self.base_currency:
            return

        today = date.today().isoformat()

        existing = self.exchange_data_manager.get_rate(from_currency, self.base_currency, today)

        if existing:
            return

        rate = self.collector.fetch_exchange_rate(from_currency, self.base_currency)

        self.exchange_data_manager.save_rate(from_currency, self.base_currency, rate, today)

    def get_latest_rate(self, from_currency):
        from_currency = from_currency.upper()

        if from_currency == self.base_currency:
            return 1.0

        rate = self.exchange_data_manager.get_latest_rate(from_currency, self.base_currency)

        if rate is None:
            self.update_rate(from_currency)

            rate = self.exchange_data_manager.get_latest_rate(from_currency, self.base_currency)

        return rate

    def convert(self, amount, from_currency):
        rate = self.get_latest_rate(from_currency)

        if rate is None:
            raise ValueError(f"Exchange rate not available: {from_currency}")

        return amount * rate
        
        