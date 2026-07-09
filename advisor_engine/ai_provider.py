from abc import ABC, abstractmethod
from advisor_engine.advisor_models import AdvisorResponse


class AIProvider(ABC):

    @property
    @abstractmethod
    def model_name(self) -> str:
        ...

    @abstractmethod
    def generate(self, *, user_prompt: str, system_prompt: str) -> AdvisorResponse:
        ...

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        ...
    
    @abstractmethod
    def health_check(self) -> AdvisorResponse:
        ...