class PortfolioAnalysis:

    def calculate_position_value(self, quantity, market_price):
        if quantity is None or market_price is None:
            return 0
        return quantity * market_price

    def calculate_portfolio_value(self, positions):
        total_value = 0

        for position in positions:
            total_value += position["market_value_base"] or 0

        return total_value

    def calculate_asset_weight(self, position_value, portfolio_value):
        if position_value is None or portfolio_value is None:
            return 0
            
        if portfolio_value <= 0 or position_value <= 0:
            return 0

        return (position_value / portfolio_value) * 100

    def calculate_exposure(self, positions):
        portfolio_value = self.calculate_portfolio_value(positions)

        exposure = {}

        for position in positions:
            symbol = position["symbol"]

            exposure[symbol] = self.calculate_asset_weight(position["market_value_base"], portfolio_value)

        return exposure

    def calculate_performance(self, quantity, avg_price, market_price):
        if (quantity is None or avg_price is None or market_price is None):
            return {
                "cost_basis": 0,
                "market_value": 0,
                "pnl": 0,
                "pnl_percent": 0
            }
            
        cost_basis = quantity * avg_price
        market_value = quantity * market_price

        pnl = market_value - cost_basis

        if cost_basis <= 0:
            pnl_percent = 0
        else:
            pnl_percent = (pnl / cost_basis) * 100

        return {
            "cost_basis": cost_basis,
            "market_value": market_value,
            "pnl": pnl,
            "pnl_percent": pnl_percent
        }

    def calculate_risk(self, positions):
        default = {
            "largest_position_weight": 0,
            "concentration_level": "low"
        }
        
        if not positions:
            return default

        portfolio_value = self.calculate_portfolio_value(positions)
        
        if portfolio_value <= 0:
            return default
            
        largest_weight = 0

        for position in positions:
            weight = self.calculate_asset_weight(position["market_value_base"], portfolio_value)

            largest_weight = max(largest_weight, weight)

        if largest_weight > 50:
            level = "high"
        elif largest_weight > 25:
            level = "medium"
        else:
            level = "low"

        return {
            "largest_position_weight": largest_weight,
            "concentration_level": level
        }