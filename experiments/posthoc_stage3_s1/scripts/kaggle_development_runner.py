from __future__ import annotations

import argparse
import gc
import importlib.metadata
import json
import os
import platform
import time
import traceback
from pathlib import Path
from typing import Any

from experiments.posthoc_stage3_s1.scripts.retrieval import (
    EMBEDDING_MODEL_ID,
    EMBEDDING_REVISION,
    RERANKER_MODEL_ID,
    RERANKER_REVISION,
    QwenDenseEncoder,
    QwenReranker,
)
from experiments.posthoc_stage3_s1.scripts.s1_pipeline import (
    GENERATOR_MODEL_ID,
    GENERATOR_REVISION,
    QwenStructuredGenerator,
)


def package_versions() -> dict[str, str | None]:
    values = {}
    for name in ("torch", "transformers", "accelerate", "bitsandbytes", "huggingface-hub", "numpy", "scikit-learn", "psutil"):
        try:
            values[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            values[name] = None
    return values


def host_ram() -> dict[str, int | None]:
    try:
        import psutil
        try:
            import resource

            peak_rss_bytes = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) * 1024
        except Exception:
            peak_rss_bytes = None

        process = psutil.Process()
        return {"process_rss_bytes": process.memory_info().rss, "peak_process_rss_bytes": peak_rss_bytes, "system_used_bytes": psutil.virtual_memory().used}
    except Exception:
        return {"process_rss_bytes": None, "peak_process_rss_bytes": None, "system_used_bytes": None}


def cuda_snapshot() -> dict[str, Any]:
    import torch

    def per_device(statistic) -> list[int]:
        values = []
        for index in range(torch.cuda.device_count()):
            with torch.cuda.device(index):
                values.append(int(statistic()))
        return values

    return {
        "available": torch.cuda.is_available(),
        "device_count": torch.cuda.device_count(),
        "devices": [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())],
        "allocated_bytes": per_device(torch.cuda.memory_allocated),
        "reserved_bytes": per_device(torch.cuda.memory_reserved),
        "peak_allocated_bytes": per_device(torch.cuda.max_memory_allocated),
        "peak_reserved_bytes": per_device(torch.cuda.max_memory_reserved),
    }


def reset_cuda_peak_memory_stats() -> None:
    import torch

    for index in range(torch.cuda.device_count()):
        with torch.cuda.device(index):
            torch.cuda.reset_peak_memory_stats()


def cleanup_cuda() -> dict[str, Any]:
    import torch

    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
    return cuda_snapshot()


def resolved_revision(model: Any) -> str | None:
    return getattr(getattr(model, "config", None), "_commit_hash", None)


def require_keys(value: dict[str, Any], keys: set[str], label: str) -> None:
    missing = sorted(keys - set(value))
    if missing:
        raise ValueError(f"{label} JSON missing keys: {missing}")


def timed_stage(receipt: dict[str, Any], name: str, operation):
    started = time.monotonic()
    value = operation()
    receipt["stages"].append(
        {
            "name": name,
            "elapsed_seconds": time.monotonic() - started,
            "cuda": cuda_snapshot(),
            "host_ram": host_ram(),
        }
    )
    return value


