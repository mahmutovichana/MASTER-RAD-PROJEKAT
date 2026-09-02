from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from docguard_ml_v2.data_contract import (
    CONTROLLED_DESIGN_LABEL_SOURCE,
    LABEL_SOURCE,
    PRIMARY_STAGE2_LABELS,
    validate_final_gold_row,
)
from scripts.build_repository_partitions_v2 import assign_partitions


ROOT = PROJECT_ROOT
MERGED = ROOT / "data/final_v2/human_review/consolidated_enriched_training_v2/consolidated_human_review.jsonl"
BASE_GOLD = ROOT / "experiments/consolidated_enriched_training_v1/gold/final_human_gold.jsonl"
OUT = ROOT / "experiments/consolidated_enriched_training_v2/gold"
PARTITIONS = ["development_train", "development_validation", "confirmation"]
TRAIN_ONLY_AUGMENTATION_SOURCES = {
    "remaining_4800_partial_positive_54",
    "controlled_real_project_positive_v1",
    "controlled_real_project_positive_v2_imbalanced",
}
NATURAL_DIVERSITY_SOURCE = "natural_diversity_expansion_v1"
EXPECTED_MERGED_ROWS = 25_913
EXPECTED_BASE_ROWS = 21_080
EXPECTED_TRAIN_ONLY_AUGMENTATION_ROWS = 4_054


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


def repo_id(row: dict[str, Any]) -> str:
    return str(row.get("repository") or "").strip().lower().removesuffix(".git")


def safe_input_key(row: dict[str, Any]) -> tuple[str, str, str, str]:
    return (
        str(row.get("language") or ""),
        json.dumps(row.get("code_changed_files"), ensure_ascii=False, sort_keys=True),
        str(row.get("code_diff_excerpt") or ""),
        str(row.get("docs_before_excerpt") or ""),
    )


def finalize(row: dict[str, Any], partition: str, augmentation: bool) -> dict[str, Any]:
    copied = dict(row)
    required = copied.get("human_docs_update_required")
    if not isinstance(required, bool):
        raise ValueError(f"{copied.get('case_id')}: human_docs_update_required is not boolean")
    category = str(copied.get("human_doc_category") or "")
    copied["gold_docs_update_required"] = required
    copied["gold_doc_category"] = category
    label_source = str(copied.get("label_source") or LABEL_SOURCE)
    copied["label_source"] = label_source
    if label_source == CONTROLLED_DESIGN_LABEL_SOURCE:
        if partition != "development_train":
            raise ValueError(f"{copied.get('case_id')}: controlled design supervision cannot enter {partition}")
        if copied.get("independent_human_reviewed") is not False or copied.get("controlled_design_supervision") is not True:
            raise ValueError(f"{copied.get('case_id')}: invalid controlled provenance flags")
    elif "independent_human_reviewed" in copied and copied.get("independent_human_reviewed") is not True:
        raise ValueError(f"{copied.get('case_id')}: natural row lacks independent human provenance")
    copied["human_review_complete"] = True
    copied["partition"] = partition
    copied["stage2_primary_eligible"] = required and category in PRIMARY_STAGE2_LABELS
    copied["stage2_coverage_bucket"] = category if required else "no_update"
    copied["augmentation_train_only"] = augmentation
    validate_final_gold_row(copied, allowed_partitions={partition})
    return copied


