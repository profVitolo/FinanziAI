from database.database_manager import DatabaseManager
from services.exchange_service import ExchangeService

from data_engine.data_supplier import DataSupplier
from data_engine.asset_analyzer import AssetAnalyzer
from data_engine.currency_enricher import CurrencyEnricher
from data_engine.portfolio_models import PortfolioItem, PortfolioResult
from data_engine.portfolio_analyzer import PortfolioAnalyzer


class DataEngine:
    def __init__(self, database=None):
        self.database = database or DatabaseManager()
        self.supplier = DataSupplier(self.database)
        self.exchange_service = ExchangeService(self.database)
        self.asset_analyzer = AssetAnalyzer()
        self.enricher = CurrencyEnricher(self.exchange_service)
        self.portfolio_analyzer = PortfolioAnalyzer(self.enricher)

    def close(self):
        self.supplier.close()

    def analyze_portfolio_full(self):
        portfolio = self.analyze_portfolio()

        if portfolio is None:
            return None

        symbols = (position["symbol"] for position in portfolio.positions)

        return {"portfolio": portfolio, "assets": self.analyze_assets(symbols)}

    def analyze_assets(self, symbols):
        return [analysis for symbol in symbols if (analysis := self.analyze_asset(symbol)) is not None]

    def analyze_asset(self, symbol, start_date=None, end_date=None):
        asset = self.supplier.get_asset_by_symbol(symbol)

        if asset is None:
            return None

        prices = self.supplier.get_prices(asset["id"],start_date,end_date)

        return self.asset_analyzer.analyze(asset, prices)

    def analyze_portfolio(self):
        raw_positions = self.supplier.get_portfolio_positions()

        portfolio_items = []

        for raw_position in raw_positions:

            asset = self.supplier.get_asset_by_id(raw_position["asset_id"])
            if asset is None:
                continue

            prices = self.supplier.get_prices(asset["id"])
            if not prices:
                continue

            portfolio_items.append(
                PortfolioItem(
                    position=raw_position,
                    asset=asset,
                    market_price=self.supplier.get_last_close(prices)
                )
            )

        return self.portfolio_analyzer.analyze(portfolio_items)