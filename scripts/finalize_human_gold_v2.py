from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.human_review_workflow_v2 import validate_integrity


LABEL_SOURCE = "human_reviewed_final_v2"
PRIMARY_STAGE2 = {"api_reference", "configuration", "developer_setup", "model_contract"}
ALLOWED_CATEGORIES = PRIMARY_STAGE2 | {"other_documentation", "no_update"}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError(f"Row at {path}:{line_number} is not an object")
            rows.append(row)
    return rows


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


def as_bool(value: Any, row_id: str) -> bool:
    if isinstance(value, bool):
        return value
    raise ValueError(f"{row_id}: human_docs_update_required must be boolean")


def repo_id(row: dict[str, Any]) -> str:
    value = row.get("repository") or row.get("repo") or row.get("project_id")
    if not value:
        url = str(row.get("source_url") or row.get("url") or "")
        parts = url.split("github.com/")[-1].split("/")
        if len(parts) >= 2:
            value = "/".join(parts[:2])
    if not value:
        raise ValueError(f"Missing repository identity for row {row.get('case_id') or row.get('id')}")
    return str(value).strip().lower()


def load_partition_assignments(path: Path | None) -> dict[str, str]:
    if path is None:
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("confirmation_sealed") is not True:
        raise ValueError("Partition manifest must have confirmation_sealed=true")
    return {str(repo).lower(): str(partition) for repo, partition in (payload.get("repository_assignments") or {}).items()}


def finalize_row(row: dict[str, Any], index: int, partition_assignments: dict[str, str] | None = None) -> dict[str, Any]:
    row_id = str(row.get("case_id") or row.get("id") or f"row_{index}")
    if row.get("review_status") != "approved":
        raise ValueError(f"{row_id}: review_status must be approved before finalization")
    if row.get("review_row_hash"):
        ok, reason = validate_integrity(row)
        if not ok:
            raise ValueError(f"{row_id}: {reason}")
    docs_required = as_bool(row.get("human_docs_update_required"), row_id)
    human_category = str(row.get("human_doc_category") or "").strip()
    if docs_required:
        if human_category not in ALLOWED_CATEGORIES or human_category == "no_update":
            raise ValueError(f"{row_id}: positive rows require a supported non-no_update human_doc_category")
        final_category = human_category
    else:
        final_category = "no_update"
    copied = dict(row)
    copied["gold_docs_update_required"] = docs_required
    copied["gold_doc_category"] = final_category
    copied["label_source"] = LABEL_SOURCE
    copied["human_review_complete"] = True
    copied["stage2_primary_eligible"] = docs_required and final_category in PRIMARY_STAGE2
    copied["stage2_coverage_bucket"] = final_category if docs_required else "no_update"
    if partition_assignments is not None:
        repo = repo_id(row)
        if repo not in partition_assignments:
            raise ValueError(f"{row_id}: repository missing from frozen partition manifest: {repo}")
        copied["partition"] = partition_assignments[repo]
    return copied


def counts(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    return dict(Counter(str(row.get(key) or "") for row in rows))


def manifest(rows: list[dict[str, Any]], output_jsonl: Path, seed: int | None) -> dict[str, Any]:
    return {
        "label_source": LABEL_SOURCE,
        "seed": seed,
        "sha256": sha256_file(output_jsonl),
        "row_count": len(rows),
        "language_counts": counts(rows, "language"),
        "class_counts": counts(rows, "gold_docs_update_required"),
        "category_counts": counts(rows, "gold_doc_category"),
        "reviewer_completion_counts": counts(rows, "review_status"),
        "stage2_primary_eligible_count": sum(1 for row in rows if row.get("stage2_primary_eligible")),
        "stage2_other_documentation_count": sum(1 for row in rows if row.get("gold_doc_category") == "other_documentation"),
        "no_class_balancing_performed": True,
    }


def write_report(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Final Human Gold V2 Validation Report",
        "",
        f"- Label source: `{payload['label_source']}`",
        f"- Rows: `{payload['row_count']}`",
        f"- SHA256: `{payload['sha256']}`",
        f"- Language counts: `{payload['language_counts']}`",
        f"- Binary class counts: `{payload['class_counts']}`",
        f"- Category counts: `{payload['category_counts']}`",
        f"- Reviewer completion counts: `{payload['reviewer_completion_counts']}`",
        f"- Primary Stage-2 eligible rows: `{payload['stage2_primary_eligible_count']}`",
        f"- Other documentation positive rows: `{payload['stage2_other_documentation_count']}`",
        "",
        "No class balancing performed.",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Finalize human-reviewed Final V2 gold labels.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--partition-manifest")
    args = parser.parse_args()
    out_dir = Path(args.output_dir)
    partition_assignments = load_partition_assignments(Path(args.partition_manifest)) if args.partition_manifest else None
    rows = [finalize_row(row, index, partition_assignments) for index, row in enumerate(load_jsonl(Path(args.input)), 1)]
    output_jsonl = out_dir / "final_human_gold.jsonl"
    write_jsonl(output_jsonl, rows)
    if partition_assignments is not None:
        split_files = {
            "development_train": "train.jsonl",
            "development_validation": "validation.jsonl",
            "confirmation": "confirmation.jsonl",
        }
        for partition, filename in split_files.items():
            write_jsonl(out_dir / filename, [row for row in rows if row.get("partition") == partition])
    payload = manifest(rows, output_jsonl, args.seed)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "human_gold_manifest.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    write_report(out_dir / "human_gold_validation_report.md", payload)
    print(json.dumps({"status": "ok", "rows": len(rows), "output_dir": str(out_dir)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
