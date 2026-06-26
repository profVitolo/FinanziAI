from advisor.asset_rules import AssetRules
from advisor.portfolio_rules import PortfolioRules
from advisor.advisor_models import AdvisorResult


class AdvisorEngine:

    @classmethod
    def evaluate(cls, portfolio, assets):
        return AdvisorResult(
            portfolio=cls.evaluate_portfolio(portfolio),
            assets=[
                cls.evaluate_asset(asset)
                for asset in assets
            ]
        )
    
    @staticmethod
    def evaluate_portfolio(portfolio):
        return PortfolioRules.evaluate(portfolio)
    
    @staticmethod
    def evaluate_asset(asset):
        return AssetRules.evaluate(asset)
    