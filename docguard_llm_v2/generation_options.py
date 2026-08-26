from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class GenerationOptions:
    temperature: float | None = None
    max_tokens: int | None = None


def options_for_purpose(config: dict[str, Any] | None, purpose: str) -> GenerationOptions:
    cfg = config or {}
    max_key = {
        "analysis": "max_tokens_analysis",
        "writer": "max_tokens_writer",
        "repair": "max_tokens_repair",
    }[purpose]
    return GenerationOptions(
        temperature=None if cfg.get("temperature") is None else float(cfg.get("temperature")),
        max_tokens=None if cfg.get(max_key) is None else int(cfg.get(max_key)),
    )


def call_llm(llm: Any, messages: list[dict[str, str]], *, model: str | None, purpose: str, options: GenerationOptions | None = None) -> str:
    try:
        return llm.generate(messages, model=model, purpose=purpose, generation_options=options)
    except TypeError as exc:
        if "generation_options" not in str(exc):
            raise
        return llm.generate(messages, model=model, purpose=purpose)
