from data_engine.portfolio_analysis import PortfolioAnalysis
from data_engine.portfolio_models import PortfolioResult

class PortfolioAnalyzer:

    def __init__(self, enricher):
        self.analysis = PortfolioAnalysis()
        self.enricher = enricher

    def analyze(self, items):
        if not items:
            return None

        positions = [self._build_position(item) for item in items]

        portfolio_value = self.analysis.calculate_portfolio_value(positions)
        exposure = self.analysis.calculate_exposure(positions)
        risk = self.analysis.calculate_risk(positions)

        return self._build_result(positions, portfolio_value, exposure, risk)

    def _build_position(self, item):
        market_value = self.analysis.calculate_position_value(item.quantity, item.market_price)
        performance = self.analysis.calculate_performance(item.quantity, item.avg_price, item.market_price)

        position = {
            "asset_id": item.asset_id,
            "symbol": item.symbol,
            "name": item.name,
            "type": item.type,
            "sector": item.sector,
            "industry": item.industry,
            "country": item.country,
            "market_cap": item.market_cap,
            "beta": item.beta,
            "quantity": item.quantity,
            "currency": item.currency,
            "avg_price": item.avg_price,
            "market_price": item.market_price,
            "market_value": market_value,
            "performance": performance
        }

        return self.enricher.enrich_position(position)

    def _build_result(self, positions,portfolio_value, exposure,risk):
        return PortfolioResult(
            base_currency=self.enricher.base_currency,
            portfolio_value=portfolio_value,
            positions=positions,
            exposure=exposure,
            risk=risk
        )