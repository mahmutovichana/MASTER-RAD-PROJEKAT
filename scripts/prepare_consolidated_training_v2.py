from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from docguard_ml_v2.data_contract import LABEL_SOURCE, PRIMARY_STAGE2_LABELS, validate_final_gold_row


ROOT = PROJECT_ROOT
MERGED = ROOT / "data/final_v2/human_review/consolidated_enriched_training_v2/consolidated_human_review.jsonl"
BASE_GOLD = ROOT / "experiments/consolidated_enriched_training_v1/gold/final_human_gold.jsonl"
OUT = ROOT / "experiments/consolidated_enriched_training_v2/gold"
PARTITIONS = ["development_train", "development_validation", "confirmation"]


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


def finalize(row: dict[str, Any], partition: str, augmentation: bool) -> dict[str, Any]:
    copied = dict(row)
    required = copied.get("human_docs_update_required")
    if not isinstance(required, bool):
        raise ValueError(f"{copied.get('case_id')}: human_docs_update_required is not boolean")
    category = str(copied.get("human_doc_category") or "")
    copied["gold_docs_update_required"] = required
    copied["gold_doc_category"] = category
    copied["label_source"] = LABEL_SOURCE
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
    if len(merged) != 25_134 or len(base_gold) != 21_080:
        raise ValueError(f"Unexpected input sizes: merged={len(merged)}, base_gold={len(base_gold)}")

    base_partition_by_case = {str(row["case_id"]): str(row["partition"]) for row in base_gold}
    if len(base_partition_by_case) != len(base_gold):
        raise ValueError("Base gold contains duplicate case IDs")
    base_repos_by_partition = {
        partition: {repo_id(row) for row in base_gold if row["partition"] == partition}
        for partition in PARTITIONS
    }

    output_rows: list[dict[str, Any]] = []
    new_repositories: set[str] = set()
    for row in merged:
        case_id = str(row["case_id"])
        if case_id in base_partition_by_case:
            output_rows.append(finalize(row, base_partition_by_case[case_id], augmentation=False))
        else:
            repository = repo_id(row)
            if repository in base_repos_by_partition["development_validation"]:
                raise ValueError(f"Augmentation repository overlaps frozen validation: {repository}")
            if repository in base_repos_by_partition["confirmation"]:
                raise ValueError(f"Augmentation repository overlaps sealed confirmation: {repository}")
            new_repositories.add(repository)
            output_rows.append(finalize(row, "development_train", augmentation=True))

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

    if len(output_rows) != 25_134:
        raise ValueError("Final gold row count mismatch")
    if sum(row["augmentation_train_only"] for row in output_rows) != 4_054:
        raise ValueError("Expected exactly 4,054 train-only augmentation rows")
    if len(rows_by_partition["development_validation"]) != 3_028:
        raise ValueError("Frozen validation row count changed")
    if len(rows_by_partition["confirmation"]) != 3_587:
        raise ValueError("Sealed confirmation row count changed")

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
    base_validation_ids = {str(row["case_id"]) for row in base_gold if row["partition"] == "development_validation"}
    base_confirmation_ids = {str(row["case_id"]) for row in base_gold if row["partition"] == "confirmation"}
    validation_ids = {str(row["case_id"]) for row in rows_by_partition["development_validation"]}
    confirmation_ids = {str(row["case_id"]) for row in rows_by_partition["confirmation"]}
    manifest = {
        "version": "consolidated_enriched_training_v2_gold",
        "row_count": len(output_rows),
        "partition_row_counts": {partition: len(rows) for partition, rows in rows_by_partition.items()},
        "partition_repository_counts": {partition: len(repos) for partition, repos in repos_by_partition.items()},
        "class_counts": class_counts,
        "category_counts": category_counts,
        "augmentation_train_only_rows": 4_054,
        "augmentation_repository_count": len(new_repositories),
        "repository_overlap_count": len(repo_overlap),
        "frozen_validation_case_ids_preserved": validation_ids == base_validation_ids,
        "sealed_confirmation_case_ids_preserved": confirmation_ids == base_confirmation_ids,
        "sha256": {},
    }
    for filename in ["final_human_gold.jsonl", "train.jsonl", "validation.jsonl", "confirmation.jsonl"]:
        manifest["sha256"][filename] = sha256_file(OUT / filename)
    if not manifest["frozen_validation_case_ids_preserved"] or not manifest["sealed_confirmation_case_ids_preserved"]:
        raise ValueError("Frozen evaluation membership changed")
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
        "- Repository overlap: **0**",
        "- Validation case membership preserved: **yes**",
        "- Confirmation case membership preserved: **yes**",
        "",
        "All controlled examples and the 54 newly reviewed natural positives are development-train-only. Validation and confirmation retain the earlier natural repository-disjoint membership.",
    ]
    (OUT / "split_report.md").write_text("\n".join(report) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
