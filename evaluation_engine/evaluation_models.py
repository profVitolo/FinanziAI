from dataclasses import dataclass, field
from enum import Enum


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(slots=True)
class EvaluationMessage:
    code: str
    type: str
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


@dataclass(slots=True)
class EvaluationReport:
    portfolio: PortfolioEvaluationResult
    assets: list[AssetEvaluationResult] = field(default_factory=list)