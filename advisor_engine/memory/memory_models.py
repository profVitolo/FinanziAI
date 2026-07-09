from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True, frozen=True)
class ConversationTurn:
    """
    Un turno completo della conversazione.
    Rappresenta una richiesta dell'utente e la relativa risposta
    dell'assistente.
    """
    timestamp: datetime
    user_message: str
    assistant_message: str


@dataclass(slots=True)
class ConversationHistory:
    """
    Collezione ordinata dei turni della conversazione.
    """
    turns: list[ConversationTurn] = field(default_factory=list)
