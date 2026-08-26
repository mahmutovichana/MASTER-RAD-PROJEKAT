from __future__ import annotations

import hashlib
import json
import math
import random
import re
from collections import Counter
from pathlib import Path
from statistics import mean, median, pstdev
from typing import Any

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics.pairwise import cosine_similarity


GENERATION_FIELDS = {
    "case_id",
    "language",
    "code_changed_files",
    "code_diff_excerpt",
    "docs_before_excerpt",
    "documentation_context_candidates",
    "pred_doc_category",
    "generated_patch",
    "target_document_path",
}
REFERENCE_ONLY_FIELDS = {
    "docs_after",
    "docs_after_excerpt",
    "docs_diff_excerpt",
    "gold_patch_summary",
    "human_label_notes",
    "manual_label_notes",
    "gold_docs_update_required",
    "gold_doc_category",
    "actual_target_document_path",
    "reference_metrics",
}
HUMAN_DIMENSIONS = [
    "human_factual_correctness",
    "human_semantic_completeness",
    "human_developer_usefulness",
    "human_readability",
    "human_style_fit",
]
BLIND_FORBIDDEN_FIELDS = REFERENCE_ONLY_FIELDS | {
    "generation_source",
    "final_source",
    "repair_attempted",
    "verifier_result",
    "writer_confidence",
    "quality_label",
    "grounded_output",
    "historical_qwen_output",
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tokenize(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9_./:-]+", str(text or "").lower())


def generation_view(row: dict[str, Any]) -> dict[str, Any]:
    view = {key: row.get(key) for key in GENERATION_FIELDS if key in row}
    leaked = REFERENCE_ONLY_FIELDS & set(view)
    if leaked:
        raise ValueError(f"Reference-only fields entered generation view: {sorted(leaked)}")
    return view


def evaluation_reference_view(row: dict[str, Any]) -> dict[str, Any]:
    return {key: row.get(key) for key in REFERENCE_ONLY_FIELDS if key in row}


def patch_text(row: dict[str, Any]) -> str:
    patch = row.get("generated_patch")
    if isinstance(patch, dict):
        return str(patch.get("patch_markdown") or patch.get("text") or patch.get("preview") or "")
    return str(row.get("patch_markdown") or row.get("generated_patch_markdown") or patch or "")


def reference_text(row: dict[str, Any]) -> str:
    return str(row.get("docs_diff_excerpt") or row.get("gold_patch_summary") or row.get("docs_after_excerpt") or row.get("docs_after") or "")


def word_overlap(generated: str, reference: str) -> dict[str, float]:
    gen = set(tokenize(generated))
    ref = set(tokenize(reference))
    if not gen or not ref:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}
    precision = len(gen & ref) / len(gen)
    recall = len(gen & ref) / len(ref)
    f1 = (2 * precision * recall / (precision + recall)) if precision + recall else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}


def tfidf_cosine(generated: str, reference: str) -> float:
    if not generated.strip() or not reference.strip():
        return 0.0
    matrix = TfidfVectorizer().fit_transform([generated, reference])
    return float(cosine_similarity(matrix[0], matrix[1])[0][0])


def evaluate_reference_row(row: dict[str, Any]) -> dict[str, Any]:
    generated = patch_text(row)
    reference = reference_text(row)
    available = bool(reference.strip())
    metrics = {
        "case_id": row.get("case_id"),
        "reference_available": available,
        "word_overlap": word_overlap(generated, reference) if available else {"precision": 0.0, "recall": 0.0, "f1": 0.0},
        "tfidf_cosine": tfidf_cosine(generated, reference) if available else 0.0,
        "exact_match": generated.strip() == reference.strip() if available else False,
    }
    return metrics


def summarize_reference(rows: list[dict[str, Any]]) -> dict[str, Any]:
    metrics = [evaluate_reference_row(row) for row in rows]
    available = [item for item in metrics if item["reference_available"]]
    return {
        "reference_availability_rate": len(available) / len(rows) if rows else 0.0,
        "case_metrics": metrics,
        "mean_word_overlap_f1": mean([item["word_overlap"]["f1"] for item in available]) if available else 0.0,
        "mean_tfidf_cosine": mean([item["tfidf_cosine"] for item in available]) if available else 0.0,
        "note": "Reference metrics are diagnostic supporting evidence, not automatic semantic truth.",
    }


def sample_primary(rows: list[dict[str, Any]], *, seed: int, target_size: int) -> list[dict[str, Any]]:
    positives = [row for row in rows if row.get("pred_docs_update_required") is True or str(row.get("pred_docs_update_required")).lower() == "true"]
    rng = random.Random(seed)
    shuffled = list(positives)
    rng.shuffle(shuffled)
    return shuffled[: min(target_size, len(shuffled))]


def sample_stress(rows: list[dict[str, Any]], *, seed: int, per_category: int) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    output: list[dict[str, Any]] = []
    for category in ["api_reference", "configuration", "developer_setup", "model_contract"]:
        bucket = [row for row in rows if row.get("pred_doc_category") == category and (row.get("pred_docs_update_required") is True or str(row.get("pred_docs_update_required")).lower() == "true")]
        rng.shuffle(bucket)
        output.extend(bucket[:per_category])
    return output