def main() -> int:
    merged = load_jsonl(MERGED)
    base_gold = load_jsonl(BASE_GOLD)
    if len(merged) != EXPECTED_MERGED_ROWS or len(base_gold) != EXPECTED_BASE_ROWS:
        raise ValueError(f"Unexpected input sizes: merged={len(merged)}, base_gold={len(base_gold)}")

    base_partition_by_case = {str(row["case_id"]): str(row["partition"]) for row in base_gold}
    if len(base_partition_by_case) != len(base_gold):
        raise ValueError("Base gold contains duplicate case IDs")
    base_repos_by_partition = {
        partition: {repo_id(row) for row in base_gold if row["partition"] == partition}
        for partition in PARTITIONS
    }

    existing_repos = {repo_id(row) for row in base_gold}
    source_counts = Counter(str(row.get("consolidated_source_dataset") or "") for row in merged)
    if source_counts[NATURAL_DIVERSITY_SOURCE] != 779:
        raise ValueError(f"Natural Diversity source count mismatch: {source_counts[NATURAL_DIVERSITY_SOURCE]}")
    natural_diversity_rows = [row for row in merged if str(row.get("consolidated_source_dataset") or "") == NATURAL_DIVERSITY_SOURCE]
    natural_diversity_assignments = assign_partitions(
        natural_diversity_rows,
        seed=42,
        confirmation_fraction=0.2,
        previously_seen=existing_repos,
    )

    output_rows: list[dict[str, Any]] = []
    new_repositories: set[str] = set()
    natural_diversity_repositories: set[str] = set()
    for row in merged:
        case_id = str(row["case_id"])
        if case_id in base_partition_by_case:
            output_rows.append(finalize(row, base_partition_by_case[case_id], augmentation=False))
            continue

        repository = repo_id(row)
        source_dataset = str(row.get("consolidated_source_dataset") or "")
        if source_dataset in TRAIN_ONLY_AUGMENTATION_SOURCES:
            if repository in base_repos_by_partition["development_validation"]:
                raise ValueError(f"Augmentation repository overlaps frozen validation: {repository}")
            if repository in base_repos_by_partition["confirmation"]:
                raise ValueError(f"Augmentation repository overlaps sealed confirmation: {repository}")
            new_repositories.add(repository)
            output_rows.append(finalize(row, "development_train", augmentation=True))
        elif source_dataset == NATURAL_DIVERSITY_SOURCE:
            natural_diversity_repositories.add(repository)
            output_rows.append(finalize(row, natural_diversity_assignments[repository], augmentation=False))
        else:
            raise ValueError(f"{case_id}: unsupported new source dataset {source_dataset!r}")

    safe_groups: dict[tuple[str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in output_rows:
        safe_groups[safe_input_key(row)].append(row)
    model_visible_collision_groups: list[dict[str, Any]] = []
    for group_index, group in enumerate([items for items in safe_groups.values() if len(items) > 1], start=1):
        group_id = f"model_visible_collision_{group_index:04d}"
        labels = sorted({f"{row.get('gold_docs_update_required')}::{row.get('gold_doc_category')}" for row in group})
        partitions = sorted({str(row.get("partition") or "") for row in group})
        cross_development_confirmation = "confirmation" in partitions and any(partition != "confirmation" for partition in partitions)
        for row in group:
            row["model_visible_collision"] = True
            row["model_visible_collision_group_id"] = group_id
            row["model_visible_collision_conflicting_labels"] = len(labels) > 1
            row["model_visible_collision_cross_development_confirmation"] = cross_development_confirmation
        model_visible_collision_groups.append(
            {
                "group_id": group_id,
                "rows": len(group),
                "case_ids": [str(row.get("case_id")) for row in group],
                "repository_pr_keys": [f"{repo_id(row)}#{row.get('pr_number')}" for row in group],
                "partitions": partitions,
                "labels": labels,
                "conflicting_labels": len(labels) > 1,
                "cross_development_confirmation": cross_development_confirmation,
            }
        )

    rows_by_partition = {
        partition: [row for row in output_rows if row["partition"] == partition]
        for partition in PARTITIONS
    }
    repos_by_partition = {
        partition: {repo_id(row) for row in rows}
        for partition, rows in rows_by_partition.items()
    }
    repo_overlap = set()
    for index, left in enumerate(PARTITIONS):
        for right in PARTITIONS[index + 1:]:
            repo_overlap |= repos_by_partition[left] & repos_by_partition[right]
    if repo_overlap:
        raise ValueError(f"Repository leakage across partitions: {sorted(repo_overlap)}")

    if len(output_rows) != EXPECTED_MERGED_ROWS:
        raise ValueError("Final gold row count mismatch")
    if sum(row["augmentation_train_only"] for row in output_rows) != EXPECTED_TRAIN_ONLY_AUGMENTATION_ROWS:
        raise ValueError("Expected exactly 4,054 train-only augmentation rows")
    base_validation_ids = {str(row["case_id"]) for row in base_gold if row["partition"] == "development_validation"}
    if not base_validation_ids:
        raise ValueError("Base validation split is empty")
    base_confirmation_ids = {str(row["case_id"]) for row in base_gold if row["partition"] == "confirmation"}
    if not base_confirmation_ids:
        raise ValueError("Base confirmation split is empty")

    OUT.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUT / "final_human_gold.jsonl", output_rows)
    filenames = {
        "development_train": "train.jsonl",
        "development_validation": "validation.jsonl",
        "confirmation": "confirmation.jsonl",
    }
    for partition, filename in filenames.items():
        write_jsonl(OUT / filename, rows_by_partition[partition])

    class_counts = {
        partition: dict(Counter(str(row["gold_docs_update_required"]) for row in rows))
        for partition, rows in rows_by_partition.items()
    }
    category_counts = {
        partition: dict(Counter(row["gold_doc_category"] for row in rows))
        for partition, rows in rows_by_partition.items()
    }
    validation_ids = {str(row["case_id"]) for row in rows_by_partition["development_validation"]}
    confirmation_ids = {str(row["case_id"]) for row in rows_by_partition["confirmation"]}
    natural_diversity_by_partition = Counter(
        str(row["partition"]) for row in output_rows if str(row.get("consolidated_source_dataset") or "") == NATURAL_DIVERSITY_SOURCE
    )
    model_visible_collision_cross_boundary = [
        group for group in model_visible_collision_groups if group["cross_development_confirmation"]
    ]
    manifest = {
        "version": "consolidated_enriched_training_v2_gold",
        "confirmation_sealed": True,
        "row_count": len(output_rows),
        "partition_row_counts": {partition: len(rows) for partition, rows in rows_by_partition.items()},
        "partition_repository_counts": {partition: len(repos) for partition, repos in repos_by_partition.items()},
        "class_counts": class_counts,
        "category_counts": category_counts,
        "augmentation_train_only_rows": EXPECTED_TRAIN_ONLY_AUGMENTATION_ROWS,
        "augmentation_repository_count": len(new_repositories),
        "natural_diversity_rows": source_counts[NATURAL_DIVERSITY_SOURCE],
        "natural_diversity_repository_count": len(natural_diversity_repositories),
        "natural_diversity_partition_row_counts": dict(sorted(natural_diversity_by_partition.items())),
        "natural_diversity_partition_assignments": dict(sorted(natural_diversity_assignments.items())),
        "natural_diversity_assignment_algorithm": "scripts.build_repository_partitions_v2.assign_partitions(seed=42, confirmation_fraction=0.2, previously_seen=base_gold_repositories)",
        "model_visible_collision_groups": len(model_visible_collision_groups),
        "model_visible_collision_rows": sum(int(row.get("model_visible_collision") is True) for row in output_rows),
        "model_visible_collision_conflicting_label_groups": sum(int(group["conflicting_labels"]) for group in model_visible_collision_groups),
        "model_visible_collision_cross_development_confirmation_groups": len(model_visible_collision_cross_boundary),
        "model_visible_collision_audit": model_visible_collision_groups,
        "repository_overlap_count": len(repo_overlap),
        "label_source_counts": dict(sorted(Counter(str(row.get("label_source")) for row in output_rows).items())),
        "consolidated_source_dataset_counts": dict(sorted(Counter(str(row.get("consolidated_source_dataset")) for row in output_rows).items())),
        "provenance_tier_counts": dict(sorted(Counter(str(row.get("provenance_tier")) for row in output_rows).items())),
        "augmentation_train_only_counts": dict(sorted(Counter(str(row.get("augmentation_train_only")) for row in output_rows).items())),
        "base_validation_case_ids_preserved": base_validation_ids <= validation_ids,
        "base_confirmation_case_ids_preserved": base_confirmation_ids <= confirmation_ids,
        "frozen_validation_case_ids_preserved": base_validation_ids <= validation_ids,
        "sealed_confirmation_case_ids_preserved": base_confirmation_ids <= confirmation_ids,
        "sha256": {},
    }
    for filename in ["final_human_gold.jsonl", "train.jsonl", "validation.jsonl", "confirmation.jsonl"]:
        manifest["sha256"][filename] = sha256_file(OUT / filename)
    if not base_validation_ids <= validation_ids:
        raise ValueError("Base frozen validation membership was not preserved")
    if not base_confirmation_ids <= confirmation_ids:
        raise ValueError("Base sealed confirmation membership was not preserved")
    if model_visible_collision_cross_boundary:
        raise ValueError(f"Model-visible collision crosses development/confirmation: {model_visible_collision_cross_boundary}")
    (OUT / "human_gold_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    report = [
        "# Consolidated enriched training v2 — leakage-safe gold split",
        "",
        f"- Total rows: **{len(output_rows):,}**",
        f"- Development train: **{len(rows_by_partition['development_train']):,}**",
        f"- Frozen development validation: **{len(rows_by_partition['development_validation']):,}**",
        f"- Sealed confirmation: **{len(rows_by_partition['confirmation']):,}**",
        "- New train-only augmentation rows: **4,054**",
        f"- New augmentation repositories: **{len(new_repositories)}**",
        f"- Natural Diversity rows: **{source_counts[NATURAL_DIVERSITY_SOURCE]:,}**",
        f"- Natural Diversity repositories: **{len(natural_diversity_repositories):,}**",
        f"- Natural Diversity split rows: **{dict(sorted(natural_diversity_by_partition.items()))}**",
        "- Repository overlap: **0**",
        "- Base validation case membership preserved: **yes**",
        "- Base confirmation case membership preserved: **yes**",
        "",
        "All controlled examples and the 54 newly reviewed natural positives remain development-train-only. The 779 Natural Diversity rows are included in Final V2 and assigned by the canonical deterministic repository-level algorithm. Existing base validation and confirmation examples remain present and repository-disjoint.",
    ]
    (OUT / "split_report.md").write_text("\n".join(report) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
