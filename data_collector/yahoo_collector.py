import yfinance as yf
from datetime import datetime, timedelta

class YahooCollector:

    def __init__(self):
        pass

    def fetch_asset_info(self, symbol):
        ticker = yf.Ticker(symbol)

        info = ticker.info

        return {
            "symbol": symbol,
            "name": info.get("longName"),
            "type": info.get("quoteType"),
            "currency": info.get("currency"),
            "exchange": info.get("exchange")
        }
        
    def fetch_prices(self, symbol, start_date=None, end_date=None):
        ticker = yf.Ticker(symbol)

        data = ticker.history(start=start_date, end=end_date)

        prices = []

        for date, row in data.iterrows():
            prices.append({
                "date": date.strftime("%Y-%m-%d"),
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": float(row["Volume"])
            })

        return prices
        
    def fetch_exchange_rate(self, from_currency, to_currency, rate_date=None):
        if from_currency == to_currency:
            return 1.0
  
        symbol = f"{from_currency.upper()}{to_currency.upper()}=X"

        ticker = yf.Ticker(symbol)
        
        if rate_date is None:
            data = ticker.history(period="1d")
        else:
            start = rate_date
            end = (datetime.strptime(rate_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")

            data = ticker.history(start=start, end=end)

        if data.empty:
            return None

        return float(data["Close"].iloc[-1])