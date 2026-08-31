"""Validate and finalize Natural Diversity Expansion V1 human review.

The JSONL review batches are authoritative.  CSV copies are checked for the
same case order and human decisions.  Every non-human field is compared with
the frozen prefilled review row before any gold artifact is produced.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


HUMAN_FIELDS = {
    "human_docs_update_required",
    "human_doc_category",
    "human_label_notes",
    "review_status",
}
POSITIVE_CATEGORIES = {
    "api_reference",
    "configuration",
    "developer_setup",
    "model_contract",
    "other_documentation",
}
ALLOWED_CATEGORIES = POSITIVE_CATEGORIES | {"no_update"}
LABEL_SOURCE = "natural_human_gold"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_number}: row is not an object")
            rows.append(value)
    return rows


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    text = str(value or "").strip().lower()
    if text in {"true", "1", "yes", "y"}:
        return True
    if text in {"false", "0", "no", "n"}:
        return False
    return None


def decision(row: dict[str, Any]) -> tuple[bool | None, str, str, str]:
    return (
        parse_bool(row.get("human_docs_update_required")),
        str(row.get("human_doc_category") or "").strip(),
        str(row.get("human_label_notes") or "").strip(),
        str(row.get("review_status") or "").strip().lower(),
    )


def immutable_projection(row: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in row.items() if key not in HUMAN_FIELDS}


def validate_decision(row: dict[str, Any]) -> list[str]:
    case_id = str(row.get("case_id") or "<missing-case-id>")
    docs_required, category, notes, status = decision(row)
    errors: list[str] = []
    if status == "approved":
        if docs_required is None:
            errors.append(f"{case_id}: approved row has no binary decision")
        elif docs_required and category not in POSITIVE_CATEGORIES:
            errors.append(f"{case_id}: positive row has invalid category {category!r}")
        elif not docs_required and category != "no_update":
            errors.append(f"{case_id}: negative row must use no_update")
        if category not in ALLOWED_CATEGORIES:
            errors.append(f"{case_id}: unsupported category {category!r}")
    elif status == "excluded":
        if not notes:
            errors.append(f"{case_id}: excluded row requires a reason in notes")
    else:
        errors.append(f"{case_id}: review_status must be approved or excluded, got {status!r}")
    if row.get("label_source") not in {None, ""}:
        errors.append(f"{case_id}: label_source was populated before finalization")
    return errors


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    approved = [row for row in rows if row["review_status"] == "approved"]
    positives = [row for row in approved if row["gold_docs_update_required"] is True]
    by_split_category: dict[str, Counter[str]] = defaultdict(Counter)
    by_language_category: dict[str, Counter[str]] = defaultdict(Counter)
    for row in approved:
        by_split_category[str(row.get("partition") or "")][str(row["gold_doc_category"])] += 1
        by_language_category[str(row.get("language") or "")][str(row["gold_doc_category"])] += 1
    return {
        "reviewed_rows": len(rows),
        "approved_rows": len(approved),
        "excluded_rows": len(rows) - len(approved),
        "positive_rows": len(positives),
        "negative_rows": len(approved) - len(positives),
        "positive_rate_approved": len(positives) / len(approved) if approved else 0.0,
        "category_counts": dict(sorted(Counter(str(row["gold_doc_category"]) for row in approved).items())),
        "positive_category_counts": dict(sorted(Counter(str(row["gold_doc_category"]) for row in positives).items())),
        "partition_counts": dict(sorted(Counter(str(row.get("partition") or "") for row in approved).items())),
        "language_counts": dict(sorted(Counter(str(row.get("language") or "") for row in approved).items())),
        "positive_language_counts": dict(sorted(Counter(str(row.get("language") or "") for row in positives).items())),
        "positive_repository_count": len({str(row.get("repository") or "") for row in positives}),
        "category_by_partition": {key: dict(sorted(value.items())) for key, value in sorted(by_split_category.items())},
        "category_by_language": {key: dict(sorted(value.items())) for key, value in sorted(by_language_category.items())},
        "surface_stratum_counts": dict(sorted(Counter(str(row.get("candidate_surface_stratum") or "") for row in approved).items())),
    }


def run(*, prefilled_path: Path, batches_dir: Path, output_dir: Path) -> dict[str, Any]:
    prefilled = read_jsonl(prefilled_path)
    expected_ids = [str(row.get("case_id") or "") for row in prefilled]
    if not all(expected_ids) or len(expected_ids) != len(set(expected_ids)):
        raise ValueError("Frozen prefilled review contains missing or duplicate case IDs")
    expected_by_id = {str(row["case_id"]): row for row in prefilled}

    json_paths = sorted(batches_dir.glob("batch_*.jsonl"))
    csv_paths = sorted(batches_dir.glob("batch_*.csv"))
    if not json_paths or len(json_paths) != len(csv_paths):
        raise ValueError("Expected matching JSONL and CSV review batches")

    reviewed: list[dict[str, Any]] = []
    errors: list[str] = []
    batch_audit: list[dict[str, Any]] = []
    for json_path, csv_path in zip(json_paths, csv_paths):
        if json_path.stem != csv_path.stem:
            errors.append(f"batch filename mismatch: {json_path.name} vs {csv_path.name}")
            continue
        json_rows = read_jsonl(json_path)
        csv_rows = read_csv(csv_path)
        if len(json_rows) != len(csv_rows):
            errors.append(f"{json_path.stem}: JSONL/CSV row count mismatch")
        for index, (json_row, csv_row) in enumerate(zip(json_rows, csv_rows), 1):
            case_id = str(json_row.get("case_id") or "")
            if case_id != str(csv_row.get("case_id") or ""):
                errors.append(f"{json_path.stem}:{index}: JSONL/CSV case order mismatch")
                continue
            if decision(json_row) != decision(csv_row):
                errors.append(f"{case_id}: JSONL/CSV human decision mismatch")
            frozen = expected_by_id.get(case_id)
            if frozen is None:
                errors.append(f"{case_id}: case not present in frozen prefilled review")
                continue
            if immutable_projection(json_row) != immutable_projection(frozen):
                errors.append(f"{case_id}: immutable evidence or metadata changed")
            errors.extend(validate_decision(json_row))
            reviewed.append(json_row)
        batch_audit.append({
            "batch": json_path.stem,
            "rows": len(json_rows),
            "jsonl_sha256": sha256_file(json_path),
            "csv_sha256": sha256_file(csv_path),
        })

    reviewed_ids = [str(row.get("case_id") or "") for row in reviewed]
    if reviewed_ids != expected_ids:
        missing = sorted(set(expected_ids) - set(reviewed_ids))
        unexpected = sorted(set(reviewed_ids) - set(expected_ids))
        errors.append(
            f"reviewed order/membership differs from frozen input; missing={len(missing)}, "
            f"unexpected={len(unexpected)}"
        )
    if len(reviewed_ids) != len(set(reviewed_ids)):
        errors.append("duplicate case IDs found across reviewed batches")

    audit = {
        "schema": "natural_diversity_expansion_v1_review_completion_audit",
        "status": "passed" if not errors else "failed",
        "prefilled_sha256": sha256_file(prefilled_path),
        "expected_rows": len(prefilled),
        "reviewed_rows": len(reviewed),
        "json_csv_decisions_cross_checked": True,
        "immutable_fields_cross_checked_against_prefilled": True,
        "batch_audit": batch_audit,
        "errors": errors,
    }
    write_json(output_dir / "review_completion_audit.json", audit)
    if errors:
        raise ValueError("Review completion audit failed: " + "; ".join(errors[:20]))

    finalized: list[dict[str, Any]] = []
    for row in reviewed:
        docs_required, category, _notes, status = decision(row)
        out = dict(row)
        out["human_docs_update_required"] = docs_required
        out["human_doc_category"] = category or None
        out["review_status"] = status
        out["label_source"] = LABEL_SOURCE
        out["supervision_source"] = LABEL_SOURCE
        out["provenance_tier"] = "natural_diversity_expansion_v1_reviewed"
        out["independent_human_reviewed"] = status == "approved"
        out["owner_accepted_for_training"] = status == "approved" and out.get("partition") == "development_train"
        out["train_only"] = out.get("partition") == "development_train"
        out["augmentation_train_only"] = False
        out["controlled_design_supervision"] = False
        out["human_review_complete"] = status == "approved"
        out["gold_docs_update_required"] = docs_required if status == "approved" else None
        out["gold_doc_category"] = category if status == "approved" else None
        out["stage2_primary_eligible"] = bool(
            status == "approved" and docs_required and category in POSITIVE_CATEGORIES - {"other_documentation"}
        )
        finalized.append(out)

    approved = [row for row in finalized if row["review_status"] == "approved"]
    train = [row for row in approved if row.get("partition") == "development_train"]
    refresh = [row for row in approved if row.get("partition") == "refresh_validation"]
    excluded = [row for row in finalized if row["review_status"] == "excluded"]
    write_jsonl(output_dir / "reviewed_all.jsonl", finalized)
    write_jsonl(output_dir / "natural_human_gold.jsonl", approved)
    write_jsonl(output_dir / "natural_expansion_train_gold.jsonl", train)
    write_jsonl(output_dir / "natural_refresh_validation_gold.jsonl", refresh)
    write_jsonl(output_dir / "excluded_reviewed.jsonl", excluded)

    summary = summarize(finalized)
    summary.update({
        "schema": "natural_diversity_expansion_v1_human_gold_manifest",
        "label_source": LABEL_SOURCE,
        "no_class_balancing_performed": True,
        "refresh_validation_excluded_from_training": True,
        "confirmation_accessed": False,
        "artifacts": {
            name: {"path": str(output_dir / name), "sha256": sha256_file(output_dir / name)}
            for name in (
                "reviewed_all.jsonl",
                "natural_human_gold.jsonl",
                "natural_expansion_train_gold.jsonl",
                "natural_refresh_validation_gold.jsonl",
                "excluded_reviewed.jsonl",
            )
        },
    })
    write_json(output_dir / "human_gold_manifest.json", summary)
    lines = [
        "# Natural Diversity Expansion V1 — completed human review",
        "",
        f"- Completion audit: **{audit['status']}**",
        f"- Reviewed rows: **{summary['reviewed_rows']}**",
        f"- Approved / excluded: **{summary['approved_rows']} / {summary['excluded_rows']}**",
        f"- Positive / negative: **{summary['positive_rows']} / {summary['negative_rows']}**",
        f"- Positive rate among approved: **{summary['positive_rate_approved']:.2%}**",
        f"- Positive categories: `{summary['positive_category_counts']}`",
        f"- Positive languages: `{summary['positive_language_counts']}`",
        f"- Positive repositories: **{summary['positive_repository_count']}**",
        f"- Partition rows: `{summary['partition_counts']}`",
        "",
        "No class balancing was performed. Refresh validation remains excluded from training.",
    ]
    (output_dir / "HUMAN_REVIEW_FINAL_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prefilled", required=True)
    parser.add_argument("--batches-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    summary = run(
        prefilled_path=Path(args.prefilled),
        batches_dir=Path(args.batches_dir),
        output_dir=Path(args.output_dir),
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
