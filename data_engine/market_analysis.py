class MarketAnalysis:

    @staticmethod
    def analyze(indicators):
        return {
            "trend": MarketAnalysis.analyze_trend(indicators),
            "volatility_level": MarketAnalysis.analyze_volatility(indicators)
        }

    @staticmethod
    def analyze_trend(indicators):
        sma20 = indicators.get("sma20")
        sma50 = indicators.get("sma50")

        if sma20 is None or sma50 is None:
            return "unknown"

        if sma20 > sma50:
            return "bullish"

        if sma20 < sma50:
            return "bearish"

        return "neutral"

    @staticmethod
    def analyze_volatility(indicators):
        volatility = indicators.get("annualized_volatility")

        if volatility is None:
            return "unknown"

        if volatility < 0.10:
            return "low"

        if volatility < 0.25:
            return "medium"

        return "high"