from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from docguard_ml_v2.data_contract import VALID_LABEL_SOURCES


SAFE_MODEL_FIELDS = {"language", "code_changed_files", "code_diff_excerpt", "docs_before_excerpt"}
ALLOWED_CATEGORIES = {"api_reference", "configuration", "developer_setup", "model_contract", "other_documentation", "no_update"}
PRIMARY_STAGE2 = {"api_reference", "configuration", "developer_setup", "model_contract"}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def repo_id(row: dict[str, Any]) -> str:
    value = row.get("repository") or row.get("repo") or row.get("project_id")
    if not value:
        url = str(row.get("source_url") or row.get("url") or "")
        parts = url.split("github.com/")[-1].split("/")
        if len(parts) >= 2:
            value = "/".join(parts[:2])
    return str(value or "").lower()


def row_id(row: dict[str, Any], index: int) -> str:
    return str(row.get("case_id") or row.get("id") or f"row_{index}")


def pr_key(row: dict[str, Any]) -> str:
    repo = repo_id(row)
    pr = row.get("pr_number")
    return f"{repo}#{int(pr)}" if repo and pr is not None else ""


def safe_serialization(row: dict[str, Any]) -> dict[str, Any]:
    return {key: row.get(key) for key in SAFE_MODEL_FIELDS}


def audit(rows: list[dict[str, Any]], partition_manifest: dict[str, Any] | None, previously_seen_rows: list[dict[str, Any]]) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    warnings: list[str] = []
    ids = [row_id(row, index) for index, row in enumerate(rows, 1)]
    urls = [str(row.get("source_url") or row.get("url") or "") for row in rows if row.get("source_url") or row.get("url")]
    prs = [pr_key(row) for row in rows if pr_key(row)]
    for duplicate in [item for item, count in Counter(ids).items() if count > 1]:
        errors.append(f"duplicate case_id: {duplicate}")
    for duplicate in [item for item, count in Counter(urls).items() if count > 1]:
        errors.append(f"duplicate source_url: {duplicate}")
    for duplicate in [item for item, count in Counter(prs).items() if count > 1]:
        errors.append(f"duplicate PR: {duplicate}")
    for index, row in enumerate(rows, 1):
        rid = row_id(row, index)
        if row.get("candidate_evidence") and any(key.startswith("gold_") for key in row) and row.get("label_source") not in VALID_LABEL_SOURCES:
            errors.append(f"{rid}: candidate generated gold fields before human finalization")
        if row.get("human_review_complete") is not True:
            errors.append(f"{rid}: missing human review")
        if row.get("label_source") not in VALID_LABEL_SOURCES:
            errors.append(f"{rid}: unsupported final label_source")
        if row.get("gold_doc_category") not in ALLOWED_CATEGORIES:
            errors.append(f"{rid}: unsupported category {row.get('gold_doc_category')}")
        for field in SAFE_MODEL_FIELDS:
            value = row.get(field)
            if value is None or value == "" or value == []:
                if field == "docs_before_excerpt":
                    warnings.append(f"{rid}: empty docs_before_excerpt requires Gate 1 empty-doc disposition")
                else:
                    errors.append(f"{rid}: empty critical model field {field}")
        leaked = [key for key in safe_serialization(row) if key.startswith("gold_") or key.startswith("suggested_") or key.startswith("human_")]
        if leaked:
            errors.append(f"{rid}: gold/audit field present in safe input serialization: {leaked}")
        policy = str(row.get("docs_before_retrieval_policy") or "")
        if policy and "no_docs_changed_files" not in policy and any(term in policy for term in ["docs_changed_files", "docs_diff_excerpt", "docs_after_excerpt"]):
            errors.append(f"{rid}: docs_before provenance dependent on docs_changed_files/outcome docs")
        original = str(row.get("original_human_doc_category") or "")
        final = str(row.get("human_doc_category") or row.get("gold_doc_category") or "")
        if original and original not in PRIMARY_STAGE2 and original != "no_update" and final in PRIMARY_STAGE2:
            errors.append(f"{rid}: forced alias use from {original} to {final}")
    if partition_manifest and "repository_assignments" not in partition_manifest:
        manifest_counts = partition_manifest.get("partition_row_counts") or {}
        actual_counts = dict(Counter(str(row.get("partition") or "") for row in rows))
        for partition, expected_count in manifest_counts.items():
            if actual_counts.get(partition, 0) != expected_count:
                errors.append(f"{partition}: partition row count mismatch; expected {expected_count}, got {actual_counts.get(partition, 0)}")
        repos_by_partition: dict[str, set[str]] = defaultdict(set)
        for row in rows:
            repos_by_partition[str(row.get("partition") or "")].add(repo_id(row))
        for index, left in enumerate(list(repos_by_partition)):
            for right in list(repos_by_partition)[index + 1 :]:
                overlap = repos_by_partition[left] & repos_by_partition[right]
                if overlap:
                    errors.append(f"repository partition overlap {left}/{right}: {sorted(overlap)[:10]}")
    elif partition_manifest:
        assignments = partition_manifest.get("repository_assignments") or {}
        if partition_manifest.get("confirmation_sealed") is not True:
            errors.append("confirmation partition is not sealed")
        by_partition: dict[str, set[str]] = defaultdict(set)
        for repo, partition in assignments.items():
            by_partition[str(partition)].add(str(repo).lower())
        for index, row in enumerate(rows, 1):
            repo = repo_id(row)
            expected = str(assignments.get(repo) or "")
            actual = str(row.get("partition") or "")
            if expected and actual and actual != expected:
                errors.append(f"{row_id(row, index)}: partition recomputation/mismatch after labels; expected {expected}, got {actual}")
        partitions = list(by_partition)
        for i, left in enumerate(partitions):
            for right in partitions[i + 1 :]:
                overlap = by_partition[left] & by_partition[right]
                if overlap:
                    errors.append(f"repository partition overlap {left}/{right}: {sorted(overlap)[:10]}")
        seen = {repo_id(row) for row in previously_seen_rows}
        confirmation_seen = by_partition.get("confirmation", set()) & seen
        if confirmation_seen:
            errors.append(f"confirmation repository previously seen: {sorted(confirmation_seen)[:10]}")
    language_class: dict[str, Counter] = defaultdict(Counter)
    repo_counts = Counter()
    for row in rows:
        language_class[str(row.get("language") or "")][str(row.get("gold_docs_update_required"))] += 1
        repo_counts[repo_id(row)] += 1
    report = {
        "total_cases": len(rows),
        "migrated_rows": sum(1 for row in rows if row.get("migrated_from_human_reviewed_v1") is True),
        "newly_reviewed_rows": sum(1 for row in rows if row.get("migrated_from_human_reviewed_v1") is not True),
        "language_distribution": dict(Counter(str(row.get("language") or "") for row in rows)),
        "natural_binary_class_distribution": dict(Counter(str(row.get("gold_docs_update_required")) for row in rows)),
        "exact_human_category_distribution": dict(Counter(str(row.get("gold_doc_category")) for row in rows)),
        "stage2_coverage": {
            "primary_eligible": sum(1 for row in rows if row.get("gold_doc_category") in PRIMARY_STAGE2),
            "other_documentation_positive": sum(1 for row in rows if row.get("gold_doc_category") == "other_documentation"),
            "no_update": sum(1 for row in rows if row.get("gold_doc_category") == "no_update"),
        },
        "per_language_class_distribution": {lang: dict(counter) for lang, counter in language_class.items()},
        "per_repository_counts": dict(repo_counts),
        "confirmation_size": sum(1 for row in rows if row.get("partition") == "confirmation"),
        "confirmation_language_distribution": dict(Counter(str(row.get("language") or "") for row in rows if row.get("partition") == "confirmation")),
        "no_class_balancing_performed": True,
        "errors": errors,
        "warnings": warnings,
    }
    return errors, report


