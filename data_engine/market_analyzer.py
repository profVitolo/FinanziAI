from data_engine.data_engine_models import (
    Indicators,
    MarketAnalysisResult,
    Trend,
    VolatilityLevel,
)


class MarketAnalyzer:

    def analyze(self, indicators: Indicators) -> MarketAnalysisResult:
        return MarketAnalysisResult(
            trend=self.analyze_trend(indicators),
            volatility_level=self.analyze_volatility(indicators),
        )

    def analyze_trend(self, indicators: Indicators) -> Trend:
        if indicators.sma20 is None or indicators.sma50 is None:
            return Trend.UNKNOWN
        if indicators.sma20 > indicators.sma50:
            return Trend.BULLISH
        if indicators.sma20 < indicators.sma50:
            return Trend.BEARISH
        return Trend.NEUTRAL

    def analyze_volatility(self, indicators: Indicators,) -> VolatilityLevel:
        volatility = indicators.annualized_volatility

        if volatility is None:
            return VolatilityLevel.UNKNOWN
        if volatility < 0.10:
            return VolatilityLevel.LOW
        if volatility < 0.25:
            return VolatilityLevel.MEDIUM

        return VolatilityLevel.HIGH