from datetime import date
from dataclasses import replace

from data_engine.data_engine_models import *
from data_engine.portfolio_calculator import PortfolioCalculator


def make_asset(**kwargs) -> AssetItem:
    data = {
        "id": 1,
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "type": "stock",
        "currency": "USD",
        "exchange": "NASDAQ",
        "sector": "Technology",
        "industry": "Consumer Electronics",
        "country": "USA",
        "market_cap": None,
        "beta": None,
        "website": None,
    }
    data.update(kwargs)
    return AssetItem.from_dict(data)

def make_position(**kwargs) -> PositionItem:
    data = {
        "asset_id": 1,
        "quantity": 10,
        "avg_price": 100,
    }
    data.update(kwargs)
    return PositionItem.from_dict(data)

def make_price(**kwargs) -> PriceItem:
    data = {
        "date": date.today(),
        "open": 100,
        "high": 105,
        "low": 98,
        "close": 102,
        "volume": 1_000_000,
    }
    data.update(kwargs)
    return PriceItem.from_dict(data)

def make_portfolio_item(*, asset=None, position=None, market_price=120):
    asset = asset or make_asset()
    position = position or make_position(asset_id=asset.id)

    return PortfolioItem(position=position, asset=asset, market_price=market_price)
    
def make_portfolio_position(*, item=None, asset=None, position=None, market_price=120, market_value_base=None):
    item = item or make_portfolio_item(asset=asset, position=position, market_price=market_price)

    quantity = item.position.quantity
    avg_price = item.position.avg_price
    market_price = item.market_price

    market_value = quantity * market_price
    cost_basis = quantity * avg_price
    pnl = market_value - cost_basis

    performance = Performance(
        cost_basis=cost_basis,
        market_value=market_value,
        pnl=pnl,
        pnl_percent=(pnl / cost_basis * 100) if cost_basis else 0
    )

    position = PortfolioPosition.from_item(
        item=item,
        market_value=market_value,
        performance=performance
    )

    if market_value_base is not None:
        position = replace(position, market_value_base=market_value_base)

    return position

def make_asset_result(
    *,
    asset=None,
    start=date(2025, 1, 1),
    end=date(2026, 1, 1),
    last_close=145.25,
    records=252,
    sma20=140.3,
    sma50=132.8,
    rsi=76.4,
    daily_volatility=0.031,
    annualized_volatility=0.49,
    period_range=112.7,
    trend=Trend.BULLISH,
    volatility_level=VolatilityLevel.HIGH
):
    asset = asset or make_asset()

    return AssetResult(
        asset=asset,
        period=AssetPeriod(
            start=start,
            end=end,
        ),
        market_data=MarketData(
            records=records,
            last_close=last_close
        ),
        indicators=Indicators(
            sma20=sma20,
            sma50=sma50,
            rsi=rsi,
            daily_volatility=daily_volatility,
            annualized_volatility=annualized_volatility,
            period_range=period_range
        ),
        analysis=MarketAnalysisResult(
            trend=trend,
            volatility_level=volatility_level
        )
    )

def make_portfolio_result(*, positions=None, base_currency="EUR"):
    positions = positions or []

    calculator = PortfolioCalculator()

    portfolio_value = calculator.calculate_portfolio_value(positions)

    return PortfolioResult(
        base_currency=base_currency,
        portfolio_value=portfolio_value,
        positions=positions,
        exposure=PortfolioExposure(by_symbol=calculator.calculate_exposure(positions)),
        risk=calculator.calculate_risk(positions)
    )

