from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from test_utils import *
from advisor_engine.llama_provider import LlamaProvider
from advisor_engine.advisor_context_builder import AdvisorContextBuilder
from advisor_engine.prompt_builder import PromptBuilder
from advisor_engine.advisor_models import InvestorProfile

SYSTEM_PROMPT = """
Sei FinanziAI-BOT.

Rispondi sempre in italiano.
Fornisci risposte concise e accurate.
"""


print_title("=== TEST ADVISOR ENGINE ===")

print("Loading LLM...")
provider = LlamaProvider()

print_result("Loaded model:", provider.model_name)

print("\nHealth Check")

response = provider.health_check()

print(response.answer)
print(f"Prompt tokens     : {response.prompt_tokens}")
print(f"Completion tokens : {response.completion_tokens}")


tests = [
    (
        "Simple reply",
        "Reply only with the word OK.",
    ),
    (
        "Capitale Italiana",
        "Qual è la capitale d'Italia? Rispondi con una sola parola.",
    ),
    (
        "Financial reasoning",
        """
Sei un consulente finanziario.

Asset:
- NVIDIA
- Beta: 1.8
- Trend: Bullish
- Volatility: High

Scrivi una breve valutazione in massimo due frasi.
""",
    ),
]


for title, user_prompt in tests:

    print_title(title)

    print("PROMPT")
    print("-" * 60)
    print(user_prompt.strip())

    response = provider.generate(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
    )

    print("\nANSWER")
    print("-" * 60)
    print(response.answer)

    print("\nTOKENS")
    print("-" * 60)
    print(f"Prompt      : {response.prompt_tokens}")
    print(f"Completion  : {response.completion_tokens}")
    print(f"Total       : {response.total_tokens}")

print_title("AdvisorContextBuilder")

builder = AdvisorContextBuilder()
context = builder.build(InvestorProfile.BALANCED)
print_result("Context", context)
    


print_title("PromptBuilder")

prompt_builder = PromptBuilder()
prompt = prompt_builder.build(
    context=context,
    user_prompt="Analizza il mio portafoglio e dammi tre suggerimenti."
)

print_result("SYSTEM PROMPT",prompt.system_prompt)
print_result("USER PROMPT", prompt.user_prompt)

print_title("=== TEST COMPLETED ===")