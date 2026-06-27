from __future__ import annotations

from docguard_llm.hf_client import HFClient
from docguard_llm.json_parser import parse_model_output
from docguard_llm.model_registry import get_model_config
from docguard_llm.prompt_builder import build_compact_prompt, build_prompt


def predict(record: dict, model_key: str, backend: str, few_shot_examples: list[dict] | None = None, compact_prompt: bool = False) -> dict:
    client = HFClient(model_key=model_key, backend=backend)
    messages = build_compact_prompt(record) if compact_prompt else build_prompt(record, few_shot_examples)
    raw_output, latency = client.generate(messages)
    parsed, parse_error = parse_model_output(raw_output)
    config = get_model_config(model_key)
    return {
        "record_id": record["id"],
        "model_key": model_key,
        "model_id": config["model_id"],
        "backend": backend,
        **parsed,
        "raw_model_output": raw_output,
        "parse_error": parse_error,
        "latency_seconds": latency,
    }
