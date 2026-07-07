from advisor_engine.advisor_models import AdvisorRequest, AdvisorResponse
from advisor_engine.advisor_context_builder import AdvisorContextBuilder
from advisor_engine.prompt_builder import PromptBuilder
from advisor_engine.llama_provider import LlamaProvider


class AdvisorEngine:

    def __init__(self):
        self._context_builder = AdvisorContextBuilder()
        self._prompt_builder = PromptBuilder()
        self._provider = LlamaProvider()

    def advise(self, request: AdvisorRequest) -> AdvisorResponse:
        context = self._context_builder.build(request.investor_profile)
        prompt = self._prompt_builder.build(context=context, user_prompt=request.prompt)

        return self._provider.generate(system_prompt=prompt.system_prompt, user_prompt=prompt.user_prompt)