def write_markdown(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# Final Dataset V2 Audit Report",
        "",
        f"- Total cases: `{report['total_cases']}`",
        f"- Migrated rows: `{report['migrated_rows']}`",
        f"- Newly reviewed rows: `{report['newly_reviewed_rows']}`",
        f"- Language distribution: `{report['language_distribution']}`",
        f"- Natural binary class distribution: `{report['natural_binary_class_distribution']}`",
        f"- Exact human category distribution: `{report['exact_human_category_distribution']}`",
        f"- Stage-2 coverage: `{report['stage2_coverage']}`",
        f"- Confirmation size: `{report['confirmation_size']}`",
        f"- Confirmation language distribution: `{report['confirmation_language_distribution']}`",
        f"- Errors: `{len(report['errors'])}`",
        f"- Warnings: `{len(report['warnings'])}`",
        "",
        "NO CLASS BALANCING / OVERSAMPLING / UNDERSAMPLING / SMOTE.",
    ]
    if report["errors"]:
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    if report["warnings"]:
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {warning}" for warning in report["warnings"])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Final V2 human gold dataset and canonical repository partitions.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--partition-manifest")
    parser.add_argument("--previously-seen-dataset", action="append", default=[])
    parser.add_argument("--report", required=True)
    parser.add_argument("--json-report")
    args = parser.parse_args()
    rows = load_jsonl(Path(args.input))
    manifest = json.loads(Path(args.partition_manifest).read_text(encoding="utf-8")) if args.partition_manifest else None
    seen_rows = [row for path in args.previously_seen_dataset for row in load_jsonl(Path(path))]
    errors, report = audit(rows, manifest, seen_rows)
    write_markdown(Path(args.report), report)
    if args.json_report:
        Path(args.json_report).write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"status": "fail" if errors else "ok", "errors": len(errors), "report": args.report}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
