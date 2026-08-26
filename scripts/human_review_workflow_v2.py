from __future__ import annotations

import csv
import hashlib
import json
import random
from collections import Counter
from pathlib import Path
from typing import Any

from sklearn.metrics import cohen_kappa_score


EVIDENCE_FIELDS = [
    "case_id",
    "repository",
    "pr_number",
    "language",
    "code_changed_files",
    "code_diff_excerpt",
    "docs_before_excerpt",
]
SUGGESTED_FIELDS = ["suggested_docs_update_required", "suggested_doc_category", "suggested_notes"]
HUMAN_FIELDS = ["human_docs_update_required", "human_doc_category", "human_label_notes", "review_status"]
REVIEWER_FIELDS = EVIDENCE_FIELDS + SUGGESTED_FIELDS + HUMAN_FIELDS + ["review_row_hash"]
ALLOWED_STATUSES = {"pending", "approved", "excluded"}
POSITIVE_CATEGORIES = {"api_reference", "configuration", "developer_setup", "model_contract", "other_documentation"}
ALLOWED_CATEGORIES = POSITIVE_CATEGORIES | {"no_update"}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
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


def stringify(value: Any) -> str:
    if isinstance(value, list):
        return json.dumps(value, ensure_ascii=False)
    if value is None:
        return ""
    return str(value)


def normalize_for_hash(row: dict[str, Any]) -> dict[str, str]:
    return {field: stringify(row.get(field)) for field in EVIDENCE_FIELDS}


def review_row_hash(row: dict[str, Any]) -> str:
    payload = json.dumps(normalize_for_hash(row), ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def parse_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    text = str(value or "").strip().lower()
    if text in {"true", "1", "yes", "y"}:
        return True
    if text in {"false", "0", "no", "n"}:
        return False
    return None


def normalize_status(value: Any) -> tuple[str, bool]:
    text = str(value or "").strip().lower()
    if text == "exclude":
        return "excluded", True
    if text in ALLOWED_STATUSES:
        return text, False
    return text, False


def make_review_row(row: dict[str, Any]) -> dict[str, Any]:
    out = {field: row.get(field) for field in EVIDENCE_FIELDS}
    out["suggested_docs_update_required"] = row.get("suggested_docs_update_required", "")
    out["suggested_doc_category"] = row.get("suggested_doc_category", "")
    out["suggested_notes"] = row.get("suggested_notes") or row.get("suggested_reason") or ""
    out["human_docs_update_required"] = ""
    out["human_doc_category"] = ""
    out["human_label_notes"] = ""
    out["review_status"] = "pending"
    out["review_row_hash"] = review_row_hash(out)
    return out


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REVIEWER_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: stringify(row.get(field)) for field in REVIEWER_FIELDS})


