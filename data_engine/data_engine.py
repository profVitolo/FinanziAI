from database.database_manager import DatabaseManager
from services.exchange_service import ExchangeService

from data_engine.asset_analyzer import AssetAnalyzer
from data_engine.currency_enricher import CurrencyEnricher
from data_engine.data_supplier import DataSupplier
from data_engine.data_engine_models import (
    AssetResult,
    PortfolioItem,
    PortfolioResult,
)
from data_engine.portfolio_analyzer import PortfolioAnalyzer


class DataEngine:
    def __init__(self, database=None):
        self.database = database or DatabaseManager()

        self.supplier = DataSupplier(self.database)

        exchange_service = ExchangeService(self.database)
        enricher = CurrencyEnricher(exchange_service)

        self.asset_analyzer = AssetAnalyzer()
        self.portfolio_analyzer = PortfolioAnalyzer(enricher)

    def close(self):
        self.supplier.close()

    # ------------------------------------------------------------------
    # Assets
    # ------------------------------------------------------------------

    def analyze_asset(self, symbol: str, start_date=None, end_date=None,) -> AssetResult | None:
        asset = self.supplier.get_asset_by_symbol(symbol)
        if asset is None:
            return None

        prices = self.supplier.get_prices(asset.id, start_date, end_date)

        return self.asset_analyzer.analyze(asset, prices)

    def analyze_assets(self, symbols) -> list[AssetResult]:

        return [analysis for symbol in symbols if (analysis := self.analyze_asset(symbol)) is not None]

    # ------------------------------------------------------------------
    # Portfolio
    # ------------------------------------------------------------------

    def analyze_portfolio(self) -> PortfolioResult | None:
        items = [
            item
            for position in self.supplier.get_portfolio_positions()
            if (item := self._build_portfolio_item(position)) is not None
        ]

        return self.portfolio_analyzer.analyze(items)

    def analyze_portfolio_full(self):
        portfolio = self.analyze_portfolio()
        if portfolio is None:
            return None

        return {
            "portfolio": portfolio,
            "assets": self.analyze_assets(
                position.asset.symbol
                for position in portfolio.positions
            ),
        }

    # ------------------------------------------------------------------
    # Builders
    # ------------------------------------------------------------------

    def _build_portfolio_item(self, position) -> PortfolioItem | None:
        asset = self.supplier.get_asset_by_id(position.asset_id)
        if asset is None:
            return None

        prices = self.supplier.get_prices(asset.id)
        if not prices:
            return None

        return PortfolioItem(
            position=position,
            asset=asset,
            market_price=prices[-1].close,
        )