from __future__ import annotations


default_model_key = "qwen2_5_coder_7b"

MODEL_REGISTRY = {
    "qwen2_5_coder_7b": {
        "model_id": "Qwen/Qwen2.5-Coder-7B-Instruct",
        "role": "primary",
        "type": "code-instruct",
        "expected_strengths": [
            "code diff understanding",
            "code reasoning",
            "structured JSON generation",
            "documentation patch generation",
        ],
    },
    "deepseek_coder_6_7b": {
        "model_id": "deepseek-ai/deepseek-coder-6.7b-instruct",
        "role": "comparison",
        "type": "code-instruct",
        "expected_strengths": [
            "code understanding",
            "project-level code reasoning",
            "documentation patch generation",
        ],
    },
    "qwen2_5_coder_3b": {
        "model_id": "Qwen/Qwen2.5-Coder-3B-Instruct",
        "role": "lightweight comparison",
        "type": "code-instruct",
        "expected_strengths": [
            "smaller local model",
            "faster inference",
            "lower resource requirements",
        ],
    },
    "qwen2_5_coder_1_5b": {
        "model_id": "Qwen/Qwen2.5-Coder-1.5B-Instruct",
        "role": "lightweight_real_local",
        "type": "code-instruct",
        "expected_strengths": [
            "lightweight local smoke tests",
            "CPU-friendly compared to 3B/7B",
            "structured JSON generation",
        ],
    },
    "qwen2_5_coder_0_5b": {
        "model_id": "Qwen/Qwen2.5-Coder-0.5B-Instruct",
        "role": "smallest_real_local",
        "type": "code-instruct",
        "expected_strengths": [
            "fastest local CPU smoke test",
            "validates real transformers_local generation path",
            "not expected to be the best quality model",
        ],
    },
}


def list_models() -> dict[str, dict]:
    return MODEL_REGISTRY


def get_model_config(model_key: str) -> dict:
    if model_key not in MODEL_REGISTRY:
        raise KeyError(f"Unsupported model key: {model_key}")
    return MODEL_REGISTRY[model_key]
