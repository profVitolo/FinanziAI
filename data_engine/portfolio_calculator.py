from collections import defaultdict
from collections.abc import Callable

from data_engine.data_engine_models import (
    ConcentrationLevel,
    Performance,
    PortfolioRisk,
    PortfolioItem,
    PortfolioPosition
)


class PortfolioCalculator:
    def build_position(self, item: PortfolioItem) -> PortfolioPosition:
        market_value = self._calculate_position_value(item.position.quantity, item.market_price)
        performance = self._calculate_performance(item.position.quantity, item.position.avg_price, item.market_price)

        return PortfolioPosition.from_item(item, market_value=market_value, performance=performance)
    
    def calculate_portfolio_value(self, positions: list[PortfolioPosition]) -> float:
        return sum(position.market_value_base or 0 for position in positions)
    
    def calculate_symbol_exposure(self, positions: list[PortfolioPosition],) -> dict[str, float]:
        return self._calculate_group_exposure(positions, lambda p: p.asset.symbol,)
    
    def calculate_sector_exposure(self, positions: list[PortfolioPosition],) -> dict[str, float]:
        return self._calculate_group_exposure(positions, lambda p: p.asset.sector,)
    
    def calculate_country_exposure(self, positions: list[PortfolioPosition],) -> dict[str, float]:
        return self._calculate_group_exposure(positions, lambda p: p.asset.country,)
    
    def calculate_currency_exposure(self, positions: list[PortfolioPosition],) -> dict[str, float]:
        return self._calculate_group_exposure(positions, lambda p: p.asset.currency,)        
    
    def calculate_risk(self, positions: list[PortfolioPosition]) -> PortfolioRisk:
        if not positions:
            return self._empty_risk()

        portfolio_value = self.calculate_portfolio_value(positions)

        if portfolio_value <= 0:
            return self._empty_risk()

        largest_weight = max(
            self._calculate_weight(
                position.market_value_base,
                portfolio_value
            )
            for position in positions
        )

        level = self._get_concentration_level(largest_weight)

        return PortfolioRisk(largest_position_weight=largest_weight, concentration_level=level)
    
    # METODI PRIVATI

    def _calculate_group_exposure(self, positions: list[PortfolioPosition],key_selector: Callable[[PortfolioPosition], str],) -> dict[str, float]:
        portfolio_value = self.calculate_portfolio_value(positions)

        exposure = defaultdict(float)

        for position in positions:
            key = key_selector(position)
            exposure[key] += (position.market_value_base or 0)

        return {
            key: self._calculate_weight(value, portfolio_value)
            for key, value in exposure.items()
        }
    
    def _calculate_position_value(self, quantity: float | None, market_price: float | None) -> float:
        if quantity is None or market_price is None:
            return 0
        return quantity * market_price

    def _calculate_weight(self, part_value: float | None, whole_value: float) -> float:
        if (part_value is None or whole_value <= 0 or part_value <= 0 ):
            return 0
        return part_value / whole_value * 100

    def _cost_basis(self, quantity, avg_price) -> float:
        return quantity * avg_price
        
    def _pnl(self, cost_basis, market_value) -> float:
        return market_value - cost_basis

    def _pnl_percent(self, pnl, cost_basis) -> float:
        return (pnl / cost_basis) * 100 if cost_basis > 0 else 0
        
    def _calculate_performance(self, quantity: float | None, avg_price: float | None, market_price: float | None, ) -> Performance:
        if (quantity is None or avg_price is None or market_price is None):
            return Performance(cost_basis=0, market_value=0, pnl=0, pnl_percent=0,)

        cost_basis = self._cost_basis(quantity, avg_price)
        market_value = self._calculate_position_value(quantity, market_price)
        pnl = self._pnl(cost_basis, market_value)
        pnl_percent = self._pnl_percent(pnl, cost_basis)

        return Performance(
            cost_basis=cost_basis,
            market_value=market_value,
            pnl=pnl,
            pnl_percent=pnl_percent
        )

    def _empty_risk(self) -> PortfolioRisk:
        return PortfolioRisk(largest_position_weight=0,concentration_level=ConcentrationLevel.LOW)
    
    def _get_concentration_level(self, weight: float) -> ConcentrationLevel:
        if weight > 50:
            return ConcentrationLevel.HIGH
        if weight > 25:
            return ConcentrationLevel.MEDIUM
        return ConcentrationLevel.LOW
        
