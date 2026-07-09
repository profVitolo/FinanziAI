from pathlib import Path

TITLE = "FinanziAI",
DESCRIPTION = "AI-Assisted Investment Analysis",
VERSION = "0.1.3"
    
ROOT_DIR = Path(__file__).resolve().parent
DB_PATH = ( ROOT_DIR / "database" / "vault.db" )
SCHEMA_PATH = (ROOT_DIR / "database" / "init_db.sql" )

BASE_CURRENCY = "EUR"
BOOTSTRAP_DAYS = 90

# Advisor Engine
LLM_MODEL = "Qwen3-8B-Q4_K_M.gguf"
LLM_MODEL_REPO = "Qwen/Qwen3-8B-GGUF"

LLM_MODEL_PATH = ROOT_DIR / "advisor_engine" / "models" / LLM_MODEL

LLM_CONTEXT_SIZE = 8192
LLM_TEMPERATURE = 0.2
LLM_TOP_P = 0.9
LLM_REPEAT_PENALTY = 1.10
LLM_MAX_TOKENS = 2048
MAX_MEMORY_TOKENS = 1200

LLM_GPU_LAYERS = -1   # >0 oppure -1 se vuoi usare CUDA/Metal
LLM_THREADS = None

MAX_MEMORY_TURNS = 8