from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.human_review_workflow_v2 import (
    POSITIVE_CATEGORIES,
    REVIEWER_FIELDS,
    parse_bool,
    review_context_hash,
    review_row_hash,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data/final_v2/human_review/consolidated_enriched_training_v1"
SOURCES = [
    (
        "natural_17880",
        ROOT / "data/final_v2/human_review/full_manual_review_17880/completed_natural_17880/merged_human_review.jsonl",
        "human",
    ),
    (
        "targeted_enrichment_1199",
        ROOT / "data/final_v2/expansion/targeted_positive_enrichment_v1/human_review/reviewed_batches/merged/merged_human_review.jsonl",
        "human",
    ),
    (
        "historical_4k_unique",
        ROOT / "data/final_v2/human_review/historical_4k_merged/merged_human_review.jsonl",
        "human",
    ),
    (
        "historical_300_gold_unique",
        ROOT / "data/external/project_case_study/generated/real_pr_gold_300_v1_high_medium.jsonl",
        "gold",
    ),
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def pr_key(row: dict[str, Any]) -> tuple[str, int]:
    repository = str(row.get("repository") or "").strip().lower().removesuffix(".git")
    return repository, int(row["pr_number"])


def normalize(row: dict[str, Any], label_kind: str) -> dict[str, Any]:
    normalized = {field: "" for field in REVIEWER_FIELDS}
    for field in REVIEWER_FIELDS:
        if field in row:
            normalized[field] = row[field]

    normalized["case_id"] = row.get("case_id") or f"github:{pr_key(row)[0]}#{pr_key(row)[1]}"
    normalized["repository"] = str(row.get("repository") or "").strip()
    normalized["pr_number"] = int(row["pr_number"])
    normalized["language"] = row.get("language") or ""
    normalized["code_changed_files"] = row.get("code_changed_files") or []
    normalized["code_diff_excerpt"] = row.get("code_diff_excerpt") or ""
    normalized["docs_before_excerpt"] = row.get("docs_before_excerpt") or ""
    normalized["docs_before_retrieved_files"] = row.get("docs_before_retrieved_files") or []

    for index in range(1, 13):
        normalized[f"doc_context_{index:02d}_path"] = row.get(f"doc_context_{index:02d}_path") or ""
        normalized[f"doc_context_{index:02d}_excerpt"] = row.get(f"doc_context_{index:02d}_excerpt") or ""

    if label_kind == "gold":
        required = parse_bool(row.get("gold_docs_update_required"))
        category = row.get("gold_doc_category")
        notes = row.get("manual_label_notes") or (
            "Migrated from the reviewed historical 300 gold subset."
        )
    else:
        required = parse_bool(row.get("human_docs_update_required"))
        category = row.get("human_doc_category")
        notes = row.get("human_label_notes") or row.get("manual_label_notes") or ""

    normalized["human_docs_update_required"] = required
    normalized["human_doc_category"] = category
    normalized["human_label_notes"] = notes
    normalized["review_status"] = "approved"
    normalized["review_row_hash"] = review_row_hash(normalized)
    normalized["review_context_hash"] = review_context_hash(normalized)
    return normalized


def csv_value(value: Any) -> str | int | bool:
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    if value is None:
        return ""
    return value


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    merged: list[dict[str, Any]] = []
    provenance: list[dict[str, Any]] = []
    duplicates: list[dict[str, Any]] = []
    index: dict[tuple[str, int], int] = {}
    source_stats: dict[str, dict[str, int]] = {}

    for source_name, source_path, label_kind in SOURCES:
        rows = load_jsonl(source_path)
        added = skipped = conflicts = 0
        for raw in rows:
            key = pr_key(raw)
            incoming = normalize(raw, label_kind)
            if key in index:
                existing = merged[index[key]]
                conflict = (
                    existing["human_docs_update_required"] != incoming["human_docs_update_required"]
                    or existing["human_doc_category"] != incoming["human_doc_category"]
                )
                duplicates.append(
                    {
                        "repository": key[0],
                        "pr_number": key[1],
                        "kept_source": provenance[index[key]]["source_dataset"],
                        "skipped_source": source_name,
                        "label_conflict": conflict,
                        "kept_label": [existing["human_docs_update_required"], existing["human_doc_category"]],
                        "skipped_label": [incoming["human_docs_update_required"], incoming["human_doc_category"]],
                    }
                )
                skipped += 1
                conflicts += int(conflict)
                continue
            index[key] = len(merged)
            merged.append(incoming)
            provenance.append(
                {
                    "repository": key[0],
                    "pr_number": key[1],
                    "case_id": incoming["case_id"],
                    "source_dataset": source_name,
                    "source_path": str(source_path.relative_to(ROOT)).replace("\\", "/"),
                    "label_protocol": "current_docs_before_review" if source_name != "historical_4k_unique" and source_name != "historical_300_gold_unique" else "historical_human_or_gold_review",
                }
            )
            added += 1
        source_stats[source_name] = {
            "input_rows": len(rows),
            "added_rows": added,
            "duplicate_rows_skipped": skipped,
            "duplicate_label_conflicts": conflicts,
        }

    errors: list[dict[str, Any]] = []
    case_ids: set[str] = set()
    for number, row in enumerate(merged, 1):
        required = row["human_docs_update_required"]
        category = row["human_doc_category"]
        if not isinstance(required, bool):
            errors.append({"row": number, "reason": "non_boolean_label"})
        if required is False and category != "no_update":
            errors.append({"row": number, "reason": "negative_category_mismatch"})
        if required is True and category not in POSITIVE_CATEGORIES:
            errors.append({"row": number, "reason": "positive_category_mismatch"})
        if row["review_status"] != "approved":
            errors.append({"row": number, "reason": "status_not_approved"})
        if row["review_row_hash"] != review_row_hash(row):
            errors.append({"row": number, "reason": "review_row_hash_mismatch"})
        if row["review_context_hash"] != review_context_hash(row):
            errors.append({"row": number, "reason": "review_context_hash_mismatch"})
        case_id = str(row["case_id"])
        if case_id in case_ids:
            errors.append({"row": number, "reason": "duplicate_case_id", "case_id": case_id})
        case_ids.add(case_id)

    label_counts = Counter("positive" if row["human_docs_update_required"] else "negative" for row in merged)
    category_counts = Counter(row["human_doc_category"] for row in merged)
    source_counts = Counter(item["source_dataset"] for item in provenance)

    write_jsonl(OUTPUT / "consolidated_human_review.jsonl", merged)
    positives = [row for row in merged if row["human_docs_update_required"] is True]
    write_jsonl(OUTPUT / "positive_training_pool.jsonl", positives)
    write_jsonl(OUTPUT / "source_provenance.jsonl", provenance)
    write_jsonl(OUTPUT / "duplicates_skipped.jsonl", duplicates)
    write_jsonl(OUTPUT / "validation_errors.jsonl", errors)

    csv_path = OUTPUT / "consolidated_human_review.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REVIEWER_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in merged:
            writer.writerow({field: csv_value(row.get(field)) for field in REVIEWER_FIELDS})

    with (OUTPUT / "positive_training_pool.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REVIEWER_FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in positives:
            writer.writerow({field: csv_value(row.get(field)) for field in REVIEWER_FIELDS})

    manifest = {
        "version": "consolidated_enriched_training_v1",
        "purpose": "training_enriched_corpus",
        "canonical_identity": "normalized repository + pr_number",
        "deduplication_priority": [item[0] for item in SOURCES],
        "row_count": len(merged),
        "unique_pr_count": len(index),
        "positive_count": label_counts["positive"],
        "negative_count": label_counts["negative"],
        "positive_rate": label_counts["positive"] / len(merged),
        "category_counts": dict(sorted(category_counts.items())),
        "source_counts": dict(sorted(source_counts.items())),
        "source_stats": source_stats,
        "duplicates_skipped": len(duplicates),
        "duplicate_label_conflicts": sum(int(row["label_conflict"]) for row in duplicates),
        "validation_error_count": len(errors),
        "sha256": {},
    }
    for name in [
        "consolidated_human_review.jsonl",
        "consolidated_human_review.csv",
        "positive_training_pool.jsonl",
        "positive_training_pool.csv",
        "source_provenance.jsonl",
    ]:
        manifest["sha256"][name] = hashlib.sha256((OUTPUT / name).read_bytes()).hexdigest()

    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    report = [
        "# Consolidated enriched training corpus v1",
        "",
        f"- Validation: **{'PASS' if not errors else 'FAIL'}**",
        f"- Rows / unique PRs: **{len(merged):,}**",
        f"- Positive: **{label_counts['positive']:,} ({label_counts['positive'] / len(merged):.2%})**",
        f"- Negative: **{label_counts['negative']:,}**",
        f"- Duplicates skipped: **{len(duplicates):,}**",
        f"- Duplicate label conflicts audited: **{manifest['duplicate_label_conflicts']:,}**",
        "",
        "## Categories",
        "",
    ]
    report.extend(f"- {name}: **{count:,}**" for name, count in sorted(category_counts.items()))
    report.extend(["", "## Sources", ""])
    report.extend(f"- {name}: **{count:,}**" for name, count in sorted(source_counts.items()))
    report.extend(
        [
            "",
            "Historical rows are retained for training enrichment and marked in source_provenance.jsonl.",
            "For duplicate PRs, the current 17,880 review wins over every historical label.",
        ]
    )
    (OUTPUT / "audit_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
