from dataclasses import dataclass, field
from enum import Enum


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(slots=True)
class AdvisorMessage:
    code: str
    type: str
    severity: Severity
    message: str


@dataclass(slots=True)
class AdvisorSummary:
    message_count: int = 0
    highest_severity: Severity | None = None


@dataclass(slots=True)
class AdvisorResult:
    messages: list[AdvisorMessage]
    summary: AdvisorSummary
    
@dataclass(slots=True)
class AssetAdvisorResult(AdvisorResult):
    symbol: str

@dataclass(slots=True)
class PortfolioAdvisorResult(AdvisorResult):
    pass


@dataclass(slots=True)
class AdvisorReport:
    portfolio: PortfolioAdvisorResult
    assets: list[AssetAdvisorResult] = field(default_factory=list)