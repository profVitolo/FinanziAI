from dataclasses import dataclass, field
from enum import StrEnum
from datetime import date

from data_engine.data_engine_models import (
    PortfolioResult,
    AssetResult,
)

from evaluation_engine.evaluation_models import (
    PortfolioEvaluationResult,
    AssetEvaluationResult,
)


class InvestorProfile(StrEnum):
    PRUDENT = "prudent"
    BALANCED = "balanced"
    DYNAMIC = "dynamic"
    AGGRESSIVE = "aggressive"


@dataclass(slots=True)
class AdvisorContext:
    """
    Tutto il contesto che verrà passato al PromptBuilder.

    Contiene sia i dati quantitativi prodotti dal DataEngine,
    sia le valutazioni deterministiche prodotte dall'EvaluationEngine.
    """

    # Portafoglio
    portfolio: PortfolioResult
    portfolio_evaluation: PortfolioEvaluationResult
    portfolio_asset_evaluations: list[AssetEvaluationResult] = field(default_factory=list)

    # Watchlist
    watchlist: list[AssetResult] = field(default_factory=list)
    watchlist_evaluations: list[AssetEvaluationResult] = field(default_factory=list)

    # Profilo investitore
    investor_profile: InvestorProfile = InvestorProfile.BALANCED
    current_date: date = field(default_factory=date.today)


@dataclass(slots=True)
class AdvisorRequest:
    """
    Richiesta proveniente dall'utente.
    """

    prompt: str
    investor_profile: InvestorProfile = InvestorProfile.BALANCED


@dataclass(slots=True)
class Prompt:
    system_prompt: str
    user_prompt: str

@dataclass(slots=True)
class PromptContext:
    current_date: str
    investor_profile: str
    portfolio: str
    portfolio_evaluation: str
    portfolio_asset_evaluations: str
    watchlist: str
    watchlist_evaluations: str

@dataclass(slots=True)
class AdvisorResponse:
    """
    Risposta prodotta dall'AdvisorEngine.
    """

    answer: str

    # Informazioni sul modello utilizzato
    model: str = ""

    # Statistiche della generazione
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None