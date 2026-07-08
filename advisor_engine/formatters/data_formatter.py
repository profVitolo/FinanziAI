from data_engine.data_engine_models import (
    AssetItem,
    AssetPeriod,
    AssetResult,
    Indicators,
    MarketAnalysisResult,
    MarketData,
    Performance,
    PortfolioExposure,
    PortfolioPosition,
    PortfolioResult,
    PortfolioRisk,
)

from advisor_engine.formatters.utils import (
    format_money,
    format_percent,
    join_lines,
    format_date
)


# ============================================================
# Portfolio
# ============================================================

def format_portfolio(portfolio: PortfolioResult) -> str:
    lines = [
        f"Portfolio value: {format_money(portfolio.portfolio_value, portfolio.base_currency)}",
        f"Base currency: {portfolio.base_currency}",
        "",
        format_portfolio_risk(portfolio.risk),
        "",
        f"Positions ({len(portfolio.positions)}):",
    ]

    for position in portfolio.positions:
        lines.append("")
        lines.append(format_portfolio_position(position))

    lines.append("")
    lines.append(format_portfolio_exposure(portfolio.exposure))

    return join_lines(lines)


def format_portfolio_position(position: PortfolioPosition) -> str:
    lines = [
        format_asset(position.asset),
        f"Quantity: {position.quantity:g}",
        f"Average price: {format_money(position.avg_price, position.currency)}",
        f"Market price: {format_money(position.market_price, position.currency)}",
        f"Market value: {format_money(position.market_value, position.currency)}",
    ]

    if position.market_value_base is not None:
        lines.append(f"Market value (base): {format_money(position.market_value_base, position.currency)}")

    lines.append(format_performance(position.performance, position.currency))

    return join_lines(lines)


def format_performance(performance: Performance, currency: str) -> str:
    lines = [
        f"Cost basis: {format_money(performance.cost_basis, currency)}",
        f"P/L: {format_money(performance.pnl, currency)} ({format_percent(performance.pnl_percent)})",
    ]

    if performance.cost_basis_base is not None:
        lines.append(f"Cost basis (base): {format_money(performance.cost_basis_base, currency)}")

    if performance.pnl_base is not None:
        lines.append(f"P/L (base): {format_money(performance.pnl_base, currency)}")

    return join_lines(lines)


def format_portfolio_risk(risk: PortfolioRisk) -> str:
    return join_lines([
        "Risk:",
        f"- Largest position: {format_percent(risk.largest_position_weight)}",
        f"- Concentration: {risk.concentration_level}",
    ])


def format_portfolio_exposure(exposure: PortfolioExposure) -> str:
    lines = ["Exposure:"]

    sections = [
        ("By symbol", exposure.by_symbol),
        ("By sector", exposure.by_sector),
        ("By country", exposure.by_country),
        ("By currency", exposure.by_currency),
    ]

    for title, values in sections:
        lines.append(title)

        for key, value in values.items():
            lines.append(f"- {key}: {format_percent(value)}")

        lines.append("")

    return join_lines(lines)


# ============================================================
# Asset
# ============================================================

def format_asset_result(asset: AssetResult) -> str:
    return join_lines([
        format_asset(asset.asset),
        format_asset_period(asset.period),
        format_market_data(asset.market_data, asset.asset.currency),
        format_market_analysis(asset.analysis),
        format_indicators(asset.indicators),
    ])


def format_asset(asset: AssetItem) -> str:
    lines = [
        f"Asset: {asset.symbol} ({asset.name})",
        f"Type: {asset.type}",
        f"Exchange: {asset.exchange}",
        f"Currency: {asset.currency}",
        f"Sector: {asset.sector}",
        f"Industry: {asset.industry}",
        f"Country: {asset.country}",
    ]

    if asset.beta is not None:
        lines.append(f"Beta: {asset.beta:.2f}")

    if asset.market_cap is not None:
        lines.append(f"Market cap: {format_money(asset.market_cap, asset.currency)}")

    return join_lines(lines)


def format_asset_period(period: AssetPeriod) -> str:
    return f"Analysis period: {format_date(period.start)} -> {format_date(period.end)}"


def format_market_data(market_data: MarketData, currency: str) -> str:
    lines = [f"Records: {market_data.records}",]

    if market_data.last_close is not None:
        lines.append(f"Last close: {format_money(market_data.last_close, currency)}")

    return join_lines(lines)


def format_market_analysis(analysis: MarketAnalysisResult) -> str:
    return join_lines([
        f"Trend: {analysis.trend.value}",
        f"Volatility: {analysis.volatility_level.value}",
    ])


def format_indicators(indicators: Indicators) -> str:
    lines = []

    if indicators.rsi is not None:
        lines.append(f"RSI: {indicators.rsi:.2f}")

    if indicators.sma20 is not None:
        lines.append(f"SMA20: {indicators.sma20:.2f}")

    if indicators.sma50 is not None:
        lines.append(f"SMA50: {indicators.sma50:.2f}")

    if indicators.daily_volatility is not None:
        lines.append(f"Daily volatility: {format_percent(indicators.daily_volatility)}")

    if indicators.annualized_volatility is not None:
        lines.append(f"Annualized volatility: {format_percent(indicators.annualized_volatility)}")

    if indicators.period_range is not None:
        lines.append(f"Period range: {format_percent(indicators.period_range)}")

    return join_lines(lines)


# ============================================================
# Watchlist
# ============================================================

def format_watchlist(watchlist: list[AssetResult]) -> str:
    return join_lines(
        format_asset_result(asset)
        for asset in watchlist
    )

