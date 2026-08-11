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
    device_map: str | None = None,
    torch_dtype: str | None = None,
    trust_remote_code: bool = False,
) -> dict[str, Any]:
    start = time.perf_counter()
    try:
        if backend == "mock":
            patch_text = _mock_generate(prompt)
        elif backend == "hf":
            patch_text = _generate_hf(
                prompt,
                model_name,
                max_new_tokens,
                temperature,
                device_map=device_map,
                torch_dtype=torch_dtype,
                trust_remote_code=trust_remote_code,
            )
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


def _resolve_torch_dtype(torch_module: Any, torch_dtype: str | None) -> Any:
    if not torch_dtype:
        return None
    if torch_dtype == "auto":
        return "auto"
    try:
        return getattr(torch_module, torch_dtype)
    except AttributeError as exc:
        raise RuntimeError(f"Unsupported torch dtype: {torch_dtype}") from exc


def _generate_hf(
    prompt: str,
    model_name: str | None,
    max_new_tokens: int,
    temperature: float,
    *,
    device_map: str | None = None,
    torch_dtype: str | None = None,
    trust_remote_code: bool = False,
) -> str:
    if not model_name:
        raise RuntimeError("backend='hf' requires an explicit model_name. No model is mandatory or downloaded by default.")
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "backend='hf' requires optional dependencies. Install transformers and torch; "
            "install accelerate as well if using --device-map auto."
        ) from exc
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=trust_remote_code)
    model_kwargs: dict[str, Any] = {"trust_remote_code": trust_remote_code}
    resolved_dtype = _resolve_torch_dtype(torch, torch_dtype)
    if resolved_dtype is not None:
        try:
            model_kwargs["torch_dtype"] = resolved_dtype
        except TypeError:
            model_kwargs["dtype"] = resolved_dtype
    if device_map:
        model_kwargs["device_map"] = device_map
    try:
        model = AutoModelForCausalLM.from_pretrained(model_name, **model_kwargs)
    except ImportError as exc:
        raise RuntimeError(
            "HuggingFace loading failed. If you used --device-map auto, install accelerate. "
            "Otherwise verify that torch and transformers are installed."
        ) from exc
    model.eval()
    inputs = tokenizer(prompt, return_tensors="pt")
    if not device_map:
        device = next(model.parameters()).device
        inputs = inputs.to(device)
    with torch.no_grad():
        generation_kwargs: dict[str, Any] = {
            "max_new_tokens": max_new_tokens,
            "do_sample": temperature > 0,
        }
        if temperature > 0:
            generation_kwargs["temperature"] = temperature
        outputs = model.generate(
            **inputs,
            **generation_kwargs,
        )
    generated = outputs[0][inputs["input_ids"].shape[-1]:]
    return tokenizer.decode(generated, skip_special_tokens=True)
