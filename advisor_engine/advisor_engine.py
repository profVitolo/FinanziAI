from advisor_engine.advisor_models import AdvisorRequest, AdvisorResponse
from advisor_engine.advisor_context_builder import AdvisorContextBuilder
from advisor_engine.prompt_builder import PromptBuilder
from advisor_engine.llama_provider import LlamaProvider
from advisor_engine.ai_provider import AIProvider
from advisor_engine.memory.memory_manager import MemoryManager
from advisor_engine.memory.memory_models import ConversationHistory


class AdvisorEngine:

    def __init__(self, provider: AIProvider | None = None):
        self._provider = provider or LlamaProvider()
        self._context_builder = AdvisorContextBuilder()
        self._memory_manager = MemoryManager(ai_provider=self._provider)
        self._prompt_builder = PromptBuilder(self._memory_manager)


    def advise(self, request: AdvisorRequest) -> AdvisorResponse:
        context = self._context_builder.build(request.investor_profile)
        prompt = self._prompt_builder.build(context=context, user_prompt=request.prompt)

        response = self._provider.generate(system_prompt=prompt.system_prompt, user_prompt=prompt.user_prompt)
        self._memory_manager.add_turn(request.prompt, response.answer)
        
        return response
        
    def get_history(self) -> ConversationHistory:
        return self._memory_manager.get_history()

    def clear_history(self) -> None:
        self._memory_manager.clear()

