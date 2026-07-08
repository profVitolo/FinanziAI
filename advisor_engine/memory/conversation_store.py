from __future__ import annotations

import json
from json import JSONDecodeError
from datetime import datetime
from pathlib import Path

from advisor_engine.memory.memory_models import ConversationHistory, ConversationTurn


class ConversationStore:
    def __init__(self, path: Path | None = None):
        self._path = path or Path(__file__).parent / "conversations.json"
    
    def load(self) -> ConversationHistory:
        if not self._path.exists():
            return ConversationHistory()

        text = self._path.read_text(encoding="utf-8").strip()
        if not text:
            return ConversationHistory()

        try:
            data = json.loads(text)
        except JSONDecodeError:
            return ConversationHistory()

        if not isinstance(data, dict):
            return ConversationHistory()

        items = data.get("turns")
        if not isinstance(items, list):
            return ConversationHistory()

        turns = []

        for item in items:
            try:
                turns.append(
                    ConversationTurn(
                        timestamp=datetime.fromisoformat(item["timestamp"]),
                        user_message=item["user_message"],
                        assistant_message=item["assistant_message"],
                    )
                )
            except (KeyError, TypeError, ValueError):
                continue

        return ConversationHistory(turns)

    def save(self, history: ConversationHistory) -> None:
        data = {
            "turns": [
                {
                    "timestamp": turn.timestamp.isoformat(),
                    "user_message": turn.user_message,
                    "assistant_message": turn.assistant_message,
                }
                for turn in history.turns
            ]
        }

        self._path.write_text(json.dumps(data, indent=4, ensure_ascii=False), encoding="utf-8")

    def clear(self) -> None:
        self.save(ConversationHistory())