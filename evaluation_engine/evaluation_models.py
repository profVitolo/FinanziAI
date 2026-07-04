from dataclasses import dataclass, field
from enum import StrEnum


class Severity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class EvaluationType(StrEnum):
    RSI = "rsi"
    TREND = "trend"
    VOLATILITY = "volatility"
    BETA = "beta"

    CONCENTRATION = "concentration"
    DIVERSIFICATION = "diversification"
    SECTOR_EXPOSURE = "sector_exposure"
    COUNTRY_EXPOSURE = "country_exposure"
    CURRENCY_EXPOSURE = "currency_exposure"
    SMALL_CAP_EXPOSURE = "small_cap_exposure"
    PORTFOLIO_BETA = "portfolio_beta"

class EvaluationCode(StrEnum):
    # Asset
    ASSET_RSI_OVERBOUGHT = "ASSET_RSI_OVERBOUGHT"
    ASSET_RSI_OVERSOLD = "ASSET_RSI_OVERSOLD"
    ASSET_HIGH_VOLATILITY = "ASSET_HIGH_VOLATILITY"
    ASSET_BULLISH_TREND = "ASSET_BULLISH_TREND"
    ASSET_BEARISH_TREND = "ASSET_BEARISH_TREND"
    ASSET_HIGH_BETA = "ASSET_HIGH_BETA"
    ASSET_LOW_BETA = "ASSET_LOW_BETA"

    # Portfolio
    PORTFOLIO_HIGH_CONCENTRATION = "PORTFOLIO_HIGH_CONCENTRATION"
    PORTFOLIO_MEDIUM_CONCENTRATION = "PORTFOLIO_MEDIUM_CONCENTRATION"
    PORTFOLIO_LOW_DIVERSIFICATION = "PORTFOLIO_LOW_DIVERSIFICATION"
    PORTFOLIO_HIGH_SECTOR_EXPOSURE = "PORTFOLIO_HIGH_SECTOR_EXPOSURE"
    PORTFOLIO_MEDIUM_SECTOR_EXPOSURE = "PORTFOLIO_MEDIUM_SECTOR_EXPOSURE"
    PORTFOLIO_COUNTRY_EXPOSURE = "PORTFOLIO_COUNTRY_EXPOSURE"
    PORTFOLIO_CURRENCY_EXPOSURE = "PORTFOLIO_CURRENCY_EXPOSURE"
    PORTFOLIO_SMALL_CAP_EXPOSURE = "PORTFOLIO_SMALL_CAP_EXPOSURE"
    PORTFOLIO_HIGH_BETA = "PORTFOLIO_HIGH_BETA"

@dataclass(slots=True)
class EvaluationMessage:
    code: EvaluationCode
    type: EvaluationType
    severity: Severity
    message: str


@dataclass(slots=True)
class EvaluationSummary:
    message_count: int = 0
    highest_severity: Severity | None = None


@dataclass(slots=True)
class EvaluationResult:
    messages: list[EvaluationMessage]
    summary: EvaluationSummary
    
@dataclass(slots=True)
class AssetEvaluationResult(EvaluationResult):
    symbol: str

@dataclass(slots=True)
class PortfolioEvaluationResult(EvaluationResult):
    pass

"""
@dataclass(slots=True)
class EvaluationReport:
    portfolio: PortfolioEvaluationResult
    assets: list[AssetEvaluationResult] = field(default_factory=list)
"""