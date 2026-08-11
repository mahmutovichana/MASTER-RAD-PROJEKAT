from __future__ import annotations

import re
import time
from typing import Any

from docguard_llm.config import DEFAULT_PATCH_MAX_NEW_TOKENS, DEFAULT_PATCH_TEMPERATURE


def _first_grounded_token(prompt: str) -> str:
    token_line = re.search(r"Concrete tokens extracted from diff:\s*(.+)", prompt)
    if token_line:
        for token in [part.strip() for part in token_line.group(1).split(",")]:
            if token and token.lower() != "none":
                return token
    patterns = [
        r"(/[A-Za-z0-9_:{}/-]+)",
        r"\b([A-Z][A-Z0-9_]{3,})\b",
        r"\b(npm run [A-Za-z0-9:_-]+)\b",
        r"\b([A-Za-z_][A-Za-z0-9_]*Id)\b",
        r"\b(\*/\d+ \* \* \* \*)\b",
        r"\b(status\s*\(\s*(\d{3})\s*\))",
    ]
    for pattern in patterns:
        match = re.search(pattern, prompt)
        if match:
            return match.group(match.lastindex or 1)
    return "the documented code change"


def _mock_generate(prompt: str) -> str:
    section_match = re.search(r"Target section:\s*(.+)", prompt)
    section = section_match.group(1).strip() if section_match else "Documentation"
    token = _first_grounded_token(prompt)
    return f"@@ {section}\n+Mock LLM patch: document `{token}` based on the supplied code diff."


def generate_documentation_patch(
    prompt: str,
    backend: str = "mock",
    model_name: str | None = None,
    max_new_tokens: int = DEFAULT_PATCH_MAX_NEW_TOKENS,
    temperature: float = DEFAULT_PATCH_TEMPERATURE,
) -> dict[str, Any]:
    start = time.perf_counter()
    try:
        if backend == "mock":
            patch_text = _mock_generate(prompt)
        elif backend == "hf":
            patch_text = _generate_hf(prompt, model_name, max_new_tokens, temperature)
        else:
            raise ValueError(f"Unsupported documentation patch backend: {backend}")
        return {
            "patch_text": patch_text,
            "backend": backend,
            "model_name": model_name,
            "generation_status": "ok",
            "error_message": "",
            "latency_seconds": time.perf_counter() - start,
        }
    except Exception as exc:
        return {
            "patch_text": "",
            "backend": backend,
            "model_name": model_name,
            "generation_status": "error",
            "error_message": str(exc) or exc.__class__.__name__,
            "latency_seconds": time.perf_counter() - start,
        }


def _generate_hf(prompt: str, model_name: str | None, max_new_tokens: int, temperature: float) -> str:
    if not model_name:
        raise RuntimeError("backend='hf' requires an explicit model_name. No model is mandatory or downloaded by default.")
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ModuleNotFoundError as exc:
        raise RuntimeError("backend='hf' requires optional dependencies: torch and transformers.") from exc
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=temperature > 0,
            temperature=temperature if temperature > 0 else None,
        )
    generated = outputs[0][inputs["input_ids"].shape[-1]:]
    return tokenizer.decode(generated, skip_special_tokens=True)
