from datetime import date
from advisor_engine.advisor_models import AdvisorContext, InvestorProfile
from data_engine.data_engine import DataEngine
from evaluation_engine.evaluation_engine import EvaluationEngine


class AdvisorContextBuilder:
    def __init__(self, data_engine: DataEngine | None = None, evaluation_engine: EvaluationEngine | None = None):
        self._data_engine = data_engine or DataEngine()
        self._evaluation_engine = evaluation_engine or EvaluationEngine()

    def build(self, profile: InvestorProfile) -> AdvisorContext:
        analysis = self._data_engine.analyze_portfolio_full()
        
        if analysis is None:
            raise RuntimeError("Unable to analyze portfolio.")

        portfolio = analysis.portfolio
        portfolio_assets = analysis.assets

        watchlist = self._data_engine.analyze_watchlist() or []

        return AdvisorContext(
            portfolio=portfolio,
            portfolio_evaluation=self._evaluation_engine.evaluate_portfolio(portfolio),
            portfolio_asset_evaluations=self._evaluation_engine.evaluate_assets(portfolio_assets),
            watchlist=watchlist,
            watchlist_evaluations=self._evaluation_engine.evaluate_assets(watchlist),
            investor_profile=profile,
        )