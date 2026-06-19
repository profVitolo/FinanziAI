from datetime import date, timedelta

from data_collector.yahoo_collector import YahooCollector
from data_manager.exchange_data_manager import ExchangeDataManager
from database.database_manager import DatabaseManager

from config import BASE_CURRENCY

class ExchangeService:

    def __init__(self, database=None):
        self.database = database or DatabaseManager()
        self.exchange_data_manager = ExchangeDataManager(self.database)
        self.collector = YahooCollector()
        self.base_currency = BASE_CURRENCY
        
    def convert(self, amount, from_currency, to_currency=BASE_CURRENCY, rate_date=None):
        if from_currency.upper() == to_currency.upper():
            return amount

        rate = self.get_latest_rate(from_currency, to_currency,rate_date)

        if rate is None:
            raise ValueError(f"Exchange rate not available: {from_currency}->{to_currency} on {rate_date}")

        return amount * rate["rate"]
    
    def get_missing_dates(self, from_currency, to_currency, start_date, end_date=None):
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        if end_date is None:
            end_date = date.today().isoformat()

        current_date = date.fromisoformat(start_date)
        end_date = date.fromisoformat(end_date)

        missing_dates = []

        while current_date <= end_date:
            rate_date = current_date.isoformat()

            rate = self.exchange_data_manager.get_rate(from_currency, to_currency, rate_date)

            if rate is None:
                missing_dates.append(rate_date)

            current_date += timedelta(days=1)

        return missing_dates
    
    def sync_rate(self, from_currency, to_currency, rate_date=None):
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        if from_currency == to_currency:
            return True

        if rate_date is None:
            rate_date = date.today().isoformat()

        existing = self.exchange_data_manager.get_rate(from_currency, to_currency, rate_date)

        if existing:
            return True

        rate = self.collector.fetch_exchange_rate(from_currency, to_currency, rate_date)

        if rate is None:
            return False

        self.exchange_data_manager.save_rate(from_currency, to_currency, rate, rate_date)

        return True

    def sync_rates(self, from_currency, to_currency, start_date, end_date=None):
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        if from_currency == to_currency:
            return {
                "processed": 0,
                "saved": 0,
                "failed": 0
            }

        if end_date is None:
            end_date = date.today().isoformat()

        current_date = date.fromisoformat(start_date)
        end_date = date.fromisoformat(end_date)

        processed = 0
        saved = 0
        failed = 0
        unavailable_dates = []
        
        while current_date <= end_date:
            rate_date = current_date.isoformat()

            success = self.sync_rate(from_currency, to_currency, rate_date)
            processed += 1

            if success:
                saved += 1
            else:
                failed += 1
                unavailable_dates.append(rate_date)

            current_date += timedelta(days=1)

        return {
            "processed": processed,
            "saved": saved,
            "failed": failed,
            "unavailable_dates": unavailable_dates
        }
    
    def get_rates(self, from_currency=None, to_currency=None, start_date=None, end_date=None):
        if to_currency is not None:
            to_currency = to_currency.upper()
            
        if from_currency is not None:
            from_currency = from_currency.upper()
            
        return self.exchange_data_manager.get_rates(
            from_currency=from_currency,
            to_currency=to_currency,
            start_date=start_date,
            end_date=end_date
        )

    def get_rate(self, from_currency, to_currency, rate_date=None):
        if rate_date is None:
            return self.get_latest_rate(from_currency.upper(), to_currency.upper())

        return self.exchange_data_manager.get_rate(from_currency.upper(),to_currency.upper(), rate_date)

    def get_latest_rate(self, from_currency, to_currency,rate_date=None):
        return self.exchange_data_manager.get_latest_rate_before(
            from_currency.upper(), 
            to_currency.upper(),
            rate_date
        )
    