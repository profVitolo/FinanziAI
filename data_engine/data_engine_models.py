from datetime import date
from dataclasses import dataclass
from enum import StrEnum


"""
    INDICATORS CALCULATOR CLASSES
"""

class RsiMethod(StrEnum):
    WILDER = "wilder"
    SIMPLE = "simple"
    

"""
    PORTFOLIO ANALYSIS CLASSES
"""

class ConcentrationLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    
@dataclass(frozen=True)
class PortfolioRisk:
    largest_position_weight: float
    concentration_level: ConcentrationLevel


"""
    MARKET ANALYZER CLASSES
"""

class Trend(StrEnum):
    UNKNOWN = "unknown"
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"


class VolatilityLevel(StrEnum):
    UNKNOWN = "unknown"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class MarketAnalysisResult:
    trend: Trend
    volatility_level: VolatilityLevel
    
    
"""
    ASSET ANALYZER CLASSES
"""

@dataclass(frozen=True)
class AssetItem:
    """
    DTO utilizzata dal AssetAnalyzer.

    Rappresenta tutti gli ingredienti necessari per costruire
    la descrizione completa di un asset.
    """
    id: int
    symbol: str
    name: str
    type: str
    currency: str
    exchange: str
    sector: str
    industry: str
    country: str
    market_cap: float | None
    beta: float | None
    website: str | None
    
    @classmethod
    def from_dict(cls, data: dict) -> "AssetItem":
        return cls(
            id=data["id"],
            symbol=data["symbol"],
            name=data["name"],
            type=data["type"],
            currency=data["currency"],
            exchange=data["exchange"],
            sector=data["sector"],
            industry=data["industry"],
            country=data["country"],
            market_cap=data["market_cap"],
            beta=data["beta"],
            website=data["website"]
        )


@dataclass(frozen=True)
class AssetPeriod:
    start: date
    end: date


@dataclass(frozen=True)
class MarketData:
    records: int
    last_close: float | None


@dataclass(frozen=True)
class Indicators:
    sma20: float | None
    sma50: float | None
    rsi: float | None
    daily_volatility: float | None
    annualized_volatility: float | None
    period_range: float | None
    
    
@dataclass(frozen=True)
class AssetResult:
    asset: AssetItem
    period: AssetPeriod
    market_data: MarketData
    indicators: Indicators
    analysis: MarketAnalysisResult    
   

@dataclass(frozen=True)
class PriceItem:
    date: date
    open: float | None
    high: float | None
    low: float | None
    close: float | None
    volume: float | None
    
    @classmethod
    def from_dict(cls, data: dict) -> "PriceItem":
        return cls(
            date=data["date"],
            open=data["open"],
            high=data["high"],
            low=data["low"],
            close=data["close"],
            volume=data["volume"]
        )
    

"""
    PORTFOLIO ANALYZER CLASSeS
"""

@dataclass(frozen=True)
class PositionItem:
    asset_id: int
    quantity: float
    avg_price: float
    
    @classmethod
    def from_dict(cls, data: dict) -> "PositionItem":
        return cls(
            asset_id=data["asset_id"],
            quantity=data["quantity"],
            avg_price=data["avg_price"],
        )
    

@dataclass(frozen=True)
class PortfolioItem:
    """
    DTO utilizzata dal PortfolioAnalyzer.

    Rappresenta tutti gli ingredienti necessari per costruire
    una posizione completa del portafoglio.
    """

    position: PositionItem
    asset: AssetItem
    market_price: float


@dataclass(frozen=True)
class Performance:
    cost_basis: float
    market_value: float
    pnl: float
    pnl_percent: float
    cost_basis_base: float | None = None
    pnl_base: float | None = None


@dataclass(frozen=True)
class PortfolioPosition:
    asset: AssetItem

    quantity: float
    currency: str
    avg_price: float
    market_price: float

    market_value: float
    market_value_base: float | None

    performance: Performance

    @classmethod
    def from_item(cls, item: PortfolioItem, market_value: float, performance: Performance) -> "PortfolioPosition":
        return cls(
            asset=item.asset,
            quantity=item.position.quantity,
            currency=item.asset.currency,
            avg_price=item.position.avg_price,
            market_price=item.market_price,
            market_value=market_value,
            market_value_base=None,
            performance=performance
        )

@dataclass(frozen=True)
class PortfolioRisk:
    largest_position_weight: float
    concentration_level: str


@dataclass(frozen=True)
class PortfolioExposure:
    by_symbol: dict[str, float]
    by_sector: dict[str, float]
    by_country: dict[str, float]
    by_currency: dict[str, float]


@dataclass(frozen=True)
class PortfolioResult:
    base_currency: str
    portfolio_value: float
    positions: list[PortfolioPosition]
    exposure: PortfolioExposure
    risk: PortfolioRisk

@dataclass(slots=True)
class PortfolioAnalysisResult:
    portfolio: PortfolioResult
    assets: list[AssetResult]
    
@dataclass(frozen=True)
class WatchlistItem:
    asset_id: int

    @classmethod
    def from_dict(cls, data):
        return cls(asset_id=data["asset_id"])