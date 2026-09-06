from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from docguard_llm_v2.gate4_study import STAGE3_CONFIG_SHA256, generation_payload, sha256_file, write_canonical_json
from docguard_llm_v2.hf_backend import HuggingFaceChatBackend
from docguard_llm_v2.pipeline import generate_semantic_documentation_patch, load_config
from docguard_ml_v2.data_contract import load_jsonl, write_jsonl


EXPECTED_CONFIG = {
    "analysis_model": "Qwen/Qwen2.5-Coder-7B-Instruct",
    "writer_model": "Qwen/Qwen2.5-Coder-7B-Instruct",
    "repair_model": "Qwen/Qwen2.5-Coder-7B-Instruct",
    "temperature": 0.1,
    "max_tokens_analysis": 512,
    "max_tokens_writer": 512,
    "max_tokens_repair": 512,
    "top_k_documents": 3,
    "max_repair_attempts": 1,
}


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_external_inputs(root: Path, manifest_path: Path) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    manifest = _load_json(manifest_path)
    if manifest.get("status") != "READY_FOR_EXTERNAL_COMPUTE" or manifest.get("confirmation_accessed") is not False or manifest.get("confirmation_paths_allowed") is not False:
        raise ValueError("Gate 4 external input manifest is not safe/ready")
    for relative, expected in manifest.get("source_sha256", {}).items():
        path = root / relative
        if not path.is_file() or sha256_file(path) != expected:
            raise ValueError(f"Gate 4 source hash mismatch: {relative}")
    samples: list[dict[str, Any]] = []
    for name in ("primary_sample", "secondary_stress_sample"):
        item = manifest["inputs"][name]
        relative = str(item["path"])
        if "confirmation" in relative.casefold():
            raise ValueError("Confirmation path is forbidden in Gate 4")
        path = root / relative
        if sha256_file(path) != item["sha256"]:
            raise ValueError(f"Gate 4 sample hash mismatch: {name}")
        samples.extend(load_jsonl(path))
    keys = [(str(row.get("sample_name")), str(row.get("case_id"))) for row in samples]
    if len(keys) != len(set(keys)):
        raise ValueError("Duplicate sample/case keys detected in Gate 4 inputs")
    primary = [row for row in samples if row.get("sample_name") == "primary_natural_distribution"]
    if any(row.get("partition") != "development_validation" for row in primary):
        raise ValueError("Primary Gate 4 inputs must be development_validation only")
    if any(row.get("partition") not in {"development_train", "development_validation"} for row in samples):
        raise ValueError("External Gate 4 inputs must be development-only")
    config_path = root / manifest["inputs"]["stage3_config"]["path"]
    if sha256_file(config_path) != STAGE3_CONFIG_SHA256 or sha256_file(config_path) != manifest["inputs"]["stage3_config"]["sha256"]:
        raise ValueError("Stage 3 config hash mismatch")
    config = load_config(config_path)
    for key, expected in EXPECTED_CONFIG.items():
        if config.get(key) != expected:
            raise ValueError(f"Stage 3 frozen setting mismatch: {key}")
    return manifest, samples, config


def _result_row(row: dict[str, Any], *, backend: Any, config: dict[str, Any]) -> dict[str, Any]:
    payload = generation_payload(row)
    base = {
        "run_key": f"{row['sample_name']}::{row['case_id']}",
        "sample_name": row["sample_name"],
        "case_id": row["case_id"],
        "frozen_binary_prediction": True,
        "frozen_category_prediction": payload["predicted_category"],
        "retrieval_context_available": bool(payload["documentation_context_candidates"]),
    }
    if not payload["documentation_context_candidates"]:
        return {
            **base,
            "final_status": "retrieval_context_unavailable",
            "llm_call_count": 0,
            "generated_patch": None,
            "selected_target_document": None,
            "latency_seconds": 0.0,
            "stage3_result": None,
        }
    started = time.perf_counter()
    calls_before = int(getattr(backend, "call_count", 0))

    try:
        stage3 = generate_semantic_documentation_patch(
            docs_update_required=True,
            predicted_category=payload["predicted_category"],
            code_diff=payload["code_diff_excerpt"],
            docs_before=payload["docs_before_excerpt"],
            documentation_context_candidates=payload["documentation_context_candidates"],
            llm_backend=backend,
            config=config,
        )
    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        calls_after = int(getattr(backend, "call_count", calls_before))
        case_calls = max(0, calls_after - calls_before)

        stage3 = {
            "final_status": "human_review_required",
            "final_source": "none",
            "final_patch": None,
            "selected_document": None,
            "llm_call_count": case_calls,
            "execution_error": {
                "code": "invalid_structured_llm_output",
                "error_type": type(exc).__name__,
                "message": str(exc),
            },
        }

    return {
        **base,
        "final_status": stage3["final_status"],
        "llm_call_count": int(stage3["llm_call_count"]),
        "generated_patch": stage3.get("final_patch"),
        "selected_target_document": stage3.get("selected_document"),
        "latency_seconds": time.perf_counter() - started,
        "stage3_result": stage3,
    }