def run_canary(cache_dir: str) -> dict[str, Any]:
    import torch

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for the frozen S1 canary")
    if not os.environ.get("HF_TOKEN"):
        raise RuntimeError("Kaggle Secret HF_TOKEN was not exported to the environment")
    reset_cuda_peak_memory_stats()
    started = time.monotonic()
    receipt: dict[str, Any] = {
        "state": "CANARY_RUNNING",
        "confirmation_accessed": False,
        "gate6_row_level_human_data_accessed": False,
        "initial_cuda": cuda_snapshot(),
        "initial_host_ram": host_ram(),
        "stages": [],
        "expected_revisions": {
            EMBEDDING_MODEL_ID: EMBEDDING_REVISION,
            RERANKER_MODEL_ID: RERANKER_REVISION,
            GENERATOR_MODEL_ID: GENERATOR_REVISION,
        },
        "resolved_revisions": {},
        "repair_count": 0,
    }

    dense = timed_stage(receipt, "embedding_load", lambda: QwenDenseEncoder(cache_dir=cache_dir))
    revision = resolved_revision(dense.model)
    receipt["resolved_revisions"][EMBEDDING_MODEL_ID] = revision
    if revision != EMBEDDING_REVISION:
        raise RuntimeError(f"Embedding revision mismatch: {revision}")
    shape = timed_stage(receipt, "embedding_inference", lambda: list(dense.encode(["changed configuration key", "configuration reference documentation"]).shape))
    if shape != [2, 1024]:
        raise RuntimeError(f"Unexpected embedding shape: {shape}")
    unload_started = time.monotonic()
    del dense
    unload_cuda = cleanup_cuda()
    receipt["stages"].append({"name": "embedding_unload", "elapsed_seconds": time.monotonic() - unload_started, "cuda": unload_cuda, "host_ram": host_ram()})

    reranker = timed_stage(receipt, "reranker_load", lambda: QwenReranker(cache_dir=cache_dir))
    revision = resolved_revision(reranker.model)
    receipt["resolved_revisions"][RERANKER_MODEL_ID] = revision
    if revision != RERANKER_REVISION:
        raise RuntimeError(f"Reranker revision mismatch: {revision}")
    scores = timed_stage(receipt, "reranker_inference", lambda: reranker.score("new configuration key", ["API overview", "configuration key reference"]))
    if len(scores) != 2 or not all(0.0 <= value <= 1.0 for value in scores):
        raise RuntimeError("Reranker did not return two bounded scores")
    unload_started = time.monotonic()
    del reranker
    unload_cuda = cleanup_cuda()
    receipt["stages"].append({"name": "reranker_unload", "elapsed_seconds": time.monotonic() - unload_started, "cuda": unload_cuda, "host_ram": host_ram()})

    generator = timed_stage(receipt, "generator_4bit_nf4_load", lambda: QwenStructuredGenerator(cache_dir=cache_dir))
    revision = resolved_revision(generator.model)
    receipt["resolved_revisions"][GENERATOR_MODEL_ID] = revision
    if revision != GENERATOR_REVISION:
        raise RuntimeError(f"Generator revision mismatch: {revision}")
    quantizer = getattr(generator.model, "hf_quantizer", None)
    if quantizer is None:
        raise RuntimeError("Generator is not using the frozen 4-bit quantized runtime")

    plan_prompt = (
        "Return JSON only. Given evidence that config key `cacheMode` changes from `local` to `shared`, create a plan with keys "
        "update_needed, target_document, target_section, change_type, developer_facing_effect, facts_to_document, "
        "facts_not_supported, style_observations, minimal_update_intent. Target docs/configuration.md, section Cache."
    )
    plan_one = timed_stage(receipt, "deterministic_plan_json_first", lambda: generator.generate_json(purpose="documentation_plan_canary", prompt=plan_prompt))
    plan_two = timed_stage(receipt, "deterministic_plan_json_repeat", lambda: generator.generate_json(purpose="documentation_plan_canary", prompt=plan_prompt))
    require_keys(plan_one, {"update_needed", "target_document", "target_section", "change_type", "developer_facing_effect", "facts_to_document", "facts_not_supported", "style_observations", "minimal_update_intent"}, "plan")
    if plan_one != plan_two:
        raise RuntimeError("Greedy generator produced non-identical repeated plan JSON")

    critic_prompt = (
        "Return JSON only with grounded, target_fit, useful, style_fit, unsupported_claims, unnecessary_content, decision, "
        "repair_instructions. Evidence supports only `cacheMode: shared`; candidate patch also claims Windows is required. "
        "Set decision to REPAIR and instruct removal of the unsupported Windows claim."
    )
    critic = timed_stage(receipt, "structured_critic_json", lambda: generator.generate_json(purpose="critic_canary", prompt=critic_prompt))
    require_keys(critic, {"grounded", "target_fit", "useful", "style_fit", "unsupported_claims", "unnecessary_content", "decision", "repair_instructions"}, "critic")
    if critic.get("decision") != "REPAIR":
        raise RuntimeError("Canary critic did not exercise the required bounded repair path")
    repair_prompt = (
        "Return JSON only with target_document, target_section, patch_markdown. Repair exactly once: remove the unsupported "
        "Windows claim and retain only the grounded statement that `cacheMode` now uses `shared`."
    )
    repaired = timed_stage(receipt, "single_bounded_repair", lambda: generator.generate_json(purpose="repair_canary", prompt=repair_prompt))
    require_keys(repaired, {"target_document", "target_section", "patch_markdown"}, "repair")
    receipt["repair_count"] = 1
    unload_started = time.monotonic()
    del generator
    unload_cuda = cleanup_cuda()
    receipt["stages"].append({"name": "generator_unload", "elapsed_seconds": time.monotonic() - unload_started, "cuda": unload_cuda, "host_ram": host_ram()})
    receipt.update(
        {
            "state": "CANARY_PASS",
            "runtime_seconds": time.monotonic() - started,
            "final_cuda": cuda_snapshot(),
            "final_host_ram": host_ram(),
            "package_versions": package_versions(),
            "structured_plan_valid": True,
            "structured_critic_valid": True,
            "deterministic_generation": True,
            "bounded_repair_path": True,
        }
    )
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description="Frozen S1 sequential Kaggle GPU canary")
    parser.add_argument("--canary", action="store_true", required=True)
    parser.add_argument("--cache-dir", default=os.environ.get("HF_HOME", "/kaggle/working/hf-cache"))
    parser.add_argument("--receipt", type=Path, default=Path("/kaggle/working/s1-development/canary_receipt.json"))
    args = parser.parse_args()
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    try:
        receipt = run_canary(args.cache_dir)
        exit_code = 0
    except Exception as exc:
        cleanup = cleanup_cuda()
        receipt = {
            "state": "CANARY_STOP",
            "confirmation_accessed": False,
            "gate6_row_level_human_data_accessed": False,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "traceback": traceback.format_exc(),
            "package_versions": package_versions(),
            "python": platform.python_version(),
            "cuda": cleanup,
            "host_ram": host_ram(),
        }
        exit_code = 2
    receipt["python"] = platform.python_version()
    args.receipt.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(receipt["state"])
    print(json.dumps({"receipt": str(args.receipt), "runtime_seconds": receipt.get("runtime_seconds")}, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
