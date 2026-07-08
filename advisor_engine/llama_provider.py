import re
from pathlib import Path
from llama_cpp import Llama
from llama_cpp import llama_print_system_info

from config import (
    LLM_MODEL_PATH,
    LLM_CONTEXT_SIZE,
    LLM_MAX_TOKENS,
    LLM_TEMPERATURE,
    LLM_TOP_P,
    LLM_REPEAT_PENALTY,
    LLM_GPU_LAYERS,
    LLM_THREADS,
)
from advisor_engine.advisor_models import AdvisorResponse


class LlamaProvider:
    """
    Wrapper minimale di llama-cpp-python.

    Responsabilità:
        - verificare la presenza del modello locale
        - caricare il modello una sola volta
        - inviare un prompt
        - restituire un AdvisorResponse
    """

    def __init__(self):
        model_path = Path(LLM_MODEL_PATH)

        if not model_path.exists():
            raise FileNotFoundError(f"LLM model not found: {model_path}")
        
        self._model_path = model_path
        self._llm = Llama(
            model_path=str(model_path),
            n_ctx=LLM_CONTEXT_SIZE,
            n_threads=LLM_THREADS,
            n_gpu_layers=LLM_GPU_LAYERS,
            verbose=False,
            chat_format="chatml",
        )

    @property
    def model_name(self) -> str:
        return self._model_path.name

    def generate(
        self,
        *,
        user_prompt: str,
        system_prompt: str,
        max_tokens: int = LLM_MAX_TOKENS,
        temperature: float = LLM_TEMPERATURE,
        top_p: float = LLM_TOP_P,
        repeat_penalty: float = LLM_REPEAT_PENALTY
    ) -> AdvisorResponse:
        """
        if thinking:
            system_prompt += "/think"
        else:
            system_prompt += "/no_think"
        """    
        response = self._llm.create_chat_completion(
             messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            repeat_penalty=repeat_penalty,
        )

        usage = response.get("usage", {})
        choice = response["choices"][0]
        
        choice = response["choices"][0]

        raw_answer = choice["message"]["content"].strip()
        answer = self._extract_answer(raw_answer)

        return AdvisorResponse(
            raw_answer=raw_answer,
            answer=answer,
            model=self.model_name,
            prompt_tokens=usage.get("prompt_tokens"),
            completion_tokens=usage.get("completion_tokens"),
            total_tokens=usage.get("total_tokens"),
        )
    
    # Metodo stupido per i test
    def health_check(self) -> AdvisorResponse:
        return self.generate(
            system_prompt="Sei un assistente.",
            user_prompt="Rispondi esclusivamente con la parola OK. /no_think",
            max_tokens=8,
            temperature=0.0,
        )
    
    def _extract_answer(self, text: str) -> str:
        """
        Rimuove l'eventuale blocco <think>...</think>
        prodotto dal modello reasoning (qwen).
        """
        return re.sub(r"<think>.*?</think>\s*", "", text, flags=re.DOTALL).strip()

