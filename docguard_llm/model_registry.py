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
}


def list_models() -> dict[str, dict]:
    return MODEL_REGISTRY


def get_model_config(model_key: str) -> dict:
    if model_key not in MODEL_REGISTRY:
        raise KeyError(f"Unsupported model key: {model_key}")
    return MODEL_REGISTRY[model_key]

