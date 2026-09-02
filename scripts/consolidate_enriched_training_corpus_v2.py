from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.human_review_workflow_v2 import (
    POSITIVE_CATEGORIES,
    parse_bool,
    review_context_hash,
    review_row_hash,
)
from docguard_ml_v2.data_contract import (
    ADDITIONAL_REVIEWED_NATURAL_POSITIVE_LABEL_SOURCE,
    CONTROLLED_DESIGN_LABEL_SOURCE,
    NATURAL_HUMAN_GOLD_LABEL_SOURCE,
)


OUTPUT = ROOT / "data/final_v2/human_review/consolidated_enriched_training_v2"
SOURCES = [
    {
        "name": "consolidated_enriched_training_v1",
        "path": ROOT / "data/final_v2/human_review/consolidated_enriched_training_v1/consolidated_human_review.jsonl",
        "expected_rows": 21_080,
        "selection": "all_approved",
        "provenance_tier": "natural_historical_and_targeted_reviewed",
    },
    {
        "name": "remaining_4800_partial_positive_54",
        "path": ROOT / "data/final_v2/expansion/targeted_positive_enrichment_v1_remaining_4800/raw_candidates_transfer_2323/reviewed_from_scratch_v1/positive_reviewed.jsonl",
        "expected_rows": 54,
        "selection": "positive_only",
        "provenance_tier": "natural_targeted_reviewed",
    },
    {
        "name": "controlled_real_project_positive_v1",
        "path": ROOT / "data/final_v2/controlled_real_project_positive_v1/human_review/reviewed_2000.jsonl",
        "expected_rows": 2_000,
        "selection": "positive_only_owner_accepted",
        "provenance_tier": "controlled_real_project_augmentation",
    },
    {
        "name": "controlled_real_project_positive_v2_imbalanced",
        "path": ROOT / "data/final_v2/controlled_real_project_positive_v2_imbalanced/human_review/reviewed_2000.jsonl",
        "expected_rows": 2_000,
        "selection": "positive_only_owner_accepted",
        "provenance_tier": "controlled_real_project_augmentation",
    },
    {
        "name": "natural_diversity_expansion_v1",
        "path": ROOT / "data/final_v2/natural_diversity_expansion_v1/human_review/finalized/natural_human_gold.jsonl",
        "expected_rows": 779,
        "selection": "all_approved",
        "provenance_tier": "natural_diversity_expansion_v1_reviewed",
    },
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig") as handle:
        return [json.loads(line) for line in handle if line.strip()]


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


def pr_key(row: dict[str, Any]) -> tuple[str, int]:
    repository = str(row.get("repository") or "").strip().lower().removesuffix(".git")
    return repository, int(row["pr_number"])


def normalize_label(row: dict[str, Any]) -> tuple[bool, str]:
    required = parse_bool(row.get("human_docs_update_required"))
    if not isinstance(required, bool):
        raise ValueError(f"{row.get('case_id')}: human_docs_update_required is not boolean")
    category = str(row.get("human_doc_category") or "").strip()
    if required and category not in POSITIVE_CATEGORIES:
        raise ValueError(f"{row.get('case_id')}: invalid positive category {category!r}")
    if not required and category != "no_update":
        raise ValueError(f"{row.get('case_id')}: negative row must use no_update")
    return required, category


def provenance_for_source(source_name: str, provenance_tier: str) -> dict[str, Any]:
    """Assign explicit supervision provenance without changing label values."""
    if provenance_tier == "controlled_real_project_augmentation":
        return {
            "label_source": CONTROLLED_DESIGN_LABEL_SOURCE,
            "supervision_source": "controlled_synthetic_positive",
            "independent_human_reviewed": False,
            "controlled_design_supervision": True,
            "owner_accepted_for_training": True,
            "train_only": True,
        }
    if source_name == "remaining_4800_partial_positive_54":
        return {
            "label_source": ADDITIONAL_REVIEWED_NATURAL_POSITIVE_LABEL_SOURCE,
            "supervision_source": "additional_natural_human_review",
            "independent_human_reviewed": True,
            "controlled_design_supervision": False,
            "owner_accepted_for_training": False,
            "train_only": False,
        }
    return {
        "label_source": NATURAL_HUMAN_GOLD_LABEL_SOURCE,
        "supervision_source": "natural_human_gold",
        "independent_human_reviewed": True,
        "controlled_design_supervision": False,
        "owner_accepted_for_training": False,
        "train_only": False,
    }


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    merged: list[dict[str, Any]] = []
    provenance: list[dict[str, Any]] = []
    duplicates: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    index_by_pr: dict[tuple[str, int], int] = {}
    case_ids: set[str] = set()
    source_stats: dict[str, dict[str, int | str]] = {}

    for source in SOURCES:
        path = Path(source["path"])
        if not path.exists():
            raise FileNotFoundError(path)
        rows = load_jsonl(path)
        if len(rows) != source["expected_rows"]:
            raise ValueError(f"{source['name']}: expected {source['expected_rows']} rows, found {len(rows)}")
        added = skipped = 0
        for raw in rows:
            required, category = normalize_label(raw)
            if source["selection"].startswith("positive_only") and not required:
                raise ValueError(f"{source['name']}: non-positive row entered positive-only source: {raw.get('case_id')}")
            if raw.get("review_status") != "approved":
                raise ValueError(f"{source['name']}: row is not approved: {raw.get('case_id')}")
            copied = dict(raw)
            copied["human_docs_update_required"] = required
            copied["human_doc_category"] = category
            copied["consolidated_source_dataset"] = source["name"]
            copied["provenance_tier"] = source["provenance_tier"]
            copied.update(provenance_for_source(source["name"], source["provenance_tier"]))
            if source["provenance_tier"] == "controlled_real_project_augmentation":
                copied["training_eligible"] = True
                copied["merge_status"] = "owner_accepted_for_augmentation"
            copied["review_row_hash"] = review_row_hash(copied)
            copied["review_context_hash"] = review_context_hash(copied)

            key = pr_key(copied)
            case_id = str(copied.get("case_id") or "").strip()
            if not case_id:
                errors.append({"source": source["name"], "reason": "missing_case_id", "repository_pr": key})
                continue
            if key in index_by_pr or case_id in case_ids:
                existing_index = index_by_pr.get(key)
                duplicates.append({
                    "source": source["name"],
                    "case_id": case_id,
                    "repository": key[0],
                    "pr_number": key[1],
                    "duplicate_kind": "repository_pr" if existing_index is not None else "case_id",
                    "kept_source": provenance[existing_index]["source_dataset"] if existing_index is not None else "earlier_source",
                })
                skipped += 1
                continue
            index_by_pr[key] = len(merged)
            case_ids.add(case_id)
            merged.append(copied)
            provenance.append({
                "case_id": case_id,
                "repository": key[0],
                "pr_number": key[1],
                "source_dataset": source["name"],
                "source_path": path.relative_to(ROOT).as_posix(),
                "selection": source["selection"],
                "provenance_tier": source["provenance_tier"],
                **provenance_for_source(source["name"], source["provenance_tier"]),
            })
            added += 1
        source_stats[source["name"]] = {
            "input_rows": len(rows),
            "added_rows": added,
            "duplicates_skipped": skipped,
            "sha256": sha256_file(path),
        }

    for number, row in enumerate(merged, start=1):
        required, category = normalize_label(row)
        if row.get("review_row_hash") != review_row_hash(row):
            errors.append({"row": number, "case_id": row.get("case_id"), "reason": "review_row_hash_mismatch"})
        if row.get("review_context_hash") != review_context_hash(row):
            errors.append({"row": number, "case_id": row.get("case_id"), "reason": "review_context_hash_mismatch"})
        if required != (category != "no_update"):
            errors.append({"row": number, "case_id": row.get("case_id"), "reason": "binary_category_mismatch"})

    label_counts = Counter("positive" if row["human_docs_update_required"] else "negative" for row in merged)
    category_counts = Counter(row["human_doc_category"] for row in merged)
    source_counts = Counter(item["source_dataset"] for item in provenance)
    controlled_count = sum(item["provenance_tier"] == "controlled_real_project_augmentation" for item in provenance)
    natural_or_historical_count = len(merged) - controlled_count

    expected_categories = Counter({
        "no_update": 19_965,
        "api_reference": 1_554,
        "configuration": 1_467,
        "developer_setup": 992,
        "model_contract": 1_122,
        "other_documentation": 813,
    })
    if len(merged) != 25_913:
        errors.append({"reason": "unexpected_total", "expected": 25_913, "actual": len(merged)})
    if category_counts != expected_categories:
        errors.append({"reason": "unexpected_category_counts", "expected": dict(expected_categories), "actual": dict(category_counts)})

    write_jsonl(OUTPUT / "consolidated_human_review.jsonl", merged)
    write_jsonl(OUTPUT / "positive_training_pool.jsonl", [row for row in merged if row["human_docs_update_required"]])
    write_jsonl(OUTPUT / "source_provenance.jsonl", provenance)
    write_jsonl(OUTPUT / "duplicates_skipped.jsonl", duplicates)
    write_jsonl(OUTPUT / "validation_errors.jsonl", errors)

    manifest = {
        "version": "consolidated_enriched_training_v2",
        "validation": "PASS" if not errors else "FAIL",
        "row_count": len(merged),
        "unique_case_ids": len(case_ids),
        "unique_repository_pr_keys": len(index_by_pr),
        "positive_count": label_counts["positive"],
        "negative_count": label_counts["negative"],
        "positive_rate": label_counts["positive"] / len(merged),
        "category_counts": dict(sorted(category_counts.items())),
        "source_counts": dict(sorted(source_counts.items())),
        "label_source_counts": dict(sorted(Counter(row["label_source"] for row in merged).items())),
        "supervision_source_counts": dict(sorted(Counter(row["supervision_source"] for row in merged).items())),
        "independent_human_reviewed_counts": dict(sorted(Counter(str(row["independent_human_reviewed"]) for row in merged).items())),
        "controlled_design_supervision_counts": dict(sorted(Counter(str(row["controlled_design_supervision"]) for row in merged).items())),
        "owner_accepted_for_training_counts": dict(sorted(Counter(str(row["owner_accepted_for_training"]) for row in merged).items())),
        "train_only_counts": dict(sorted(Counter(str(row["train_only"]) for row in merged).items())),
        "source_stats": source_stats,
        "controlled_augmentation_rows": controlled_count,
        "natural_or_historical_rows": natural_or_historical_count,
        "natural_diversity_included_rows": source_counts["natural_diversity_expansion_v1"],
        "natural_diversity_expected_rows": 779,
        "natural_diversity_missing_rows": 779 - source_counts["natural_diversity_expansion_v1"],
        "duplicates_skipped": len(duplicates),
        "validation_error_count": len(errors),
        "sha256": {},
    }
    for filename in ["consolidated_human_review.jsonl", "positive_training_pool.jsonl", "source_provenance.jsonl"]:
        manifest["sha256"][filename] = sha256_file(OUTPUT / filename)
    (OUTPUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    report = [
        "# Consolidated enriched training corpus v2",
        "",
        f"- Validation: **{manifest['validation']}**",
        f"- Rows: **{len(merged):,}**",
        f"- Positive: **{label_counts['positive']:,} ({manifest['positive_rate']:.2%})**",
        f"- Negative: **{label_counts['negative']:,}**",
        f"- Controlled augmentation rows: **{controlled_count:,}**",
        f"- Natural/historical reviewed rows: **{natural_or_historical_count:,}**",
        f"- Natural Diversity Expansion V1 included rows: **{source_counts['natural_diversity_expansion_v1']:,} / 779**",
        f"- Duplicates skipped: **{len(duplicates):,}**",
        "",
        "## Categories",
        "",
    ]
    report.extend(f"- `{name}`: **{count:,}**" for name, count in sorted(category_counts.items()))
    report.extend(["", "## Sources", ""])
    report.extend(f"- `{name}`: **{count:,}**" for name, count in sorted(source_counts.items()))
    report.extend([
        "",
        "## Provenance",
        "",
    ])
    report.extend(f"- `{name}`: **{count:,}**" for name, count in sorted(manifest["label_source_counts"].items()))
    report.extend([
        "",
        "Controlled rows use `label_source=controlled_design_label`, `supervision_source=controlled_synthetic_positive`, `independent_human_reviewed=false`, and `train_only=true`. Natural human gold and the 54 additional natural positives use separate provenance values. Controlled rows must remain development-train-only so repository/template leakage cannot inflate validation or sealed-confirmation metrics.",
    ])
    (OUTPUT / "audit_report.md").write_text("\n".join(report) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
