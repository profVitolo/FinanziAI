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

        existing = self.exchange_data_manager.get_rate(from_currency, self.base_currency, rate_date)

        if existing:
            return True
        
        rate = self.collector.fetch_exchange_rate(from_currency, self.base_currency, rate_date)
        
        if rate is None:
            return False

        self.exchange_data_manager.save_rate(from_currency, self.base_currency, rate, rate_date)
        return True

    def get_rate(self, from_currency, rate_date=None):
        from_currency = from_currency.upper()

        if from_currency == self.base_currency:
            return 1.0
        
        self.update_rate(from_currency, rate_date)
        rate = self.exchange_data_manager.get_latest_rate_before(from_currency, self.base_currency, rate_date)
        
        return rate["rate"] if rate else None

    def convert(self, amount, from_currency, date=None):
        rate = self.get_rate(from_currency.upper(), date)

        if rate is None:
            raise ValueError(f"Exchange rate on {date} not available: {from_currency}")
        
        return amount * rate
        
        