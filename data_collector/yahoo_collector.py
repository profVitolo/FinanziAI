import yfinance as yf


class YahooCollector:

    def __init__(self):
        pass

    def fetch_prices(self, symbol, start_date=None, end_date=None):
        """
        Scarica dati OHLC da Yahoo Finance.

        Returns:
            lista di dict:
            [
                {
                    "date": "YYYY-MM-DD",
                    "open": float,
                    "high": float,
                    "low": float,
                    "close": float,
                    "volume": float
                }
            ]
        """

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