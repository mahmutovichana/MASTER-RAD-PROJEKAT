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

os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

from experiments.posthoc_stage3_s1.scripts.retrieval import (
    EMBEDDING_MODEL_ID,
    EMBEDDING_LOGICAL_BATCH_SIZE,
    EMBEDDING_MAX_LENGTH,
    EMBEDDING_REVISION,
    RERANKER_MODEL_ID,
    RERANKER_MAX_LENGTH,
    RERANKER_REVISION,
    QwenDenseEncoder,
    QwenReranker,
    path_aware_lexical_top_documents,
)
from experiments.posthoc_stage3_s1.scripts.repository_corpus import DocumentChunk
from experiments.posthoc_stage3_s1.scripts.s1_pipeline import (
    GENERATOR_MODEL_ID,
    GENERATOR_REVISION,
    QwenStructuredGenerator,
    SchemaRetryingGenerator,
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


class ControlledIncompleteCriticOnce:
    """Canary-only fault injection; retry still uses the real frozen generator."""

    def __init__(self, backend: QwenStructuredGenerator):
        self.backend = backend
        self.calls = 0

    def generate_json(self, *, purpose: str, prompt: str) -> dict[str, Any]:
        self.calls += 1
        if self.calls == 1:
            return {
                "target_fit": True,
                "useful": True,
                "style_fit": True,
                "unsupported_claims": ["Windows is required"],
                "unnecessary_content": [],
                "decision": "REPAIR",
                "repair_instructions": ["Remove the unsupported Windows claim"],
            }
        return self.backend.generate_json(purpose=purpose, prompt=prompt)


def controlled_reranker_memory_checks(torch: Any) -> dict[str, Any]:
    documents = [str(index) for index in range(5)]
    adaptive = object.__new__(QwenReranker)
    adaptive.torch = torch
    adaptive.last_score_diagnostics = {}

    def split_injection(query: str, batch: list[str]) -> list[float]:
        if len(batch) > 2:
            raise torch.cuda.OutOfMemoryError(f"controlled reranker OOM at {len(batch)}")
        return [int(document) / 10.0 for document in batch]

    adaptive._score_batch = split_injection
    scores = adaptive.score("synthetic query", documents)
    if scores != [0.0, 0.1, 0.2, 0.3, 0.4]:
        raise RuntimeError("Controlled adaptive reranker split did not preserve document order")
    if adaptive.last_score_diagnostics["attempted_batch_sizes"] != [5, 2, 3, 1, 2]:
        raise RuntimeError("Controlled adaptive reranker split was not deterministic")

    single = object.__new__(QwenReranker)
    single.torch = torch
    single.last_score_diagnostics = {}
    single._score_batch = lambda query, batch: (_ for _ in ()).throw(torch.cuda.OutOfMemoryError("controlled single-item OOM"))
    try:
        single.score("synthetic query", ["0"])
    except torch.cuda.OutOfMemoryError:
        if not single.last_score_diagnostics["single_item_oom"]:
            raise RuntimeError("Controlled single-item reranker OOM was not recorded")
    else:
        raise RuntimeError("Controlled single-item reranker OOM did not fail closed")

    unrelated = object.__new__(QwenReranker)
    unrelated.torch = torch
    unrelated.last_score_diagnostics = {}
    unrelated._score_batch = lambda query, batch: (_ for _ in ()).throw(RuntimeError("controlled unrelated failure"))
    try:
        unrelated.score("synthetic query", ["0", "1"])
    except RuntimeError as exc:
        if str(exc) != "controlled unrelated failure":
            raise
    else:
        raise RuntimeError("Unrelated reranker RuntimeError did not propagate")

    return {
        "synthetic_input_count": len(documents),
        "output_count": len(scores),
        "original_order_preserved": True,
        "no_candidate_dropped": True,
        "recursive_split_exercised": True,
        "single_item_oom_fails_closed": True,
        "unrelated_runtime_error_propagates": True,
        "diagnostics": adaptive.last_score_diagnostics,
    }


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
            GENERATOR_MODEL_ID: GENERATOR_REVISION,
        },
        "inactive_model_revisions_documented_not_loaded": {
            EMBEDDING_MODEL_ID: EMBEDDING_REVISION,
            RERANKER_MODEL_ID: RERANKER_REVISION,
        },
        "resolved_revisions": {},
        "repair_count": 0,
    }

    lexical_query = "configuration cache mode shared"
    lexical_chunks = [
        DocumentChunk("docs/api.md", "API", ("API",), "API endpoints and request fields.", 0),
        DocumentChunk("docs/config.md", "Cache", ("Configuration", "Cache"), "The cache mode supports shared configuration.", 0),
        DocumentChunk("docs/config.md", "Legacy", ("Configuration", "Legacy"), "Legacy unrelated option.", 1),
        DocumentChunk("docs/setup.md", "Setup", ("Setup",), "Install and configure the service.", 0),
    ]
    lexical_first = timed_stage(
        receipt,
        "active_lexical_retrieval_canary",
        lambda: path_aware_lexical_top_documents(lexical_query, lexical_chunks),
    )
    lexical_second = path_aware_lexical_top_documents(lexical_query, lexical_chunks)
    first_identity = [(item.chunk.path, item.chunk.chunk_index, item.lexical_score) for item in lexical_first]
    second_identity = [(item.chunk.path, item.chunk.chunk_index, item.lexical_score) for item in lexical_second]
    if first_identity != second_identity or len(lexical_first) != 3 or len({item.chunk.path for item in lexical_first}) != 3:
        raise RuntimeError("Active lexical retrieval canary is not deterministic top-3 distinct-document retrieval")
    receipt["active_retrieval"] = {
        "retrieval_method": "PATH_AWARE_LEXICAL_TOP3",
        "deterministic": True,
        "top_k_distinct_documents": 3,
        "embedding_model_loaded": False,
        "reranker_model_loaded": False,
        "historical_embedding_and_reranker_revisions_documented_only": True,
    }

    generator = timed_stage(receipt, "generator_4bit_nf4_load", lambda: QwenStructuredGenerator(cache_dir=cache_dir))
    revision = resolved_revision(generator.model)
    receipt["resolved_revisions"][GENERATOR_MODEL_ID] = revision
    if revision != GENERATOR_REVISION:
        raise RuntimeError(f"Generator revision mismatch: {revision}")
    quantizer = getattr(generator.model, "hf_quantizer", None)
    if quantizer is None:
        raise RuntimeError("Generator is not using the frozen 4-bit quantized runtime")
    structured = SchemaRetryingGenerator(generator)

    plan_prompt = (
        "Return JSON only. Given evidence that config key `cacheMode` changes from `local` to `shared`, create a plan with keys "
        "update_needed, target_document, target_section, change_type, developer_facing_effect, facts_to_document, "
        "facts_not_supported, style_observations, minimal_update_intent. Target docs/configuration.md, section Cache."
    )
    plan_one = timed_stage(receipt, "deterministic_plan_json_first", lambda: structured.generate_json(purpose="documentation_plan", prompt=plan_prompt))
    plan_two = timed_stage(receipt, "deterministic_plan_json_repeat", lambda: structured.generate_json(purpose="documentation_plan", prompt=plan_prompt))
    require_keys(plan_one, {"update_needed", "target_document", "target_section", "change_type", "developer_facing_effect", "facts_to_document", "facts_not_supported", "style_observations", "minimal_update_intent"}, "plan")
    if plan_one != plan_two:
        raise RuntimeError("Greedy generator produced non-identical repeated plan JSON")

    critic_prompt = (
        "Return JSON only with grounded, target_fit, useful, style_fit, unsupported_claims, unnecessary_content, decision, "
        "repair_instructions. Evidence supports only `cacheMode: shared`; candidate patch also claims Windows is required. "
        "Set decision to REPAIR and instruct removal of the unsupported Windows claim."
    )
    critic = timed_stage(receipt, "structured_critic_json", lambda: structured.generate_json(purpose="critic", prompt=critic_prompt))
    require_keys(critic, {"grounded", "target_fit", "useful", "style_fit", "unsupported_claims", "unnecessary_content", "decision", "repair_instructions"}, "critic")
    if critic.get("decision") != "REPAIR":
        raise RuntimeError("Canary critic did not exercise the required bounded repair path")
    repair_prompt = (
        "Return JSON only with target_document, target_section, patch_markdown. Repair exactly once: remove the unsupported "
        "Windows claim and retain only the grounded statement that `cacheMode` now uses `shared`."
    )
    repaired = timed_stage(receipt, "single_bounded_repair", lambda: structured.generate_json(purpose="repair", prompt=repair_prompt))
    require_keys(repaired, {"target_document", "target_section", "patch_markdown"}, "repair")
    receipt["repair_count"] = 1
    controlled = SchemaRetryingGenerator(ControlledIncompleteCriticOnce(generator))
    timed_stage(receipt, "controlled_schema_correction_retry", lambda: controlled.generate_json(purpose="critic", prompt=critic_prompt))
    controlled_diagnostic = controlled.diagnostics[-1]
    if not controlled_diagnostic["schema_retry_used"] or not controlled_diagnostic["schema_retry_valid"]:
        raise RuntimeError("Controlled schema-correction retry did not validate successfully")
    receipt["structured_call_diagnostics"] = [*structured.diagnostics, controlled_diagnostic]
    receipt["schema_correction_retry_exercised"] = True
    receipt["schema_correction_retries_in_controlled_exercise"] = 1
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
