from data_manager.asset_data_manager import AssetDataManager
from data_manager.portfolio_data_manager import PortfolioDataManager
from database.database_manager import DatabaseManager

from data_engine.indicators import Indicators
from data_engine.market_analysis import MarketAnalysis
from data_engine.portfolio_analysis import PortfolioAnalysis

from services.exchange_service import ExchangeService


## un solo DataManager → chiudo il DataManager; 
## più DataManager condivisi → chiudo il DatabaseManager (self.database)

class DataEngine:
   
    def __init__(self, database=None):
        self.database = database or DatabaseManager()
        self.asset_data_manager = AssetDataManager(self.database)
        self.portfolio_data_manager = PortfolioDataManager(self.database)
        self.portfolio_analysis = PortfolioAnalysis()

        self.exchange_service = ExchangeService(self.database)
        
    def analyze_asset(self, symbol, start_date=None, end_date=None):
        try:
            asset = self._load_asset(symbol)

            if not asset:
                return None
            
            prices = self._load_prices(asset, start_date, end_date)

            if not prices:
                return None

            close_prices = self._extract_close_prices(prices)
            
            if not close_prices:
                return None
            
            indicators = self._calculate_indicators(close_prices)
            analysis = MarketAnalysis.analyze(indicators)

            return self._build_asset_result(asset, prices, indicators, analysis)
        finally:
            self.database.close()

    def _load_asset(self, symbol):
        return (self.asset_data_manager.get_asset_by_symbol(symbol))
    
    def _get_last_valid_close(self, prices):
        for row in reversed(prices):
            if row["close"] is not None:
                return row["close"]
        return None
    
    def _load_prices(self, asset, start_date=None, end_date=None):
        if asset is None:
            return None

        asset_id = asset["id"]

        return self.asset_data_manager.get_prices(asset_id, start_date, end_date)

    def _extract_close_prices(self, prices):
        return [
            row["close"]
            for row in prices
            if row["close"] is not None
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

    def _build_asset_result(self, asset, prices, indicators, analysis):
        first_date = prices[0]["date"]
        last_date = prices[-1]["date"]
        
        last_close = self._get_last_valid_close(prices)

        return {
             "asset": {
                "id": asset["id"],
                "symbol": asset["symbol"],
                "name": asset["name"],
                "type": asset["type"],
                "currency": asset["currency"],
                "exchange": asset["exchange"]
            },
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
        try:
            positions = self.portfolio_data_manager.get_all_positions()

            if not positions:
                return None

            portfolio_positions = self._build_portfolio_positions(positions)

            return self._build_portfolio_analysis(portfolio_positions)
        finally:
            self.database.close()
    
    def _enrich_performance_with_base_currency(self, performance, currency):
        result = performance.copy()

        try:
            result["cost_basis_base"] = self.exchange_service.convert(performance["cost_basis"], currency)

            result["pnl_base"] = self.exchange_service.convert(performance["pnl"], currency)
        except ValueError:
            result["cost_basis_base"] = None
            result["pnl_base"] = None

        return result
    
    def _build_portfolio_positions(self, positions):
        result = []

        for position in positions:
            asset_id = position["asset_id"]
            quantity = position["quantity"]
            avg_price = position["avg_price"]

            asset = self.asset_data_manager.get_asset_by_id(asset_id)

            if not asset:
                continue

            symbol = asset["symbol"]
            currency = asset["currency"]

            prices = self.asset_data_manager.get_prices(asset_id)

            if not prices:
                continue

            market_price = self._get_last_valid_close(prices)
            market_value = (self.portfolio_analysis.calculate_position_value(quantity, market_price))
            performance = (self.portfolio_analysis.calculate_performance(quantity, avg_price, market_price))
            performance = self._enrich_performance_with_base_currency(performance, currency)
            
            try:
                market_value_base = self.exchange_service.convert(amount=market_value, from_currency=currency)
            except ValueError:
                market_value_base = None
                
            result.append({
                "asset_id": asset_id,
                "symbol": symbol,
                "quantity": quantity,
                "currency": currency,
                "avg_price": avg_price,
                "market_price": market_price,
                "market_value": market_value,
                "market_value_base": market_value_base,
                "performance": performance
            })

        return result

    def _build_portfolio_analysis(self, positions):
        portfolio_value = (self.portfolio_analysis.calculate_portfolio_value(positions))
        exposure = (self.portfolio_analysis.calculate_exposure(positions))
        risk = (self.portfolio_analysis.calculate_risk(positions))

        return {
            "base_currency": self.exchange_service.base_currency,
            "portfolio_value": portfolio_value,
            "positions": positions,
            "exposure": exposure,
            "risk": risk
        }


