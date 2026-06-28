from data_engine.currency_enricher import CurrencyEnricher

from data_engine.portfolio_calculator import PortfolioCalculator
from data_engine.data_engine_models import (
    PortfolioItem,
    PortfolioPosition,
    PortfolioExposure,
    PortfolioResult,
)


class PortfolioAnalyzer:
    def __init__(self, enricher: CurrencyEnricher, calculator: PortfolioCalculator | None = None):
        self.enricher = enricher
        self.calculator = calculator or PortfolioCalculator()

    def analyze(self, items: list[PortfolioItem]) -> PortfolioResult | None:
        if not items:
            return None

        positions = [self.enricher.enrich_position(self._build_position(item)) for item in items]

        return PortfolioResult(
            base_currency=self.enricher.base_currency,
            portfolio_value=self.calculator.calculate_portfolio_value(positions),
            positions=positions,
            exposure=PortfolioExposure(
                by_symbol=self.calculator.calculate_exposure(positions),
            ),
            risk=self.calculator.calculate_risk(positions)
        )

    def _build_position(self, item: PortfolioItem) -> PortfolioPosition:
        market_value = self.calculator.calculate_position_value(item.position.quantity, item.market_price)
        performance = self.calculator.calculate_performance(item.position.quantity, item.position.avg_price, item.market_price)

        return PortfolioPosition.from_item(item, market_value=market_value, performance=performance)