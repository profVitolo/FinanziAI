from dataclasses import replace

from data_engine.data_engine_models import Performance, PortfolioPosition
from services.exchange_service import ExchangeService


class CurrencyEnricher:
    def __init__(self, exchange_service: ExchangeService):
        self.exchange_service = exchange_service
        self.base_currency = exchange_service.base_currency

    def enrich_position(self, position: PortfolioPosition) -> PortfolioPosition:
        return replace(
            position,
            performance=self._enrich_performance(
                position.performance,
                position.currency,
            ),
            market_value_base=self.convert(
                position.market_value,
                position.currency,
            ),
        )

    def enrich_positions(self, positions: list[PortfolioPosition]) -> list[PortfolioPosition]:
        return [self.enrich_position(position) for position in positions]

    def _enrich_performance(self, performance: Performance, currency: str) -> Performance:
        return replace(
            performance,
            cost_basis_base=self.convert(performance.cost_basis, currency),
            pnl_base=self.convert(performance.pnl,currency)
        )

    def convert(self, amount: float | None, from_currency: str) -> float | None:
        if amount is None:
            return None

        try:
            return self.exchange_service.convert(amount, from_currency)
        except ValueError:
            return None