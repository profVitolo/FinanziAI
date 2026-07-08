from datetime import datetime

from config import MAX_MEMORY_TURNS
from advisor_engine.memory.conversation_store import ConversationStore
from advisor_engine.memory.memory_models import ConversationHistory, ConversationTurn


class MemoryManager:
    def __init__(self, conversation_store: ConversationStore | None = None):
        self._conversation_store = conversation_store or ConversationStore()

    def build_memory(self) -> str:
        history = self._conversation_store.load()

        if not history.turns:
            return ""

        sections: list[str] = []

        for turn in history.turns:
            sections.extend(
                [
                    "Utente:",
                    turn.user_message,
                    "",
                    "Assistente:",
                    turn.assistant_message,
                    "",
                ]
            )

        return "\n".join(sections).strip()

    def add_turn(self, user_message: str, assistant_message: str) -> None:
        history = self._conversation_store.load()

        history.turns.append(
            ConversationTurn(
                timestamp=datetime.now(),
                user_message=user_message,
                assistant_message=assistant_message,
            )
        )

        self._maintain_memory(history)

        self._conversation_store.save(history)
    
    def clear(self) -> None:
        self._conversation_store.clear()
    
    def get_history(self) -> ConversationHistory:
        return self._conversation_store.load()
        
    def _maintain_memory(self, history: ConversationHistory) -> None:
        history.turns = history.turns[-MAX_MEMORY_TURNS:]

