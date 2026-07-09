from datetime import datetime

from config import MAX_MEMORY_TURNS, MAX_MEMORY_TOKENS, TITLE
from advisor_engine.ai_provider import AIProvider
from advisor_engine.memory.conversation_store import ConversationStore
from advisor_engine.memory.memory_models import ConversationHistory, ConversationTurn


class MemoryManager:
    def __init__(self, conversation_store: ConversationStore | None = None, ai_provider : AIProvider | None = None):
        self._ai_provider  = ai_provider 
        self._conversation_store = conversation_store or ConversationStore()

    def build_memory(self) -> str:
        history = self._conversation_store.load()

        if not history.turns:
            return ""

        sections: list[str] = []
        used_tokens = 0

        for turn in reversed(history.turns):
            section = (
                f"Utente:\n"
                f"{turn.user_message}\n\n"
                f"Assistente {TITLE}:\n"
                f"{turn.assistant_message}\n\n"
            )

            tokens = self._estimate_tokens(section)

            if used_tokens + tokens > MAX_MEMORY_TOKENS:
                break

            sections.append(section)
            used_tokens += tokens

        sections.reverse()

        return "".join(sections).strip()
    
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
        
    def _estimate_tokens(self, text: str) -> int:
        if self._ai_provider  is not None:
            return self._ai_provider.count_tokens(text)

        # fallback indipendente da LLama-ccp
        return max(1, len(text) // 4)
        

