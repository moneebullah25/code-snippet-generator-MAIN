import os
from functools import lru_cache
from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_current_user
from app.models import CodeGeneratorInput

router = APIRouter()

# Path to the fine-tuned GPT-2 checkpoint (not shipped in this repo).
MODEL_PATH = os.getenv("CODE_MODEL_PATH", "app/api/fine_tuned_code_completion_model")


@lru_cache(maxsize=1)
def _load_model() -> tuple[Any, Any]:
    # Lazy import/load so the API starts even when the checkpoint is absent.
    from transformers import GPT2LMHeadModel, GPT2Tokenizer

    tokenizer = GPT2Tokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
    model = GPT2LMHeadModel.from_pretrained(MODEL_PATH, local_files_only=True)
    model.eval()
    return tokenizer, model


@router.post("/", dependencies=[Depends(get_current_user)])
def get_response(*, item_in: CodeGeneratorInput) -> Any:
    try:
        tokenizer, model = _load_model()
    except (OSError, ImportError) as e:
        raise HTTPException(
            status_code=503,
            detail=f"Code generation model unavailable (CODE_MODEL_PATH={MODEL_PATH})",
        ) from e

    input_ids = tokenizer.encode(item_in.input, return_tensors="pt")
    output = model.generate(
        input_ids, max_length=100, num_return_sequences=1, no_repeat_ngram_size=2
    )
    return tokenizer.decode(output[0], skip_special_tokens=True)
