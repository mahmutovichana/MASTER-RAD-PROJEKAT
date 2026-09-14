from __future__ import annotations

import argparse
import csv
import gc
import hashlib
import json
import logging
import multiprocessing
import os
import random
import subprocess
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np

from experiments.posthoc_stage3_s1.scripts.kaggle_development_runner import cuda_snapshot, host_ram, package_versions
from experiments.posthoc_stage3_s1.scripts.repository_corpus import (
    BareGitRepositoryProvider,
    DocumentChunk,
    discover_candidates,
    resolve_pre_change_source,
    semantic_chunks,
)
from experiments.posthoc_stage3_s1.scripts.retrieval import (
    EMBEDDING_MODEL_ID,
    EMBEDDING_REVISION,
    RERANKER_MODEL_ID,
    RERANKER_REVISION,
    QwenDenseEncoder,
    QwenReranker,
    RankedChunk,
    chunk_text,
    cosine_dense_scores,
    lexical_scores,
)
from experiments.posthoc_stage3_s1.scripts.s1_pipeline import (
    GENERATOR_MODEL_ID,
    GENERATOR_REVISION,
    QwenStructuredGenerator,
    S1Agent,
    S1Configuration,
    build_retrieval_query,
)


FROZEN_SHA = "38f9afb479f738081301172176d3133e4056bd7c"
MEMBERSHIP_COUNT = 200
CONTROLLED_TARGET_COUNT = 79
GRID = ((5, 5), (5, 10), (10, 5), (10, 10))
THRESHOLDS = (0.35, 0.50, 0.65)
VARIANTS = ("P1", "P2")
PROMPT_SELECTION_POPULATIONS = (50, 75, 100)
PROMPT_SELECTION_MINIMUM_REVIEWABLE = 20


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def append_jsonl(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(value, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def atomic_jsonl(path: Path, values: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as handle:
        for value in values:
            handle.write(json.dumps(value, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_case_id(case_id: str) -> str:
    return hashlib.sha256(case_id.encode()).hexdigest()[:20]


def safe_model_row(row: dict[str, Any]) -> dict[str, Any]:
    """Whitelist the only fields allowed to reach retrieval/generation prompts."""
    allowed = (
        "case_id", "repository", "language", "code_changed_files", "code_diff_excerpt", "docs_before_excerpt",
        "frozen_category_prediction", "predicted_category", "sample_name", "partition",
    )
    return {key: row.get(key) for key in allowed}


def git_head(root: Path) -> str:
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True, capture_output=True, text=True).stdout.strip()


def assert_frozen_checkout(root: Path) -> None:
    actual = git_head(root)
    if actual != FROZEN_SHA:
        raise RuntimeError(f"Frozen checkout mismatch: expected {FROZEN_SHA}, got {actual}")


def assert_materialized(path: Path) -> None:
    prefix = path.read_bytes()[:80]
    if prefix.startswith(b"version https://git-lfs.github.com/spec"):
        raise RuntimeError(f"Required Git LFS object is not materialized: {path}")


def valid_score_checkpoint(path: Path, case_id: str, document_count: int) -> bool:
    if not path.is_file() or path.name.endswith(".tmp"):
        return False
    try:
        with np.load(path, allow_pickle=False) as arrays:
            required = {"case_id", "query_embedding", "document_embeddings", "lexical_scores", "dense_scores"}
            if not required.issubset(arrays.files) or str(arrays["case_id"].item()) != case_id:
                return False
            query = arrays["query_embedding"]
            documents = arrays["document_embeddings"]
            lexical = arrays["lexical_scores"]
            dense = arrays["dense_scores"]
            if query.shape != (1024,) or documents.shape != (document_count, 1024):
                return False
            if lexical.shape != (document_count,) or dense.shape != (document_count,):
                return False
            return bool(np.isfinite(query).all() and np.isfinite(documents).all() and np.isfinite(lexical).all() and np.isfinite(dense).all())
    except (OSError, ValueError, KeyError, EOFError):
        return False


def chunk_to_dict(value: DocumentChunk) -> dict[str, Any]:
    return {
        "path": value.path,
        "heading": value.heading,
        "heading_path": list(value.heading_path),
        "text": value.text,
        "chunk_index": value.chunk_index,
        "priority_tier": value.priority_tier,
        "path_distance": value.path_distance,
        "identifier_overlap": value.identifier_overlap,
    }


def chunk_from_dict(value: dict[str, Any]) -> DocumentChunk:
    return DocumentChunk(
        value["path"], value["heading"], tuple(value["heading_path"]), value["text"], value["chunk_index"],
        value["priority_tier"], value["path_distance"], value["identifier_overlap"],
    )


def load_unique_jsonl(path: Path, key_name: str) -> dict[str, dict[str, Any]]:
    values = {}
    for row in read_jsonl(path):
        key = str(row[key_name])
        if key in values and values[key] != row:
            raise RuntimeError(f"Conflicting duplicate checkpoint key {key} in {path}")
        if key in values:
            raise RuntimeError(f"Duplicate checkpoint key {key} in {path}")
        values[key] = row
    return values


def reranker_candidate_indices(chunks: list[DocumentChunk], lexical: np.ndarray, dense: np.ndarray) -> list[int]:
    union: set[int] = set()
    for lexical_k, dense_k in GRID:
        union.update(sorted(range(len(chunks)), key=lambda i: (-float(lexical[i]), chunks[i].path, chunks[i].chunk_index))[:lexical_k])
        union.update(sorted(range(len(chunks)), key=lambda i: (-float(dense[i]), chunks[i].path, chunks[i].chunk_index))[:dense_k])
    return sorted(union)


def valid_reranker_record(record: Any, case_id: str, candidate_indices: list[int]) -> bool:
    if not isinstance(record, dict) or record.get("case_id") != case_id:
        return False
    scores = record.get("scores")
    expected_keys = [str(index) for index in candidate_indices]
    if not isinstance(scores, dict) or set(scores) != set(expected_keys):
        return False
    if "candidate_indices" in record and record["candidate_indices"] != candidate_indices:
        return False
    try:
        values = [float(scores[key]) for key in expected_keys]
    except (TypeError, ValueError, KeyError):
        return False
    return len(values) == len(candidate_indices) and all(np.isfinite(value) and 0.0 <= value <= 1.0 for value in values)


def load_valid_reranker_checkpoints(path: Path, expected_indices: dict[str, list[int]]) -> dict[str, dict[str, Any]]:
    if not path.is_file() or path.name.endswith(".tmp"):
        return {}
    values: dict[str, dict[str, Any]] = {}
    seen_case_ids: set[str] = set()
    for encoded_line in path.read_bytes().splitlines():
        if not encoded_line.strip():
            continue
        try:
            line = encoded_line.decode("utf-8")
            row = json.loads(line)
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        if not isinstance(row, dict) or not isinstance(row.get("case_id"), str):
            continue
        case_id = row["case_id"]
        if case_id in seen_case_ids:
            raise RuntimeError(f"Duplicate reranker checkpoint case_id {case_id} in {path}")
        seen_case_ids.add(case_id)
        if case_id not in expected_indices:
            raise RuntimeError(f"Unexpected reranker checkpoint case_id {case_id} in {path}")
        if valid_reranker_record(row, case_id, expected_indices[case_id]):
            values[case_id] = row
    return values


def assign_cases_to_workers(rows: list[dict[str, Any]], missing_case_ids: set[str], worker_count: int) -> list[list[str]]:
    if worker_count < 1:
        raise ValueError("worker_count must be positive")
    assignments = [[] for _ in range(worker_count)]
    for frozen_index, row in enumerate(rows):
        if row["case_id"] in missing_case_ids:
            assignments[frozen_index % worker_count].append(row["case_id"])
    return assignments


def reranker_worker_count(cuda_device_count: int) -> int:
    return 2 if cuda_device_count >= 2 else 1


def merge_reranker_sources(
    rows: list[dict[str, Any]],
    expected_indices: dict[str, list[int]],
    sources: list[dict[str, dict[str, Any]]],
) -> dict[str, dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for source in sources:
        for case_id, record in source.items():
            if case_id in merged:
                raise RuntimeError(f"Duplicate reranker checkpoint case_id across shards: {case_id}")
            if case_id not in expected_indices or not valid_reranker_record(record, case_id, expected_indices[case_id]):
                raise RuntimeError(f"Invalid or unexpected reranker checkpoint case_id: {case_id}")
            merged[case_id] = record
    expected_case_ids = [row["case_id"] for row in rows]
    missing = [case_id for case_id in expected_case_ids if case_id not in merged]
    unexpected = sorted(set(merged) - set(expected_case_ids))
    if missing or unexpected:
        raise RuntimeError(f"Reranker shard merge identity mismatch: missing={missing}, unexpected={unexpected}")
    return {case_id: merged[case_id] for case_id in expected_case_ids}


def reranker_process_worker(
    worker_id: int,
    device_index: int,
    tasks: list[dict[str, Any]],
    shard_path_text: str,
    receipt_path_text: str,
    cache_dir: str,
) -> None:
    import torch

    started = time.monotonic()
    shard_path = Path(shard_path_text)
    receipt_path = Path(receipt_path_text)
    expected = {task["case_id"]: task["candidate_indices"] for task in tasks}
    completed = load_valid_reranker_checkpoints(shard_path, expected)
    reused_count = len(completed)
    try:
        torch.cuda.set_device(device_index)
        reranker = QwenReranker(cache_dir=cache_dir, device=f"cuda:{device_index}")
        if getattr(reranker.model.config, "_commit_hash", None) != RERANKER_REVISION:
            raise RuntimeError("Reranker revision mismatch")
        for task in tasks:
            case_id = task["case_id"]
            if case_id in completed:
                continue
            values = reranker.score(task["query"], task["documents"])
            record = {
                "case_id": case_id,
                "candidate_indices": task["candidate_indices"],
                "scores": {str(index): float(score) for index, score in zip(task["candidate_indices"], values)},
                "reranker_runtime_diagnostics": reranker.last_score_diagnostics,
                "worker_id": worker_id,
                "worker_device": f"cuda:{device_index}",
            }
            if not valid_reranker_record(record, case_id, task["candidate_indices"]):
                raise RuntimeError(f"Invalid reranker result for {case_id}")
            completed[case_id] = record
            atomic_jsonl(shard_path, [completed[item["case_id"]] for item in tasks if item["case_id"] in completed])
        atomic_jsonl(shard_path, [completed[task["case_id"]] for task in tasks])
        atomic_json(receipt_path, {
            "state": "COMPLETE",
            "worker_id": worker_id,
            "device": f"cuda:{device_index}",
            "assigned_case_count": len(tasks),
            "reused_case_count": reused_count,
            "new_case_count": len(tasks) - reused_count,
            "runtime_seconds": time.monotonic() - started,
        })
    except Exception as exc:
        atomic_json(receipt_path, {
            "state": "FAILED",
            "worker_id": worker_id,
            "device": f"cuda:{device_index}",
            "assigned_case_count": len(tasks),
            "reused_case_count": reused_count,
            "runtime_seconds": time.monotonic() - started,
            "error_type": type(exc).__name__,
            "error": str(exc),
        })
        raise


class PersistentBackend:
    def __init__(self, backend: QwenStructuredGenerator, path: Path):
        self.backend = backend
        self.path = path
        self.cache = {}
        for row in read_jsonl(path):
            key = (row["purpose"], row["prompt_sha256"])
            if key in self.cache and self.cache[key] != row["response"]:
                raise RuntimeError(f"Conflicting cached model call: {key}")
            self.cache[key] = row["response"]

    def generate_json(self, *, purpose: str, prompt: str) -> dict[str, Any]:
        prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()
        key = (purpose, prompt_hash)
        if key in self.cache:
            return self.cache[key]
        response = self.backend.generate_json(purpose=purpose, prompt=prompt)
        append_jsonl(self.path, {"purpose": purpose, "prompt_sha256": prompt_hash, "response": response})
        self.cache[key] = response
        return response


def retrieval_metric(ranks: list[int | None]) -> dict[str, Any]:
    n = len(ranks)
    return {
        "n": n,
        "hit_at_1": sum(rank == 1 for rank in ranks) / n,
        "hit_at_3": sum(rank is not None and rank <= 3 for rank in ranks) / n,
        "mrr": sum(0.0 if rank is None else 1.0 / rank for rank in ranks) / n,
    }


def outcome_summary(results: dict[str, dict[str, Any]], case_ids: list[str], threshold: float) -> dict[str, Any]:
    selected = []
    for case_id in case_ids:
        value = results[case_id]
        confidence = float((value.get("target_decision") or {}).get("confidence") or 0.0)
        if confidence < threshold:
            value = {"state": "ABSTAINED_NO_TARGET", "repair_count": 0, "target_decision": value.get("target_decision")}
        selected.append(value)
    n = len(selected)
    accepted = [item for item in selected if item["state"] == "ACCEPTED"]
    generated = [item for item in selected if item.get("patch")]
    unsupported = [item for item in selected if item["state"] == "ABSTAINED_UNSUPPORTED_CLAIMS" or (item.get("critic") or {}).get("unsupported_claims") or item.get("deterministic_unsupported_claims")]
    target_violations = [item for item in selected if item.get("patch") and str(item["patch"].get("target_document") or "") != str((item.get("target_decision") or {}).get("target_document") or "")]
    return {
        "n": n,
        "generation_invocation_rate": len(generated) / n,
        "accepted_output_coverage": len(accepted) / n,
        "abstention_rate": sum(str(item["state"]).startswith("ABSTAINED_") for item in selected) / n,
        "execution_error_rate": sum(item["state"] == "FAILED_EXECUTION" for item in selected) / n,
        "unsupported_fact_violation_rate": len(unsupported) / n,
        "target_not_retrieved_rate": len(target_violations) / n,
        "first_pass_accept_rate": sum(item["state"] == "ACCEPTED" and item.get("repair_count") == 0 for item in selected) / n,
        "repaired_accept_rate": sum(item["state"] == "ACCEPTED" and item.get("repair_count") == 1 for item in selected) / n,
        "state_counts": dict(sorted(Counter(item["state"] for item in selected).items())),
    }


def prompt_selection_case_ids(rows: list[dict[str, Any]], population: int = 50) -> list[str]:
    if len(rows) != MEMBERSHIP_COUNT or population not in PROMPT_SELECTION_POPULATIONS:
        raise ValueError("Prompt-selection membership requires 200 frozen rows and population 50, 75, or 100")
    primary = sorted((row["case_id"] for row in rows[:100]), key=lambda case_id: hashlib.sha256(f"42:{case_id}".encode()).hexdigest())
    secondary = sorted((row["case_id"] for row in rows[100:]), key=lambda case_id: hashlib.sha256(f"42:{case_id}".encode()).hexdigest())
    selected = [*primary[:25], *secondary[:25]]
    if population >= 75:
        selected.extend([*primary[25:38], *secondary[25:37]])
    if population >= 100:
        selected.extend([*primary[38:50], *secondary[37:50]])
    if len(selected) != population or len(set(selected)) != population:
        raise RuntimeError("Prompt-selection subset construction failed")
    return selected


def paired_prompt_run_keys(rows: list[dict[str, Any]], population: int) -> list[str]:
    return [f"{variant}:{case_id}" for case_id in prompt_selection_case_ids(rows, population) for variant in VARIANTS]


def selected_prompt_missing_run_keys(case_ids: list[str], selected_variant: str, completed_keys: set[str]) -> list[str]:
    if selected_variant not in VARIANTS:
        raise ValueError("Selected prompt variant must be P1 or P2")
    return [f"{selected_variant}:{case_id}" for case_id in case_ids if f"{selected_variant}:{case_id}" not in completed_keys]


def next_prompt_selection_population(population: int, reviewable_pairs: int) -> int:
    if population not in PROMPT_SELECTION_POPULATIONS:
        raise ValueError("Invalid paired prompt-selection population")
    if reviewable_pairs >= PROMPT_SELECTION_MINIMUM_REVIEWABLE or population == 100:
        return population
    return population + 25


def reviewable_pair_count(case_ids: list[str], completed_rows: dict[str, dict[str, Any]]) -> int:
    count = 0
    for case_id in case_ids:
        p1 = completed_rows[f"P1:{case_id}"]["result"]
        p2 = completed_rows[f"P2:{case_id}"]["result"]
        patch1 = str((p1.get("patch") or {}).get("patch_markdown") or "")
        patch2 = str((p2.get("patch") or {}).get("patch_markdown") or "")
        count += bool(patch1 and patch2 and patch1 != patch2)
    return count


def select_prompt_from_completed_blind_review(sheet: Path, mapping_path: Path) -> dict[str, Any] | None:
    if not sheet.is_file() or not mapping_path.is_file():
        return None
    with sheet.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        return None
    mapping_rows = json.loads(mapping_path.read_text(encoding="utf-8"))["rows"]
    mapping = {row["review_item_id"]: row for row in mapping_rows}
    if len(mapping) != len(mapping_rows) or set(mapping) != {row.get("review_item_id") for row in rows}:
        raise RuntimeError("Blind review private mapping identity mismatch")
    judgment_dimensions = ("target_fit", "grounding", "usefulness", "style_fit")
    preference_counts = {"P1": 0, "P2": 0}
    positive_counts = {"P1": 0, "P2": 0}

    def candidate(value: str) -> str | None:
        normalized = str(value).strip().casefold().replace("candidate", "").replace("_", "").replace(" ", "")
        return normalized.upper() if normalized in {"a", "b"} else None

    def positive(value: str) -> bool | None:
        normalized = str(value).strip().casefold()
        if normalized in {"yes", "y", "true", "1", "positive"}:
            return True
        if normalized in {"no", "n", "false", "0", "negative"}:
            return False
        return None

    for row in rows:
        preference = candidate(row.get("reviewer_preference", ""))
        judgments = {
            (side, dimension): positive(row.get(f"reviewer_{dimension}_{side}", ""))
            for side in ("A", "B") for dimension in judgment_dimensions
        }
        if preference is None or any(value is None for value in judgments.values()):
            return None
        identity = mapping[row["review_item_id"]]
        preference_counts[identity[f"candidate_{preference}"]] += 1
        for side in ("A", "B"):
            prompt = identity[f"candidate_{side}"]
            positive_counts[prompt] += sum(bool(judgments[(side, dimension)]) for dimension in judgment_dimensions)
    if preference_counts["P1"] != preference_counts["P2"]:
        selected = max(preference_counts, key=preference_counts.get)
        selection_basis = "reviewer_preference"
    elif positive_counts["P1"] != positive_counts["P2"]:
        selected = max(positive_counts, key=positive_counts.get)
        selection_basis = "total_human_positive_judgments"
    else:
        selected = "P1"
        selection_basis = "preregistered_deterministic_tiebreaker"
    return {
        "selected_prompt_variant": selected,
        "selection_basis": selection_basis,
        "reviewer_preference_counts": preference_counts,
        "human_positive_judgment_counts": positive_counts,
        "reviewed_pair_count": len(rows),
    }


def write_blind_review(output: Path, rows: list[dict[str, Any]], outcomes: dict[str, dict[str, dict[str, Any]]]) -> dict[str, Any]:
    columns = [
        "review_item_id", "case_id", "code_changed_files", "code_diff_excerpt", "docs_before_excerpt",
        "candidate_A_target_document", "candidate_A_patch", "candidate_B_target_document", "candidate_B_patch",
        "reviewer_preference", "reviewer_target_fit_A", "reviewer_target_fit_B", "reviewer_grounding_A", "reviewer_grounding_B",
        "reviewer_usefulness_A", "reviewer_usefulness_B", "reviewer_style_fit_A", "reviewer_style_fit_B", "reviewer_notes",
    ]
    review_rows = []
    private_mapping = []
    by_id = {row["case_id"]: row for row in rows}
    for case_id in [row["case_id"] for row in rows]:
        p1 = outcomes["P1"][case_id]; p2 = outcomes["P2"][case_id]
        patch1 = str((p1.get("patch") or {}).get("patch_markdown") or "")
        patch2 = str((p2.get("patch") or {}).get("patch_markdown") or "")
        if not patch1 or not patch2 or patch1 == patch2:
            continue
        swap = int(hashlib.sha256(f"42:{case_id}".encode()).hexdigest(), 16) % 2 == 1
        a, b = (p2, p1) if swap else (p1, p2)
        item_id = f"S1-DEV-{len(review_rows) + 1:03d}"
        source = by_id[case_id]
        review_rows.append({
            "review_item_id": item_id, "case_id": case_id,
            "code_changed_files": json.dumps(source.get("code_changed_files") or []),
            "code_diff_excerpt": source.get("code_diff_excerpt") or "", "docs_before_excerpt": source.get("docs_before_excerpt") or "",
            "candidate_A_target_document": (a.get("target_decision") or {}).get("target_document") or "",
            "candidate_A_patch": (a.get("patch") or {}).get("patch_markdown") or "",
            "candidate_B_target_document": (b.get("target_decision") or {}).get("target_document") or "",
            "candidate_B_patch": (b.get("patch") or {}).get("patch_markdown") or "",
            **{column: "" for column in columns if column.startswith("reviewer_")},
        })
        private_mapping.append({"review_item_id": item_id, "candidate_A": "P2" if swap else "P1", "candidate_B": "P1" if swap else "P2"})
    sheet = output / "s1_development_blind_prompt_review.csv"
    mapping_path = output / "checkpoints/blind_review_private_mapping.json"
    if sheet.is_file() and mapping_path.is_file():
        with sheet.open("r", encoding="utf-8-sig", newline="") as handle:
            existing_rows = list(csv.DictReader(handle))
        nonreviewer_columns = [column for column in columns if not column.startswith("reviewer_")]
        existing_public = [{column: row.get(column, "") for column in nonreviewer_columns} for row in existing_rows]
        proposed_public = [{column: str(row.get(column, "")) for column in nonreviewer_columns} for row in review_rows]
        existing_mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
        if existing_public != proposed_public or existing_mapping.get("rows") != private_mapping:
            raise RuntimeError("Existing blind review does not match frozen paired subset")
        return {"status": "BLIND_DEVELOPMENT_REVIEW_REQUIRED", "row_count": len(existing_rows), "path": str(sheet), "sha256": sha256(sheet)}
    with sheet.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns); writer.writeheader(); writer.writerows(review_rows)
    atomic_json(mapping_path, {"seed": 42, "rows": private_mapping})
    return {"status": "BLIND_DEVELOPMENT_REVIEW_REQUIRED", "row_count": len(review_rows), "path": str(sheet), "sha256": sha256(sheet)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Frozen, resumable Gate 4 development-only S1 GPU study")
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("/kaggle/working/s1-development"))
    parser.add_argument("--cache-dir", default=os.environ.get("HF_HOME", "/kaggle/working/hf-cache"))
    parser.add_argument("--canary-receipt", type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    if not os.environ.get("HF_TOKEN"):
        raise RuntimeError("HF_TOKEN must be supplied through the Kaggle Secret environment")
    canary = json.loads(args.canary_receipt.read_text(encoding="utf-8"))
    if canary.get("state") != "CANARY_PASS" or canary.get("confirmation_accessed") is not False:
        raise RuntimeError("Development run forbidden unless the frozen canary receipt says CANARY_PASS")
    root = args.root.resolve(); output = args.output.resolve(); output.mkdir(parents=True, exist_ok=True)
    assert_frozen_checkout(root)
    if any(term in str(output).casefold() for term in ("confirmation", "gate6", "e0", "e1", "e2")):
        raise ValueError("Development output path enters a forbidden evaluation area")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", handlers=[logging.FileHandler(output / "execution.log", encoding="utf-8"), logging.StreamHandler()])
    log = logging.getLogger("s1-development")
    random.seed(42); np.random.seed(42)
    import torch
    torch.manual_seed(42); torch.cuda.manual_seed_all(42)

    primary_path = root / "reports/final_v2/gate4/primary_sample.jsonl"
    secondary_path = root / "reports/final_v2/gate4/secondary_stress_sample.jsonl"
    gold_paths = [root / "experiments/consolidated_enriched_training_v2/gold/train.jsonl", root / "experiments/consolidated_enriched_training_v2/gold/validation.jsonl"]
    for path in (primary_path, secondary_path, *gold_paths):
        assert_materialized(path)
    sampled = read_jsonl(primary_path) + read_jsonl(secondary_path)
    if len(sampled) != MEMBERSHIP_COUNT or len({row["case_id"] for row in sampled}) != MEMBERSHIP_COUNT:
        raise RuntimeError("Frozen development membership is not exactly 200 unique cases")
    gold = {}
    for path in gold_paths:
        for row in read_jsonl(path): gold[row["case_id"]] = row
    rows = []
    for item in sampled:
        row = dict(gold.get(item["case_id"], {})); row.update(item); rows.append(row)
    if sum(bool(row.get("synthetic_target_doc_path")) for row in rows) != CONTROLLED_TARGET_COUNT:
        raise RuntimeError("Controlled target evidence is not exactly 79 rows")

    runtime_manifest = {
        "state": "RUNNING", "frozen_git_sha": FROZEN_SHA, "confirmation_accessed": False,
        "gate6_row_level_human_data_accessed": False, "development_case_count": 200,
        "controlled_target_evidence_count": 79, "seed": 42, "cuda": cuda_snapshot(), "host_ram": host_ram(),
        "package_versions": package_versions(),
        "models": {EMBEDDING_MODEL_ID: EMBEDDING_REVISION, RERANKER_MODEL_ID: RERANKER_REVISION, GENERATOR_MODEL_ID: GENERATOR_REVISION},
        "source_sha256": {str(path.relative_to(root)): sha256(path) for path in (primary_path, secondary_path, *gold_paths)},
    }
    atomic_json(output / "runtime_manifest.json", runtime_manifest)
    checkpoints = output / "checkpoints"; corpus_dir = checkpoints / "repository_corpus"; score_dir = checkpoints / "retrieval_scores"
    corpus_dir.mkdir(parents=True, exist_ok=True); score_dir.mkdir(parents=True, exist_ok=True)

    provider = BareGitRepositoryProvider(checkpoints / "repository_cache")
    groups: dict[str, set[str]] = defaultdict(set); sources = {}
    for row in rows:
        source = resolve_pre_change_source(row, root=root); sources[row["case_id"]] = source
        if source.kind == "git_commit": groups[source.repository].add(source.revision)
    for repository, revisions in groups.items():
        if not all(provider.ensure_commits(repository, revisions).values()):
            raise RuntimeError(f"Explicit pre-change object unavailable in {repository}; HEAD fallback is forbidden")

    corpora: dict[str, list[DocumentChunk]] = {}
    for index, row in enumerate(rows, 1):
        path = corpus_dir / f"{safe_case_id(row['case_id'])}.json"
        if path.is_file():
            cached = json.loads(path.read_text(encoding="utf-8"))
            if cached["case_id"] != row["case_id"]: raise RuntimeError("Corpus cache identity mismatch")
            chunks = [chunk_from_dict(value) for value in cached["chunks"]]
        else:
            source = sources[row["case_id"]]
            if source.kind == "git_commit":
                paths = provider.list_paths(source.repository, source.revision)
                read = lambda p, s=source: provider.read_text(s.repository, s.revision, p)
            else:
                local = Path(source.local_root); paths = [p.relative_to(local).as_posix() for p in local.rglob("*") if p.is_file()]
                read = lambda p, local=local: (local / Path(p)).read_text(encoding="utf-8", errors="replace")
            discovered = discover_candidates(paths, changed_paths=list(row.get("code_changed_files") or []), code_diff=str(row.get("code_diff_excerpt") or ""))[:64]
            chunks = []
            for document, tier, distance, overlap in discovered:
                chunks.extend(semantic_chunks(document, read(document), max_chars=4000, priority_tier=tier, distance=distance, identifier_overlap=overlap))
            atomic_json(path, {"case_id": row["case_id"], "chunks": [chunk_to_dict(value) for value in chunks]})
        corpora[row["case_id"]] = chunks
    atomic_json(checkpoints / "repository_corpus_complete.json", {"state": "COMPLETE", "case_count": len(corpora)})
    log.info("Repository corpus complete: %d cases", len(corpora))

    missing_scores = [
        row for row in rows
        if not valid_score_checkpoint(score_dir / f"{safe_case_id(row['case_id'])}.npz", row["case_id"], len(corpora[row["case_id"]]))
    ]
    if missing_scores:
        dense = QwenDenseEncoder(cache_dir=args.cache_dir, batch_size=8)
        if getattr(dense.model.config, "_commit_hash", None) != EMBEDDING_REVISION: raise RuntimeError("Embedding revision mismatch")
        for row in missing_scores:
            case_id = row["case_id"]; chunks = corpora[case_id]; query = build_retrieval_query(safe_model_row(row))
            lexical = lexical_scores(query, chunks); embeddings = dense.encode([query, *[chunk_text(chunk) for chunk in chunks]])
            dense_scores = cosine_dense_scores(embeddings[0], embeddings[1:])
            target = score_dir / f"{safe_case_id(case_id)}.npz"; temporary = target.with_suffix(".npz.tmp")
            embedding_diagnostics = json.dumps(dense.last_encode_diagnostics, sort_keys=True)
            with temporary.open("wb") as handle: np.savez_compressed(handle, case_id=case_id, query_embedding=embeddings[0], document_embeddings=embeddings[1:], lexical_scores=lexical, dense_scores=dense_scores, embedding_runtime_diagnostics=embedding_diagnostics)
            os.replace(temporary, target)
        del dense; gc.collect(); torch.cuda.empty_cache(); torch.cuda.synchronize()
    atomic_json(checkpoints / "embedding_candidate_retrieval_complete.json", {"state": "COMPLETE", "case_count": 200})
    embedding_diagnostics = []
    for row in rows:
        path = score_dir / f"{safe_case_id(row['case_id'])}.npz"
        with np.load(path, allow_pickle=False) as arrays:
            if "embedding_runtime_diagnostics" in arrays.files:
                diagnostic = json.loads(str(arrays["embedding_runtime_diagnostics"].item()))
                diagnostic.update({"case_id": row["case_id"], "reused_without_recorded_diagnostics": False})
            else:
                diagnostic = {"case_id": row["case_id"], "configured_max_batch_size": 8, "effective_batch_sizes_used": None, "oom_split_count": None, "minimum_effective_batch_size": None, "single_item_oom": None, "reused_without_recorded_diagnostics": True}
            embedding_diagnostics.append(diagnostic)
    atomic_json(checkpoints / "embedding_runtime_diagnostics.json", {"case_count": 200, "cases": embedding_diagnostics})
    known_diagnostics = [item for item in embedding_diagnostics if not item["reused_without_recorded_diagnostics"]]
    effective_sizes = [size for item in known_diagnostics for size in item["effective_batch_sizes_used"]]
    runtime_manifest["embedding_microbatch"] = {
        "configured_max_batch_size": 8,
        "effective_batch_sizes_used": sorted(set(effective_sizes)),
        "oom_split_count": sum(item["oom_split_count"] for item in known_diagnostics),
        "minimum_effective_batch_size": min(effective_sizes) if effective_sizes else None,
        "single_item_oom": any(item["single_item_oom"] for item in known_diagnostics),
        "valid_pre_amendment_checkpoints_reused_without_diagnostics": sum(item["reused_without_recorded_diagnostics"] for item in embedding_diagnostics),
    }
    atomic_json(output / "runtime_manifest.json", runtime_manifest)
    log.info("Embedding and candidate retrieval complete: 200 cases")

    expected_reranker_indices: dict[str, list[int]] = {}
    for row in rows:
        case_id = row["case_id"]
        with np.load(score_dir / f"{safe_case_id(case_id)}.npz", allow_pickle=False) as arrays:
            expected_reranker_indices[case_id] = reranker_candidate_indices(
                corpora[case_id], arrays["lexical_scores"], arrays["dense_scores"]
            )
    reranker_path = checkpoints / "reranker_scores.jsonl"
    rerank_cache = load_valid_reranker_checkpoints(reranker_path, expected_reranker_indices)
    missing_rerank = [row for row in rows if row["case_id"] not in rerank_cache]
    available_reranker_workers = reranker_worker_count(torch.cuda.device_count())
    if missing_rerank and available_reranker_workers == 1:
        missing_ids = {row["case_id"] for row in missing_rerank}
        prior_two_worker_assignments = assign_cases_to_workers(rows, missing_ids, 2)
        for worker_id, case_ids in enumerate(prior_two_worker_assignments):
            shard_path = checkpoints / f"reranker_scores_worker_{worker_id}.jsonl"
            shard_expected = {case_id: expected_reranker_indices[case_id] for case_id in case_ids}
            for case_id, record in load_valid_reranker_checkpoints(shard_path, shard_expected).items():
                if case_id in rerank_cache:
                    raise RuntimeError(f"Duplicate reranker checkpoint case_id across global file and worker shard: {case_id}")
                rerank_cache[case_id] = record
        missing_rerank = [row for row in rows if row["case_id"] not in rerank_cache]
    reranker_worker_receipts: list[dict[str, Any]] = []
    if not missing_rerank:
        for receipt_path in sorted(checkpoints.glob("reranker_worker_*_receipt.json")):
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            if receipt.get("state") == "COMPLETE":
                reranker_worker_receipts.append(receipt)
    if missing_rerank:
        if available_reranker_workers == 2:
            missing_ids = {row["case_id"] for row in missing_rerank}
            assignments = assign_cases_to_workers(rows, missing_ids, 2)
            row_by_id = {row["case_id"]: row for row in rows}
            processes = []
            worker_paths = []
            context = multiprocessing.get_context("spawn")
            for worker_id, case_ids in enumerate(assignments):
                tasks = []
                for case_id in case_ids:
                    row = row_by_id[case_id]
                    indices = expected_reranker_indices[case_id]
                    tasks.append({
                        "case_id": case_id,
                        "candidate_indices": indices,
                        "query": build_retrieval_query(safe_model_row(row)),
                        "documents": [chunk_text(corpora[case_id][index]) for index in indices],
                    })
                shard_path = checkpoints / f"reranker_scores_worker_{worker_id}.jsonl"
                receipt_path = checkpoints / f"reranker_worker_{worker_id}_receipt.json"
                worker_paths.append((shard_path, receipt_path, {case_id: expected_reranker_indices[case_id] for case_id in case_ids}))
                process = context.Process(
                    target=reranker_process_worker,
                    args=(worker_id, worker_id, tasks, str(shard_path), str(receipt_path), args.cache_dir),
                )
                process.start()
                processes.append(process)
            for process in processes:
                process.join()
            failed_exit_codes = [process.exitcode for process in processes if process.exitcode != 0]
            if failed_exit_codes:
                raise RuntimeError(f"Reranker worker failure exit codes: {failed_exit_codes}")
            shard_caches = []
            for shard_path, receipt_path, expected in worker_paths:
                receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
                if receipt.get("state") != "COMPLETE":
                    raise RuntimeError(f"Reranker worker receipt is not complete: {receipt_path}")
                reranker_worker_receipts.append(receipt)
                shard_caches.append(load_valid_reranker_checkpoints(shard_path, expected))
            rerank_cache = merge_reranker_sources(rows, expected_reranker_indices, [rerank_cache, *shard_caches])
        else:
            single_started = time.monotonic()
            reranker = QwenReranker(cache_dir=args.cache_dir)
            if getattr(reranker.model.config, "_commit_hash", None) != RERANKER_REVISION: raise RuntimeError("Reranker revision mismatch")
            for row in missing_rerank:
                case_id = row["case_id"]
                chunks = corpora[case_id]
                indices = expected_reranker_indices[case_id]
                values = reranker.score(build_retrieval_query(safe_model_row(row)), [chunk_text(chunks[i]) for i in indices])
                record = {
                    "case_id": case_id,
                    "candidate_indices": indices,
                    "scores": {str(i): float(score) for i, score in zip(indices, values)},
                    "reranker_runtime_diagnostics": reranker.last_score_diagnostics,
                    "worker_id": 0,
                    "worker_device": "existing_single_worker_device_map",
                }
                if not valid_reranker_record(record, case_id, indices):
                    raise RuntimeError(f"Invalid reranker result for {case_id}")
                rerank_cache[case_id] = record
                atomic_jsonl(reranker_path, [rerank_cache[item["case_id"]] for item in rows if item["case_id"] in rerank_cache])
            single_receipt = {
                "state": "COMPLETE",
                "worker_id": 0,
                "device": "existing_single_worker_device_map",
                "assigned_case_count": len(missing_rerank),
                "reused_case_count": len(rows) - len(missing_rerank),
                "new_case_count": len(missing_rerank),
                "runtime_seconds": time.monotonic() - single_started,
            }
            reranker_worker_receipts.append(single_receipt)
            atomic_json(checkpoints / "reranker_worker_0_receipt.json", single_receipt)
            del reranker; gc.collect(); torch.cuda.empty_cache(); torch.cuda.synchronize()
    atomic_jsonl(reranker_path, [rerank_cache[row["case_id"]] for row in rows])
    reranker_diagnostics = []
    for row in rows:
        record = rerank_cache[row["case_id"]]
        diagnostic = record.get("reranker_runtime_diagnostics")
        reranker_diagnostics.append({
            "case_id": row["case_id"],
            "candidate_count": len(expected_reranker_indices[row["case_id"]]),
            "reused_without_recorded_diagnostics": diagnostic is None,
            **(diagnostic or {}),
        })
    atomic_json(checkpoints / "reranker_runtime_diagnostics.json", {"case_count": 200, "cases": reranker_diagnostics})
    known_reranker_diagnostics = [item for item in reranker_diagnostics if not item["reused_without_recorded_diagnostics"]]
    reranker_effective_sizes = [size for item in known_reranker_diagnostics for size in item["effective_batch_sizes_used"]]
    runtime_manifest["reranker_microbatch"] = {
        "forward_mode": "LAST_TOKEN_ONLY",
        "logits_to_keep": 1,
        "use_cache": False,
        "last_token_projection_is_exact_execution_optimization_not_scoring_method_change": True,
        "original_full_candidate_batch_attempted_first": True,
        "effective_batch_sizes_used": sorted(set(reranker_effective_sizes)),
        "total_oom_split_count": sum(item["oom_split_count"] for item in known_reranker_diagnostics),
        "minimum_effective_batch_size": min(reranker_effective_sizes) if reranker_effective_sizes else None,
        "single_item_oom": any(item["single_item_oom"] for item in known_reranker_diagnostics),
        "valid_pre_amendment_checkpoints_reused_without_diagnostics": sum(item["reused_without_recorded_diagnostics"] for item in reranker_diagnostics),
        "worker_count": len(reranker_worker_receipts),
        "worker_device_assignments": [item["device"] for item in reranker_worker_receipts],
        "worker_case_counts": [item["assigned_case_count"] for item in reranker_worker_receipts],
        "worker_runtime_seconds": [item["runtime_seconds"] for item in reranker_worker_receipts],
        "peak_allocated_cuda_bytes": [item.get("peak_allocated_cuda_bytes") for item in known_reranker_diagnostics],
    }
    atomic_json(output / "runtime_manifest.json", runtime_manifest)
    atomic_json(checkpoints / "reranking_complete.json", {"state": "COMPLETE", "case_count": 200})
    log.info("Reranking complete: 200 cases")

    retrieval: dict[str, dict[str, list[RankedChunk]]] = {f"l{l}_d{d}": {} for l, d in GRID}
    retrieval_metrics = {}
    retrieval_rows = []
    for lexical_k, dense_k in GRID:
        key = f"l{lexical_k}_d{dense_k}"; ranks = []
        for row in rows:
            case_id = row["case_id"]; chunks = corpora[case_id]; arrays = np.load(score_dir / f"{safe_case_id(case_id)}.npz")
            lexical = arrays["lexical_scores"]; dense_values = arrays["dense_scores"]
            lex_ids = sorted(range(len(chunks)), key=lambda i: (-float(lexical[i]), chunks[i].path, chunks[i].chunk_index))[:lexical_k]
            den_ids = sorted(range(len(chunks)), key=lambda i: (-float(dense_values[i]), chunks[i].path, chunks[i].chunk_index))[:dense_k]
            score_map = rerank_cache[case_id]["scores"]; ranked = [RankedChunk(chunks[i], float(lexical[i]), float(dense_values[i]), float(score_map[str(i)])) for i in set(lex_ids) | set(den_ids)]
            best = {}
            for value in ranked:
                if value.chunk.path not in best or value.reranker_score > best[value.chunk.path].reranker_score: best[value.chunk.path] = value
            top = sorted(best.values(), key=lambda value: (-value.reranker_score, value.chunk.path))[:3]; retrieval[key][case_id] = top
            retrieval_rows.append({"configuration": key, "case_id": case_id, "candidates": [{"path": v.chunk.path, "heading": v.chunk.heading, "lexical_score": v.lexical_score, "dense_score": v.dense_score, "reranker_score": v.reranker_score} for v in top]})
            target = row.get("synthetic_target_doc_path")
            if target:
                paths = [value.chunk.path for value in top]; ranks.append(paths.index(target) + 1 if target in paths else None)
        retrieval_metrics[key] = retrieval_metric(ranks)
    if any(value["n"] != 79 for value in retrieval_metrics.values()): raise RuntimeError("Target metrics escaped the controlled 79-row denominator")
    selected_key = sorted(retrieval_metrics, key=lambda key: (-retrieval_metrics[key]["hit_at_3"], -retrieval_metrics[key]["mrr"], -retrieval_metrics[key]["hit_at_1"], int(key.split("_")[0][1:]), int(key.split("_")[1][1:])))[0]
    atomic_json(output / "retrieval_metrics.json", {"controlled_only": True, "natural_target_ground_truth": False, "metrics": retrieval_metrics, "selected_retrieval_key": selected_key})
    retrieval_jsonl = output / "retrieval_results.jsonl"
    temporary = retrieval_jsonl.with_suffix(".jsonl.tmp"); temporary.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in retrieval_rows), encoding="utf-8"); os.replace(temporary, retrieval_jsonl)

    generation_path = output / "generation_results.jsonl"
    completed_rows = load_unique_jsonl(generation_path, "run_key")
    all_case_ids = [row["case_id"] for row in rows]
    allowed_run_keys = {f"{variant}:{case_id}" for variant in VARIANTS for case_id in all_case_ids}
    if set(completed_rows) - allowed_run_keys:
        raise RuntimeError("Generation checkpoint contains an unexpected variant or case identity")
    row_map = {row["case_id"]: row for row in rows}
    lexical_k = int(selected_key.split("_")[0][1:])
    dense_k = int(selected_key.split("_")[1][1:])
    generator = None
    backend = None
    newly_completed = 0

    def run_generation_keys(required_keys: list[str], phase: str) -> None:
        nonlocal generator, backend, newly_completed
        missing_keys = [key for key in required_keys if key not in completed_rows]
        if missing_keys and generator is None:
            generator = QwenStructuredGenerator(cache_dir=args.cache_dir)
            if getattr(generator.model.config, "_commit_hash", None) != GENERATOR_REVISION:
                raise RuntimeError("Generator revision mismatch")
            backend = PersistentBackend(generator, checkpoints / "model_call_cache.jsonl")
        for run_key in missing_keys:
            variant, case_id = run_key.split(":", 1)
            row = row_map[case_id]
            agent = S1Agent(backend, S1Configuration(lexical_k, dense_k, 3, 0.35, variant))
            result = agent.run(safe_model_row(row), retrieval[selected_key][case_id], document_corpus=corpora[case_id])
            record = {"run_key": run_key, "variant": variant, "case_id": case_id, "result": result, "execution_phase": phase}
            append_jsonl(generation_path, record)
            completed_rows[run_key] = record
            newly_completed += 1
            if newly_completed % 25 == 0:
                atomic_json(checkpoints / "generation_progress.json", {
                    "state": "RUNNING", "phase": phase, "completed_total": len(completed_rows),
                    "phase_required": len(required_keys), "last_run_key": run_key,
                })
                log.info("Generation checkpoint: %d total completed", len(completed_rows))

    plan_path = checkpoints / "prompt_selection_subset.json"
    if plan_path.is_file():
        prompt_plan = json.loads(plan_path.read_text(encoding="utf-8"))
        population = int(prompt_plan["paired_population"])
    else:
        population = 50
    while True:
        paired_case_ids = prompt_selection_case_ids(rows, population)
        paired_keys = paired_prompt_run_keys(rows, population)
        atomic_json(plan_path, {
            "seed": 42,
            "paired_population": population,
            "case_ids": paired_case_ids,
            "selection_source": "frozen membership and SHA256('42:' + case_id) only",
            "primary_count": sum(case_id in set(all_case_ids[:100]) for case_id in paired_case_ids),
            "secondary_count": sum(case_id in set(all_case_ids[100:]) for case_id in paired_case_ids),
            "maximum_paired_population": 100,
        })
        run_generation_keys(paired_keys, "PHASE_A_PAIRED_PROMPT_SELECTION")
        if any(key not in completed_rows for key in paired_keys):
            raise RuntimeError("Phase A paired prompt checkpoint is incomplete")
        reviewable_pairs = reviewable_pair_count(paired_case_ids, completed_rows)
        extended_population = next_prompt_selection_population(population, reviewable_pairs)
        if extended_population == population:
            break
        population = extended_population

    paired_case_set = set(paired_case_ids)
    losing_outside_subset = [
        key for key in completed_rows
        if key.split(":", 1)[1] not in paired_case_set
    ]
    selection_rows = [row_map[case_id] for case_id in paired_case_ids]
    paired_outcomes = {
        variant: {case_id: completed_rows[f"{variant}:{case_id}"]["result"] for case_id in paired_case_ids}
        for variant in VARIANTS
    }
    review = write_blind_review(output, selection_rows, paired_outcomes)
    mapping_path = checkpoints / "blind_review_private_mapping.json"
    prompt_selection = select_prompt_from_completed_blind_review(Path(review["path"]), mapping_path)
    if prompt_selection is None:
        if losing_outside_subset:
            raise RuntimeError("Losing prompt has results outside the frozen paired subset before human selection")
        selection = {
            "state": "PROMPT_SELECTION_BLIND_REVIEW_REQUIRED",
            "selected_retrieval_key": selected_key,
            "selected_threshold": None,
            "selected_prompt_variant": None,
            "paired_population": population,
            "reviewable_pair_count": reviewable_pairs,
            "review": review,
            "selection_uses_self_critic_metrics": False,
        }
        atomic_json(output / "development_selection_status.json", selection)
        atomic_json(checkpoints / "generation_progress.json", {
            "state": "PROMPT_SELECTION_BLIND_REVIEW_REQUIRED",
            "phase": "PHASE_A",
            "paired_population": population,
            "completed_paired_runs": len(paired_keys),
        })
        if generator is not None:
            del generator; gc.collect(); torch.cuda.empty_cache(); torch.cuda.synchronize()
        prompt_dir = Path(__file__).resolve().parents[1] / "prompts"
        atomic_json(output / "prompt_hashes.json", {path.name: sha256(path) for path in sorted(prompt_dir.glob("*.txt"))})
        atomic_json(output / "model_revision_receipt.json", canary.get("resolved_revisions", {}))
        runtime_manifest.update({"state": "PROMPT_SELECTION_BLIND_REVIEW_REQUIRED", "runtime_seconds": time.monotonic() - started, "final_cuda": cuda_snapshot(), "final_host_ram": host_ram()})
        atomic_json(output / "runtime_manifest.json", runtime_manifest)
        log.info("Paired prompt subset complete; blind human review required before Phase B")
        print("PROMPT_SELECTION_BLIND_REVIEW_REQUIRED")
        return 0

    selected_variant = prompt_selection["selected_prompt_variant"]
    losing_variant = "P2" if selected_variant == "P1" else "P1"
    invalid_losing_keys = [key for key in completed_rows if key.startswith(f"{losing_variant}:") and key.split(":", 1)[1] not in paired_case_set]
    if invalid_losing_keys:
        raise RuntimeError("Losing prompt result exists outside the frozen paired selection subset")
    selected_keys = [f"{selected_variant}:{case_id}" for case_id in all_case_ids]
    selected_missing_keys = selected_prompt_missing_run_keys(all_case_ids, selected_variant, set(completed_rows))
    run_generation_keys(selected_missing_keys, "PHASE_B_SELECTED_PROMPT_ONLY")
    if any(key not in completed_rows for key in selected_keys):
        raise RuntimeError("Selected prompt does not have all 200 development results")
    if generator is not None:
        del generator; gc.collect(); torch.cuda.empty_cache(); torch.cuda.synchronize()
    atomic_json(checkpoints / "generation_progress.json", {
        "state": "COMPLETE", "phase": "PHASE_B", "selected_prompt_variant": selected_variant,
        "selected_prompt_completed": len(selected_keys), "paired_population": population,
    })
    selected_outcomes = {case_id: completed_rows[f"{selected_variant}:{case_id}"]["result"] for case_id in all_case_ids}
    groups = {"all_development": all_case_ids, "primary": all_case_ids[:100], "secondary": all_case_ids[100:]}
    development_metrics = {
        str(threshold): {group: outcome_summary(selected_outcomes, ids, threshold) for group, ids in groups.items()}
        for threshold in THRESHOLDS
    }
    atomic_json(output / "development_metrics.json", {
        "confirmation_accessed": False,
        "self_critic_is_human_ground_truth": False,
        "selected_prompt_variant": selected_variant,
        "thresholds": list(THRESHOLDS),
        "metrics": development_metrics,
        "paired_prompt_selection_population": population,
    })
    selection = {
        "state": "DEVELOPMENT_METRICS_COMPLETE_SELECTED_PROMPT",
        "selected_retrieval_key": selected_key,
        "selected_threshold": None,
        "paired_population": population,
        "reviewable_pair_count": reviewable_pairs,
        "review": review,
        **prompt_selection,
    }
    atomic_json(output / "development_selection_status.json", selection)
    prompt_dir = Path(__file__).resolve().parents[1] / "prompts"
    atomic_json(output / "prompt_hashes.json", {path.name: sha256(path) for path in sorted(prompt_dir.glob("*.txt"))})
    atomic_json(output / "model_revision_receipt.json", canary.get("resolved_revisions", {}))
    runtime_manifest.update({"state": "DEVELOPMENT_METRICS_COMPLETE_SELECTED_PROMPT", "runtime_seconds": time.monotonic() - started, "final_cuda": cuda_snapshot(), "final_host_ram": host_ram()})
    atomic_json(output / "runtime_manifest.json", runtime_manifest)
    atomic_json(checkpoints / "development_metrics_complete.json", {"state": "COMPLETE", "selection_state": selection["state"]})
    log.info("Development metrics complete for human-selected prompt across 200 cases")
    print("DEVELOPMENT_METRICS_COMPLETE_SELECTED_PROMPT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
