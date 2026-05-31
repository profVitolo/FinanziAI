from data_manager.asset_data_manager import AssetDataManager
from data_manager.portfolio_data_manager import PortfolioDataManager

from data_engine.indicators import Indicators
from data_engine.market_analysis import MarketAnalysis
from data_engine.portfolio_analysis import PortfolioAnalysis


class DataEngine:

    def __init__(self, db_path):
        self.asset_data_manager = AssetDataManager(db_path)
        self.portfolio_data_manager = PortfolioDataManager(db_path)
        self.portfolio_analysis = PortfolioAnalysis()
        
    def analyze_asset(self, symbol, start_date=None, end_date=None):
        prices = self._load_prices(symbol, start_date, end_date)

        if not prices:
            return None

        close_prices = self._extract_close_prices(prices)
        indicators = self._calculate_indicators(close_prices)
        analysis = MarketAnalysis.analyze(indicators)

        return self._build_asset_result(symbol, prices, indicators, analysis)

    def _load_prices(self, symbol, start_date=None, end_date=None):
        asset = self.asset_data_manager.get_asset_by_symbol(symbol)

        if asset is None:
            return None

        asset_id = asset[0]

        return self.asset_data_manager.get_prices(asset_id, start_date, end_date)

    def _extract_close_prices(self, prices):
        return [
            row[4]
            for row in prices
            if row[4] is not None
        ]

    def _calculate_indicators(self, close_prices):
        return {
            "sma20": Indicators.calculate_sma(close_prices, 20),
            "sma50": Indicators.calculate_sma(close_prices, 50),
            "rsi": Indicators.calculate_rsi(close_prices),
            "daily_volatility": Indicators.calculate_daily_volatility(close_prices),
            "annualized_volatility": Indicators.calculate_annualized_volatility(close_prices),
            "period_range": Indicators.calculate_period_range(close_prices)
        }

    def _build_asset_result(self, symbol, prices, indicators, analysis):
        first_date = prices[0][0]
        last_date = prices[-1][0]
        last_close = prices[-1][4]

        return {
            "symbol": symbol,
            "period": {
                "start": first_date,
                "end": last_date
            },
            "market_data": {
                "records": len(prices),
                "last_close": last_close
            },
            "indicators": indicators,
            "analysis": analysis
        }

    def analyze_portfolio(self):
        positions = self.portfolio_data_manager.get_all_positions()

        if not positions:
            return None

        portfolio_positions = self._build_portfolio_positions(positions)

        return self._build_portfolio_analysis(portfolio_positions)
        
    def _build_portfolio_positions(self, positions):
        result = []

        for position in positions:
            asset_id = position[1]
            quantity = position[2]
            avg_price = position[3]

            asset = self.asset_data_manager.get_asset_by_id(asset_id)

            if not asset:
                continue

            symbol = asset[1]

            prices = self.asset_data_manager.get_prices(asset_id)

            if not prices:
                continue

            market_price = prices[-1][4]

            market_value = (
                self.portfolio_analysis
                .calculate_position_value(
                    quantity,
                    market_price
                )
            )

            performance = (
                self.portfolio_analysis
                .calculate_performance(
                    quantity,
                    avg_price,
                    market_price
                )
            )

            result.append({
                "asset_id": asset_id,
                "symbol": symbol,
                "quantity": quantity,
                "avg_price": avg_price,
                "market_price": market_price,
                "market_value": market_value,
                "performance": performance
            })

        return result

    def _build_portfolio_analysis(self, positions):
        portfolio_value = (
            self.portfolio_analysis
            .calculate_portfolio_value(
                positions
            )
        )

        exposure = (
            self.portfolio_analysis
            .calculate_exposure(
                positions
            )
        )

        risk = (
            self.portfolio_analysis
            .calculate_risk(
                positions
            )
        )

        return {
            "portfolio_value": portfolio_value,
            "positions": positions,
            "exposure": exposure,
            "risk": risk
        }


