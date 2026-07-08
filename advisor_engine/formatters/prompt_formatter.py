from advisor_engine.advisor_models import AdvisorContext, PromptContext
from advisor_engine.formatters.data_formatter import format_portfolio, format_watchlist
from advisor_engine.formatters.evaluation_formatter import format_portfolio_evaluation, format_asset_evaluations


class PromptFormatter:

    @staticmethod
    def format(context: AdvisorContext) -> PromptContext:
        return PromptContext(
            current_date=context.current_date.isoformat(),
            investor_profile=context.investor_profile.value,
            portfolio=format_portfolio(context.portfolio),
            portfolio_evaluation=format_portfolio_evaluation(context.portfolio_evaluation),
            portfolio_asset_evaluations=format_asset_evaluations(context.portfolio_asset_evaluations),
            watchlist=format_watchlist(context.watchlist),
            watchlist_evaluations=format_asset_evaluations(context.watchlist_evaluations),
        )