def _append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def pending_run_keys(samples: list[dict[str, Any]], checkpoint_rows: list[dict[str, Any]]) -> list[str]:
    completed = [str(row.get("run_key") or "") for row in checkpoint_rows]
    if len(completed) != len(set(completed)) or any(not key for key in completed):
        raise ValueError("Duplicate or empty run_key values in checkpoint")
    completed_set = set(completed)
    return [f"{row['sample_name']}::{row['case_id']}" for row in samples if f"{row['sample_name']}::{row['case_id']}" not in completed_set]


def _runtime_metadata(backend: HuggingFaceChatBackend) -> dict[str, Any]:
    torch = backend.torch
    import transformers
    import accelerate
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "accelerate": accelerate.__version__,
        "cuda_available": bool(torch.cuda.is_available()),
        "cuda_device_count": int(torch.cuda.device_count()),
        "cuda_devices": [torch.cuda.get_device_name(index) for index in range(torch.cuda.device_count())],
        "model": backend.model_name,
        "precision": "float16",
        "quantized": False,
    }


def _deterministic_archive(output_dir: Path, files: list[Path]) -> tuple[Path, str]:
    archive = output_dir / "gate4_external_return.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as handle:
        for path in sorted(files, key=lambda item: item.name):
            info = zipfile.ZipInfo(path.name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            handle.writestr(info, path.read_bytes())
    digest = sha256_file(archive)
    (output_dir / "gate4_external_return.sha256").write_text(f"{digest}  {archive.name}\n", encoding="utf-8", newline="\n")
    return archive, digest


def run(root: Path, manifest_path: Path, output_dir: Path) -> dict[str, Any]:
    manifest, samples, config = validate_external_inputs(root, manifest_path)
    checkpoint = output_dir / "development_generation_checkpoint.jsonl"
    existing = load_jsonl(checkpoint) if checkpoint.exists() else []
    existing_by_key = {str(row["run_key"]): row for row in existing}
    pending_keys = set(pending_run_keys(samples, existing))
    pending_available = [row for row in samples if f"{row['sample_name']}::{row['case_id']}" not in existing_by_key and row.get("retrieval_context_available")]
    backend = None
    if pending_available:
        backend = HuggingFaceChatBackend(EXPECTED_CONFIG["analysis_model"], seed=42, require_cuda=True)
    for row in samples:
        key = f"{row['sample_name']}::{row['case_id']}"
        if key not in pending_keys:
            continue
        result = _result_row(row, backend=backend, config=config)
        _append_jsonl(checkpoint, result)
        existing_by_key[key] = result
    ordered = [existing_by_key[f"{row['sample_name']}::{row['case_id']}"] for row in samples]
    if len(ordered) != len(samples):
        raise RuntimeError("Incomplete Gate 4 execution")
    results_path = output_dir / "development_generation_results.jsonl"
    write_jsonl(results_path, ordered)
    status_counts: dict[str, int] = {}
    safety_violations: dict[str, int] = {}
    execution_errors: dict[str, int] = {}

    for row in ordered:
        status_counts[row["final_status"]] = status_counts.get(row["final_status"], 0) + 1
        stage3 = row.get("stage3_result") or {}

        execution_error = stage3.get("execution_error") or {}
        if execution_error:
            code = str(execution_error.get("code") or "unknown")
            execution_errors[code] = execution_errors.get(code, 0) + 1

        for verifier_key in ("first_pass_verifier", "repair_verifier"):
            for violation in (stage3.get(verifier_key) or {}).get("violations") or []:
                code = str(violation.get("code") or "unknown")
                safety_violations[code] = safety_violations.get(code, 0) + 1
    runtime = _runtime_metadata(backend) if backend is not None else {"model_loaded": False, "reason": "all rows already checkpointed or context-unavailable"}
    receipt = {
        "schema_version": "gate4_external_run_receipt_v1",
        "status": "COMPLETED_DEVELOPMENT_ONLY",
        "input_manifest_sha256": sha256_file(manifest_path),
        "source_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip(),
        "processed_rows": len(ordered),
        "unique_case_ids": len({row["case_id"] for row in ordered}),
        "stage3_invocation_count": sum(row["retrieval_context_available"] for row in ordered),
        "llm_call_count": sum(row["llm_call_count"] for row in ordered),
        "final_status_counts": dict(sorted(status_counts.items())),
        "safety_violation_counts": dict(sorted(safety_violations.items())),
        "execution_error_counts": dict(sorted(execution_errors.items())),
        "results_sha256": sha256_file(results_path),
        "runtime": runtime,
        "confirmation_accessed": False,
    }
    receipt_path = output_dir / "gate4_external_run_receipt.json"
    write_canonical_json(receipt_path, receipt)
    archive, archive_sha = _deterministic_archive(output_dir, [results_path, receipt_path])
    return {**receipt, "return_archive": archive.name, "return_archive_sha256": archive_sha}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run development-only Gate 4 Qwen generation on CUDA.")
    parser.add_argument("--input-manifest", default="reports/final_v2/gate4/external_run_input_manifest.json")
    parser.add_argument("--output-dir", default="reports/final_v2/gate4/external_return")
    args = parser.parse_args()
    print(json.dumps(run(ROOT, ROOT / args.input_manifest, ROOT / args.output_dir), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
