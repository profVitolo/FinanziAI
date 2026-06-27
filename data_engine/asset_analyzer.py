from data_engine.indicators import Indicators
from data_engine.market_analysis import MarketAnalysis


class AssetAnalyzer:
    @staticmethod
    def analyze(asset, prices):    
        if not asset or not prices:
            return None

        close_prices = AssetAnalyzer._extract_close_prices(prices)

        if not close_prices:
            return None

        indicators = AssetAnalyzer._calculate_indicators(close_prices)
        analysis = MarketAnalysis.analyze(indicators)

        return AssetAnalyzer._build_result(asset, prices, indicators, analysis)

    @staticmethod
    def _extract_close_prices(prices):
        return [row["close"] for row in prices if row["close"] is not None]

    @staticmethod
    def _calculate_indicators(close_prices):
        return {
            "sma20": Indicators.calculate_sma(close_prices, 20),
            "sma50": Indicators.calculate_sma(close_prices, 50),
            "rsi": Indicators.calculate_rsi(close_prices),
            "daily_volatility":
                Indicators.calculate_daily_volatility(close_prices),
            "annualized_volatility":
                Indicators.calculate_annualized_volatility(close_prices),
            "period_range":
                Indicators.calculate_period_range(close_prices)
        }

    @staticmethod
    def _last_close(prices):
        for row in reversed(prices):
            if row["close"] is not None:
                return row["close"]
        return None

    @staticmethod
    def _build_result(asset, prices, indicators, analysis):
        return {
            "asset": {
                "id": asset["id"],
                "symbol": asset["symbol"],
                "name": asset["name"],
                "type": asset["type"],
                "currency": asset["currency"],
                "exchange": asset["exchange"],
                "sector": asset["sector"],
                "industry": asset["industry"],
                "country": asset["country"],
                "market_cap": asset["market_cap"],
                "beta": asset["beta"],
                "website": asset["website"]
            },
            "period": {
                "start": prices[0]["date"],
                "end": prices[-1]["date"]
            },
            "market_data": {
                "records": len(prices),
                "last_close": AssetAnalyzer._last_close(prices)
            },
            "indicators": indicators,
            "analysis": analysis
        }