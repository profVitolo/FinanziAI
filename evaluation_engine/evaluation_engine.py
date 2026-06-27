from evaluation_engine.asset_evaluator import AssetEvaluator
from evaluation_engine.portfolio_evaluator import PortfolioEvaluator
from evaluation_engine.evaluation_models import EvaluationReport


class EvaluationEngine:

    """
    @classmethod
    def build_evaluation_reports(cls, portfolio, assets):
        return EvaluationReport(
            portfolio=cls.evaluate_portfolio(portfolio),
            assets=[
                cls.evaluate_asset(asset)
                for asset in assets
            ]
        )
    """
    
    @staticmethod
    def evaluate_portfolio(portfolio):
        return PortfolioEvaluator.evaluate(portfolio)
    
    @staticmethod
    def evaluate_asset(asset):
        return AssetEvaluator.evaluate(asset)
    