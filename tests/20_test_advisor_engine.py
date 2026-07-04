from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from test_utils import *

from advisor_engine.llama_provider import LlamaProvider


print_title("=== TEST ADVISOR ENGINE ===")

print("Loading LLM...")

provider = LlamaProvider()

print_result("Loaded model: ", provider.model_name)


print("Health Check")
response = provider.health_check()

print(response.answer)
print(response.prompt_tokens)
print(response.completion_tokens)


tests = [
    (
        "Simple reply",
        "Reply only with the word OK."
    ),
    (
        "Capitale Italiana",
        "Qual è la capitale d'Italia? Rispondi con una sola parola."
    ),
    (
        "Financial reasoning",
        """
        Sei un consulente finanziario, FinaziAI-BOT.

        Asset:
        - NVIDIA
        - Beta: 1.8
        - Trend: Bullish
        - Volatility: High

        Scrivi una breve valutazione in massimo due frasi.
        """
    ),
]

i = 0

for title, prompt in tests:

    print_title(title)

    print("PROMPT")
    print("-" * 60)
    print(prompt.strip())
    
    shouldThink = True if i > 1 else False
    response = provider.generate(prompt, thinking=shouldThink)

    print("\nANSWER")
    print("-" * 60)
    print(response.answer)

    print("\nTOKENS")
    print("-" * 60)
    print(f"Prompt      : {response.prompt_tokens}")
    print(f"Completion  : {response.completion_tokens}")
    print(f"Total       : {response.total_tokens}")
    i += 1
    
print_title("=== TEST COMPLETED ===")