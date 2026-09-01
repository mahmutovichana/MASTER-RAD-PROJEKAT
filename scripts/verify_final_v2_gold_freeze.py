from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from docguard_ml_v2.data_contract import PRIMARY_STAGE2_LABELS, SAFE_MODEL_FIELDS, validate_final_gold_row


DEFAULT_MANIFEST = PROJECT_ROOT / "reports/final_v2/GOLD_FREEZE_MANIFEST.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_number}: expected JSON object")
            rows.append(row)
    return rows


def repo_id(row: dict[str, Any]) -> str:
    return str(row.get("repository") or "").strip().lower().removesuffix(".git")


def repo_pr_key(row: dict[str, Any]) -> tuple[str, str]:
    return repo_id(row), str(row.get("pr_number") or "")


def safe_input_key(row: dict[str, Any]) -> tuple[str, str, str, str]:
    return (
        str(row.get("language") or ""),
        json.dumps(row.get("code_changed_files"), ensure_ascii=False, sort_keys=True),
        str(row.get("code_diff_excerpt") or ""),
        str(row.get("docs_before_excerpt") or ""),
    )


def count_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    positives = sum(row.get("gold_docs_update_required") is True for row in rows)
    negatives = sum(row.get("gold_docs_update_required") is False for row in rows)
    return {
        "rows": len(rows),
        "positive": positives,
        "negative": negatives,
        "category_counts": dict(sorted(Counter(str(row.get("gold_doc_category") or "") for row in rows).items())),
        "language_counts": dict(sorted(Counter(str(row.get("language") or "unknown") for row in rows).items())),
        "repository_count": len({repo_id(row) for row in rows}),
    }


def duplicate_groups(rows: list[dict[str, Any]], key_name: str) -> list[dict[str, Any]]:
    key_fn = {
        "case_id": lambda row: str(row.get("case_id") or ""),
        "repo_pr": repo_pr_key,
        "safe_input": safe_input_key,
    }[key_name]
    groups: dict[Any, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[key_fn(row)].append(row)
    duplicates: list[dict[str, Any]] = []
    for key, group in groups.items():
        if len(group) <= 1:
            continue
        labels = sorted({f"{row.get('gold_docs_update_required')}::{row.get('gold_doc_category')}" for row in group})
        duplicates.append(
            {
                "key": str(key),
                "rows": len(group),
                "case_ids": [str(row.get("case_id")) for row in group],
                "labels": labels,
                "conflicting_labels": len(labels) > 1,
            }
        )
    return duplicates


def verify(manifest_path: Path = DEFAULT_MANIFEST, *, project_root: Path = PROJECT_ROOT) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    if not manifest_path.exists():
        return {
            "status": "FAIL",
            "errors": [f"freeze manifest does not exist: {manifest_path}"],
            "warnings": [],
        }

    manifest = load_json(manifest_path)
    if manifest.get("gate") != 1:
        errors.append("freeze manifest gate must be 1")
    if manifest.get("confirmation_accessed_by_gate_1") is not False:
        errors.append("freeze manifest must state confirmation_accessed_by_gate_1=false")
    if manifest.get("confirmation_sealed") is not True:
        errors.append("freeze manifest must state confirmation_sealed=true")
    if manifest.get("safe_model_fields") != SAFE_MODEL_FIELDS:
        errors.append("safe_model_fields changed")

    gold_path = project_root / manifest.get("canonical_dataset_path", "")
    partition_path = project_root / manifest.get("partition_manifest_path", "")
    completion_path = project_root / manifest.get("completion_audit_path", "")

    for label, path in {
        "gold file": gold_path,
        "partition manifest": partition_path,
        "completion audit": completion_path,
    }.items():
        if not path.exists():
            errors.append(f"{label} missing: {path}")

    rows: list[dict[str, Any]] = []
    if gold_path.exists():
        if sha256_file(gold_path) != manifest.get("canonical_dataset_sha256"):
            errors.append("canonical gold SHA-256 mismatch")
        rows = load_jsonl(gold_path)
        if len(rows) != manifest.get("row_count"):
            errors.append("row count mismatch")
        for row in rows:
            try:
                validate_final_gold_row(row)
            except ValueError as exc:
                errors.append(str(exc))
        empty_docs = [str(row.get("case_id")) for row in rows if not str(row.get("docs_before_excerpt") or "").strip()]
        if empty_docs:
            errors.append(f"{len(empty_docs)} rows have empty docs_before_excerpt")
        for key_name in ["case_id", "repo_pr"]:
            dupes = duplicate_groups(rows, key_name)
            if dupes:
                errors.append(f"{key_name} duplicate groups: {len(dupes)}")
        safe_dupes = duplicate_groups(rows, "safe_input")
        safe_conflicts = [group for group in safe_dupes if group["conflicting_labels"]]
        if safe_conflicts:
            errors.append(f"conflicting labels for identical model-safe input groups: {len(safe_conflicts)}")
        elif safe_dupes:
            warnings.append(f"identical model-safe input duplicate groups without label conflict: {len(safe_dupes)}")

    if partition_path.exists():
        if sha256_file(partition_path) != manifest.get("partition_manifest_sha256"):
            errors.append("partition manifest SHA-256 mismatch")
        partition_manifest = load_json(partition_path)
        if partition_manifest.get("confirmation_sealed") is not True:
            errors.append("partition manifest confirmation_sealed is not true")

    if completion_path.exists() and sha256_file(completion_path) != manifest.get("completion_audit_sha256"):
        errors.append("completion audit SHA-256 mismatch")

    if rows:
        by_partition: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in rows:
            by_partition[str(row.get("partition") or "")].append(row)
        for partition, expected in (manifest.get("split_counts") or {}).items():
            actual = count_rows(by_partition.get(partition, []))
            if actual["rows"] != expected.get("rows"):
                errors.append(f"{partition} row count mismatch")
            if actual["positive"] != expected.get("positive"):
                errors.append(f"{partition} positive count mismatch")
            if actual["negative"] != expected.get("negative"):
                errors.append(f"{partition} negative count mismatch")
        partitions = sorted(by_partition)
        for index, left in enumerate(partitions):
            for right in partitions[index + 1 :]:
                repo_overlap = {repo_id(row) for row in by_partition[left]} & {repo_id(row) for row in by_partition[right]}
                case_overlap = {str(row.get("case_id")) for row in by_partition[left]} & {str(row.get("case_id")) for row in by_partition[right]}
                source_overlap = {repo_pr_key(row) for row in by_partition[left]} & {repo_pr_key(row) for row in by_partition[right]}
                if repo_overlap:
                    errors.append(f"repository overlap between {left} and {right}: {len(repo_overlap)}")
                if case_overlap:
                    errors.append(f"case overlap between {left} and {right}: {len(case_overlap)}")
                if source_overlap:
                    errors.append(f"source PR overlap between {left} and {right}: {len(source_overlap)}")

    return {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "primary_labels": PRIMARY_STAGE2_LABELS,
        "safe_model_fields": SAFE_MODEL_FIELDS,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the Final V2 Gate 1 frozen human-gold identity without reading confirmation results.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    result = verify(args.manifest)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
