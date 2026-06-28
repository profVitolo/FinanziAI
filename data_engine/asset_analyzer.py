from data_engine.data_engine_models import (
    AssetItem,
    AssetPeriod,
    AssetResult,
    Indicators,
    MarketData,
    PriceItem,
)
from data_engine.indicators_calculator import IndicatorsCalculator
from data_engine.market_analyzer import MarketAnalyzer


class AssetAnalyzer:
    def __init__(self, indicators_calculator: IndicatorsCalculator | None = None, market_analyzer: MarketAnalyzer | None = None):
        self.indicators_calculator = indicators_calculator or IndicatorsCalculator()
        self.market_analyzer = market_analyzer or MarketAnalyzer()

    def analyze(self, asset: AssetItem, prices: list[PriceItem],) -> AssetResult | None:
        if not prices:
            return None

        close_prices = [price.close for price in prices if price.close is not None]

        if not close_prices:
            return None

        indicators = self._calculate_indicators(close_prices)

        return AssetResult(
            asset=asset,
            period=AssetPeriod(
                start=prices[0].date,
                end=prices[-1].date,
            ),
            market_data=MarketData(
                records=len(prices),
                last_close=next(
                    (
                        price.close
                        for price in reversed(prices)
                        if price.close is not None
                    ),
                    None,
                ),
            ),
            indicators=indicators,
            analysis=self.market_analyzer.analyze(indicators),
        )

    def _calculate_indicators(self, close_prices: list[float]) -> Indicators:
        daily = self.indicators_calculator.daily_volatility(close_prices)

        return Indicators(
            sma20=self.indicators_calculator.sma(close_prices, 20),
            sma50=self.indicators_calculator.sma(close_prices, 50),
            rsi=self.indicators_calculator.rsi(close_prices),
            daily_volatility=daily,
            annualized_volatility=self.indicators_calculator.annualized_volatility(daily),
            period_range=self.indicators_calculator.period_range(close_prices),
        )