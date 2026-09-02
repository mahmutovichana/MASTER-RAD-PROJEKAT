from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from sklearn.model_selection import StratifiedGroupKFold

from docguard_ml_v2.data_contract import (
    PRIMARY_STAGE2_LABELS,
    SAFE_MODEL_FIELDS,
    binary_labels,
    category_eligible_rows,
    category_labels,
    load_jsonl,
    validate_final_gold_row,
)


DEVELOPMENT_PARTITIONS = {"development_train", "development_validation"}
CONFIRMATION_PARTITION = "confirmation"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _stable_row_identity(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "case_id": str(row["case_id"]),
        "repository": str(row["repository"]).strip().lower(),
        "partition": str(row["partition"]),
        "safe": {field: row.get(field) for field in SAFE_MODEL_FIELDS},
        "binary": bool(row["gold_docs_update_required"]),
        "category": str(row["gold_doc_category"]),
    }


def development_view_hash(rows: Iterable[dict[str, Any]]) -> str:
    digest = hashlib.sha256()
    for row in sorted(rows, key=lambda item: str(item["case_id"])):
        payload = json.dumps(_stable_row_identity(row), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        digest.update(payload.encode("utf-8"))
        digest.update(b"\n")
    return digest.hexdigest()


def load_development_rows(*, config_path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    config = load_config(config_path)
    gate1 = config["gate1"]
    gold_path = Path(gate1["gold_path"])
    actual_hash = sha256_file(gold_path)
    if actual_hash != gate1["gold_sha256"]:
        raise RuntimeError(f"Gate 1 SHA mismatch: expected {gate1['gold_sha256']}, got {actual_hash}")
    all_rows = load_jsonl(gold_path)
    development: list[dict[str, Any]] = []
    confirmation_count = 0
    for row in all_rows:
        validate_final_gold_row(row)
        partition = str(row["partition"])
        if partition == CONFIRMATION_PARTITION:
            confirmation_count += 1
            continue
        if partition not in DEVELOPMENT_PARTITIONS:
            raise RuntimeError(f"Unexpected partition {partition!r}")
        development.append(row)
    if len(development) != int(gate1["expected_development_rows"]):
        raise RuntimeError(f"Development row mismatch: {len(development)}")
    if confirmation_count != int(gate1["expected_confirmation_rows"]):
        raise RuntimeError(f"Confirmation row mismatch: {confirmation_count}")
    if any(row["partition"] == CONFIRMATION_PARTITION for row in development):
        raise RuntimeError("Fail-closed loader admitted confirmation")
    metadata = {
        "gold_sha256": actual_hash,
        "development_rows": len(development),
        "confirmation_rows_excluded": confirmation_count,
        "development_view_sha256": development_view_hash(development),
    }
    return development, metadata


def _valid_splits(rows: list[dict[str, Any]], labels: list[Any], splits: int, seed: int) -> list[tuple[list[int], list[int]]] | None:
    groups = [str(row["repository"]).strip().lower() for row in rows]
    cv = StratifiedGroupKFold(n_splits=splits, shuffle=True, random_state=seed)
    assignments = list(cv.split(rows, labels, groups))
    required = set(labels)
    seen_validation_repositories: set[str] = set()
    for train_idx, val_idx in assignments:
        train_repos = {groups[index] for index in train_idx}
        val_repos = {groups[index] for index in val_idx}
        if train_repos & val_repos or seen_validation_repositories & val_repos:
            return None
        if set(labels[index] for index in train_idx) != required or set(labels[index] for index in val_idx) != required:
            return None
        seen_validation_repositories.update(val_repos)
    if seen_validation_repositories != set(groups):
        return None
    return assignments


def make_outer_folds(rows: list[dict[str, Any]], *, task: str, config: dict[str, Any]) -> tuple[list[dict[str, Any]], int]:
    if task == "binary":
        task_rows = rows
        labels: list[Any] = binary_labels(task_rows)
        candidates = [int(config["cross_validation"]["outer"]["requested_splits"])]
    elif task == "category":
        task_rows = category_eligible_rows(rows, allowed_partitions=DEVELOPMENT_PARTITIONS)
        labels = category_labels(task_rows)
        candidates = [int(value) for value in config["cross_validation"]["category_fallback_splits"]]
    else:
        raise ValueError(f"Unknown task {task!r}")
    assignments = None
    selected_splits = 0
    for splits in candidates:
        assignments = _valid_splits(task_rows, labels, splits, int(config["seed"]))
        if assignments is not None:
            selected_splits = splits
            break
    if assignments is None:
        raise RuntimeError(f"No valid preregistered repository-disjoint fold count for {task}")
    fold_by_repository: dict[str, int] = {}
    for fold, (_, val_idx) in enumerate(assignments):
        for index in val_idx:
            repository = str(task_rows[index]["repository"]).strip().lower()
            previous = fold_by_repository.setdefault(repository, fold)
            if previous != fold:
                raise RuntimeError(f"Repository {repository} assigned to multiple folds")
    records: list[dict[str, Any]] = []
    by_repository: dict[str, list[tuple[dict[str, Any], Any]]] = defaultdict(list)
    for row, label in zip(task_rows, labels):
        by_repository[str(row["repository"]).strip().lower()].append((row, label))
    for repository in sorted(by_repository):
        items = by_repository[repository]
        records.append({
            "task": task,
            "fold": fold_by_repository[repository],
            "repository": repository,
            "case_count": len(items),
            "label_distribution": json.dumps(dict(sorted(Counter(str(label) for _, label in items).items())), sort_keys=True),
            "language_distribution": json.dumps(dict(sorted(Counter(str(row.get("language") or "unknown").lower() for row, _ in items).items())), sort_keys=True),
        })
    return records, selected_splits


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0]) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_fold_map(path: Path, *, task: str) -> dict[str, int]:
    result: dict[str, int] = {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["task"] != task:
                raise RuntimeError(f"Unexpected task in {path}: {row['task']}")
            repository = row["repository"]
            fold = int(row["fold"])
            if repository in result:
                raise RuntimeError(f"Duplicate repository in fold file: {repository}")
            result[repository] = fold
    return result


def safe_code_view(row: dict[str, Any]) -> str:
    language = str(row.get("language") or "unknown").strip().lower() or "unknown"
    raw_files = row.get("code_changed_files") or []
    files = raw_files if isinstance(raw_files, list) else [raw_files]
    normalized = "\n".join(str(item).replace("\\", "/") for item in files if str(item).strip())
    return f"<language>\n{language}\n<changed_files>\n{normalized}\n<code_diff>\n{str(row.get('code_diff_excerpt') or '')}"


def safe_docs_view(row: dict[str, Any]) -> str:
    return str(row.get("docs_before_excerpt") or "")


def append_registry(path: Path, record: dict[str, Any]) -> None:
    required = {"run_id", "task", "family", "outer_fold", "config", "random_seed", "source_commit", "gold_sha", "status"}
    missing = sorted(required - set(record))
    if missing:
        raise ValueError(f"Registry record missing fields: {missing}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def assert_registered_family(config: dict[str, Any], family: str) -> None:
    if family not in config["families"]:
        raise ValueError(f"Unregistered Gate 2 family: {family}")


def assert_inner_repo_disjoint(rows: list[dict[str, Any]], train_idx: Iterable[int], val_idx: Iterable[int]) -> None:
    train_repos = {str(rows[index]["repository"]).strip().lower() for index in train_idx}
    val_repos = {str(rows[index]["repository"]).strip().lower() for index in val_idx}
    overlap = train_repos & val_repos
    if overlap:
        raise RuntimeError(f"Inner repository leakage: {sorted(overlap)[:3]}")


def primary_labels() -> list[str]:
    return list(PRIMARY_STAGE2_LABELS)