def sample_manifest(source: Path, rows: list[dict[str, Any]], *, seed: int, method: str) -> dict[str, Any]:
    return {
        "source_hash": sha256_file(source),
        "seed": seed,
        "sampling_method": method,
        "prevalence": sum(1 for row in rows if row.get("pred_docs_update_required") is True or str(row.get("pred_docs_update_required")).lower() == "true") / len(rows) if rows else 0.0,
        "category_counts": dict(Counter(str(row.get("pred_doc_category") or "") for row in rows)),
        "language_counts": dict(Counter(str(row.get("language") or "") for row in rows)),
        "repository_counts": dict(Counter(str(row.get("repository") or "") for row in rows)),
    }


def build_blind_row(row: dict[str, Any]) -> dict[str, Any]:
    result = {
        "case_id": row.get("case_id"),
        "language": row.get("language"),
        "code_changed_files": row.get("code_changed_files"),
        "code_diff_excerpt": row.get("code_diff_excerpt"),
        "docs_before_excerpt": row.get("docs_before_excerpt"),
        "selected_target_document": row.get("target_document_path") or row.get("selected_document"),
        "generated_documentation_patch": patch_text(row),
        "review_status": "pending",
        "human_accept_as_is": "",
        "human_notes": "",
    }
    for dimension in HUMAN_DIMENSIONS:
        result[dimension] = None
    leaked = BLIND_FORBIDDEN_FIELDS & set(result)
    if leaked:
        raise ValueError(f"Blind review row leaked fields: {sorted(leaked)}")
    return result


def validate_review(row: dict[str, Any]) -> tuple[bool, str]:
    if str(row.get("review_status") or "").strip().lower() != "approved":
        return False, "not_approved"
    for dimension in HUMAN_DIMENSIONS:
        value = row.get(dimension)
        if not isinstance(value, int) or value < 1 or value > 5:
            return False, f"invalid_{dimension}"
    if str(row.get("human_accept_as_is") or "").strip().lower() not in {"yes", "no"}:
        return False, "invalid_human_accept_as_is"
    return True, "approved"


def summarize_human_reviews(rows: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {"total_approved": len(rows), "dimensions": {}}
    for dimension in HUMAN_DIMENSIONS:
        values = [int(row[dimension]) for row in rows]
        summary["dimensions"][dimension] = {
            "mean": mean(values) if values else 0.0,
            "median": median(values) if values else 0.0,
            "stddev": pstdev(values) if len(values) > 1 else 0.0,
            "distribution": dict(Counter(str(value) for value in values)),
        }
    accepts = [str(row.get("human_accept_as_is") or "").lower() == "yes" for row in rows]
    summary["accept_as_is_rate"] = sum(accepts) / len(accepts) if accepts else 0.0
    summary["composite_descriptive_mean"] = mean([mean([int(row[dim]) for dim in HUMAN_DIMENSIONS]) for row in rows]) if rows else 0.0
    return summary


def weighted_kappa(a: list[int], b: list[int]) -> float:
    if len(a) < 2:
        return 0.0
    return float(cohen_kappa_score(a, b, weights="quadratic"))


def yes_no_kappa(a: list[str], b: list[str]) -> float:
    if len(a) < 2:
        return 0.0
    return float(cohen_kappa_score(a, b))


def reviewer_agreement(left: list[dict[str, Any]], right: list[dict[str, Any]]) -> dict[str, Any]:
    left_by_id = {str(row.get("case_id")): row for row in left if validate_review(row)[0]}
    right_by_id = {str(row.get("case_id")): row for row in right if validate_review(row)[0]}
    ids = sorted(set(left_by_id) & set(right_by_id))
    result: dict[str, Any] = {"overlap_size": len(ids), "reliability_claim_allowed": len(ids) >= 20, "dimensions": {}}
    for dimension in HUMAN_DIMENSIONS:
        a = [int(left_by_id[cid][dimension]) for cid in ids]
        b = [int(right_by_id[cid][dimension]) for cid in ids]
        result["dimensions"][dimension] = {
            "raw_agreement": sum(1 for x, y in zip(a, b) if x == y) / len(ids) if ids else 0.0,
            "weighted_cohens_kappa": weighted_kappa(a, b),
        }
    accept_a = [str(left_by_id[cid].get("human_accept_as_is") or "").lower() for cid in ids]
    accept_b = [str(right_by_id[cid].get("human_accept_as_is") or "").lower() for cid in ids]
    result["accept_as_is"] = {
        "raw_agreement": sum(1 for x, y in zip(accept_a, accept_b) if x == y) / len(ids) if ids else 0.0,
        "cohens_kappa": yes_no_kappa(accept_a, accept_b),
    }
    return result


def bootstrap_mean_ci(values: list[float], *, seed: int = 42, n_bootstrap: int = 500) -> dict[str, float]:
    if not values:
        return {"low": 0.0, "high": 0.0}
    rng = np.random.default_rng(seed)
    means = []
    for _ in range(n_bootstrap):
        indexes = rng.integers(0, len(values), len(values))
        means.append(float(np.mean([values[index] for index in indexes])))
    return {"low": float(np.quantile(means, 0.025)), "high": float(np.quantile(means, 0.975))}