def read_csv(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def read_review_file(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() == ".csv":
        return read_csv(path)
    return load_jsonl(path)


def validate_taxonomy(row: dict[str, Any]) -> tuple[bool, str]:
    status, _normalized = normalize_status(row.get("review_status"))
    if status not in ALLOWED_STATUSES:
        return False, "invalid_status"
    if status != "approved":
        return False, "not_approved"
    docs_required = parse_bool(row.get("human_docs_update_required"))
    if docs_required is None:
        return False, "missing_required_human_field"
    category = str(row.get("human_doc_category") or "").strip()
    if category not in ALLOWED_CATEGORIES:
        return False, "invalid_category"
    if docs_required is False and category != "no_update":
        return False, "negative_must_be_no_update"
    if docs_required is True and category not in POSITIVE_CATEGORIES:
        return False, "positive_requires_positive_category"
    return True, "ok"


def validate_integrity(row: dict[str, Any]) -> tuple[bool, str]:
    expected = str(row.get("review_row_hash") or "")
    actual = review_row_hash(row)
    if not expected:
        return False, "missing_review_row_hash"
    if expected != actual:
        return False, "immutable_evidence_modified"
    return True, "ok"


def label_tuple(row: dict[str, Any]) -> tuple[Any, str, str]:
    return (parse_bool(row.get("human_docs_update_required")), str(row.get("human_doc_category") or ""), str(row.get("review_status") or ""))


def progress(rows: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(rows)
    statuses = Counter(normalize_status(row.get("review_status") or "pending")[0] or "pending" for row in rows)
    approved = [row for row in rows if normalize_status(row.get("review_status"))[0] == "approved"]
    positive_approved = [row for row in approved if parse_bool(row.get("human_docs_update_required")) is True]
    return {
        "total": total,
        "pending": statuses.get("pending", 0),
        "approved": statuses.get("approved", 0),
        "excluded": statuses.get("excluded", 0),
        "percentage_complete": ((statuses.get("approved", 0) + statuses.get("excluded", 0)) / total) if total else 0.0,
        "approved_docs_update_counts": dict(Counter(str(parse_bool(row.get("human_docs_update_required"))) for row in approved)),
        "approved_positive_taxonomy_counts": dict(Counter(str(row.get("human_doc_category") or "") for row in positive_approved)),
        "language_counts": dict(Counter(str(row.get("language") or "") for row in rows)),
        "repository_counts": dict(Counter(str(row.get("repository") or "") for row in rows)),
    }


def reviewer_overlap_agreement(left: list[dict[str, Any]], right: list[dict[str, Any]]) -> dict[str, Any]:
    left_by_id = {str(row.get("case_id")): row for row in left if str(row.get("review_status") or "") == "approved"}
    right_by_id = {str(row.get("case_id")): row for row in right if str(row.get("review_status") or "") == "approved"}
    ids = sorted(set(left_by_id) & set(right_by_id))
    left_binary = [parse_bool(left_by_id[cid].get("human_docs_update_required")) for cid in ids]
    right_binary = [parse_bool(right_by_id[cid].get("human_docs_update_required")) for cid in ids]
    binary_agreement = sum(1 for a, b in zip(left_binary, right_binary) if a == b) / len(ids) if ids else 0.0
    positive_ids = [cid for cid in ids if parse_bool(left_by_id[cid].get("human_docs_update_required")) is True and parse_bool(right_by_id[cid].get("human_docs_update_required")) is True]
    left_cat = [str(left_by_id[cid].get("human_doc_category") or "") for cid in positive_ids]
    right_cat = [str(right_by_id[cid].get("human_doc_category") or "") for cid in positive_ids]
    conflicts = [
        {"case_id": cid, "reviewer_a": left_by_id[cid], "reviewer_b": right_by_id[cid]}
        for cid in ids
        if label_tuple(left_by_id[cid]) != label_tuple(right_by_id[cid])
    ]
    return {
        "overlap_size": len(ids),
        "binary_agreement": binary_agreement,
        "binary_cohens_kappa": float(cohen_kappa_score(left_binary, right_binary)) if len(ids) >= 2 else 0.0,
        "positive_category_overlap": len(positive_ids),
        "positive_category_agreement": sum(1 for a, b in zip(left_cat, right_cat) if a == b) / len(positive_ids) if positive_ids else 0.0,
        "positive_category_cohens_kappa": float(cohen_kappa_score(left_cat, right_cat)) if len(positive_ids) >= 2 else 0.0,
        "conflicts": conflicts,
    }


def deterministic_sample(rows: list[dict[str, Any]], target: int, seed: int) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    groups: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        groups.setdefault(str(row.get("repository") or ""), []).append(row)
    for repo_rows in groups.values():
        repo_rows.sort(key=lambda row: str(row.get("case_id") or ""))
        rng.shuffle(repo_rows)
    repos = sorted(groups)
    rng.shuffle(repos)
    ordered: list[dict[str, Any]] = []
    while any(groups[repo] for repo in repos):
        for repo in repos:
            if groups[repo]:
                ordered.append(groups[repo].pop(0))
    return ordered[: min(target, len(ordered))]
