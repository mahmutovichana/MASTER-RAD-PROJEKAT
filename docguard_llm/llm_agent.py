from __future__ import annotations

from docguard_llm.hf_client import HFClient
from docguard_llm.json_parser import parse_model_output_detailed
from docguard_llm.label_normalizer import add_normalized_fields
from docguard_llm.model_registry import get_model_config
from docguard_llm.prompt_builder import build_prompt_for_mode


def predict(record: dict, model_key: str, backend: str, few_shot_examples: list[dict] | None = None, compact_prompt: bool = False, prompt_mode: str | None = None) -> dict:
    client = HFClient(model_key=model_key, backend=backend)
    mode = prompt_mode or ("compact" if compact_prompt else "full")
    messages = build_prompt_for_mode(record, mode, few_shot_examples)
    raw_output, latency = client.generate(messages)
    parsed, parse_error, parse_error_type = parse_model_output_detailed(raw_output)
    config = get_model_config(model_key)
    row = {
        "record_id": record["id"],
        "model_key": model_key,
        "model_id": config["model_id"],
        "backend": backend,
        **parsed,
        "raw_model_output": raw_output,
        "parse_error": parse_error,
        "parse_error_type": parse_error_type,
        "latency_seconds": latency,
    }
    return add_normalized_fields(row, record)
