from pathlib import Path
from huggingface_hub import hf_hub_download

from config import (
    LLM_MODEL,
    LLM_MODEL_REPO,
    LLM_MODEL_PATH,
)


def ensure_model() -> Path:
    """
    Verifica che il modello locale esista.
    Se manca lo scarica automaticamente da HuggingFace.
    Restituisce sempre il path del modello.
    """

    if LLM_MODEL_PATH.exists():
        print(f"LLM model found: {LLM_MODEL_PATH}")
        return LLM_MODEL_PATH

    print("=" * 60)
    print("Local LLM model not found.")
    print(f"Downloading {LLM_MODEL} (~5 GB)")
    print("This operation is required only the first time.")
    print("=" * 60)

    LLM_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

    downloaded = hf_hub_download(
        repo_id=LLM_MODEL_REPO,
        filename=LLM_MODEL,
        local_dir=LLM_MODEL_PATH.parent,
        local_dir_use_symlinks=False,
    )

    print("Download completed.")

    return Path(downloaded)