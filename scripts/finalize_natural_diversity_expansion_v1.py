"""Audit, split, and prepare pending human review for the natural pilot.

This script never assigns labels.  Repository partitioning is deterministic
and label-independent, and review rows expose only pre-change evidence.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


ORIGIN = "natural_diversity_expansion_v1"
SAFE_MODEL_FIELDS = {"language", "code_changed_files", "code_diff_excerpt", "docs_before_excerpt"}
FORBIDDEN_REVIEW_FIELDS = {"docs_changed_files", "docs_diff_excerpt", "docs_after_excerpt", "head_sha", "merged_at", "candidate_evidence", "audit_only_fields"}
REVIEW_COLUMNS = [
    "case_id", "repository", "pr_number", "language", "source_url", "base_sha",
    "code_changed_files", "code_diff_excerpt", "docs_before_excerpt",
    "docs_before_retrieved_files", "documentation_context_candidates",
    "candidate_surface_stratum", "acquisition_origin", "partition",
    "human_docs_update_required", "human_doc_category", "human_label_notes",
    "review_status", "label_source", "review_row_hash",
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def deterministic_repo_split(repositories: set[str], *, seed: int, refresh_fraction: float = 0.2) -> dict[str, str]:
    ordered = sorted(repositories, key=lambda repo: hashlib.sha256(f"{seed}:{repo}".encode()).hexdigest())
    refresh_count = max(1, round(len(ordered) * refresh_fraction))
    refresh = set(ordered[:refresh_count])
    return {repo: "refresh_validation" if repo in refresh else "development_train" for repo in sorted(repositories)}


def review_hash(row: dict[str, Any]) -> str:
    immutable = {key: row.get(key) for key in REVIEW_COLUMNS if key not in {"human_docs_update_required", "human_doc_category", "human_label_notes", "review_status", "label_source", "review_row_hash"}}
    return hashlib.sha256(json.dumps(immutable, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def make_review_row(row: dict[str, Any], *, surface: str, partition: str) -> dict[str, Any]:
    model_input = row.get("classifier_model_input") or {}
    review = {
        "case_id": row.get("case_id"),
        "repository": str(row.get("repository") or "").lower(),
        "pr_number": row.get("pr_number"),
        "language": model_input.get("language") or row.get("language"),
        "source_url": row.get("source_url"),
        "base_sha": row.get("base_sha"),
        "code_changed_files": model_input.get("code_changed_files") or row.get("code_changed_files") or [],
        "code_diff_excerpt": model_input.get("code_diff_excerpt") or row.get("code_diff_excerpt") or "",
        "docs_before_excerpt": model_input.get("docs_before_excerpt") or row.get("docs_before_excerpt") or "",
        "docs_before_retrieved_files": row.get("docs_before_retrieved_files") or [],
        "documentation_context_candidates": row.get("documentation_context_candidates") or [],
        "candidate_surface_stratum": surface,
        "acquisition_origin": ORIGIN,
        "partition": partition,
        "human_docs_update_required": None,
        "human_doc_category": None,
        "human_label_notes": "",
        "review_status": "pending",
        "label_source": None,
    }
    review["review_row_hash"] = review_hash(review)
    return review


def audit_candidates(rows: list[dict[str, Any]], *, seen: set[str], surface_assignments: dict[str, str]) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    case_ids = [str(row.get("case_id") or "") for row in rows]
    keys = [(str(row.get("repository") or "").lower(), int(row.get("pr_number") or 0)) for row in rows]
    repositories = {repo for repo, _ in keys}
    duplicate_case_ids = len(case_ids) - len(set(case_ids))
    duplicate_keys = len(keys) - len(set(keys))
    overlap = sorted(repositories & seen)
    if duplicate_case_ids:
        errors.append(f"duplicate case_ids: {duplicate_case_ids}")
    if duplicate_keys:
        errors.append(f"duplicate repository/pr keys: {duplicate_keys}")
    if overlap:
        errors.append(f"seen repository overlap: {overlap}")
    missing_surfaces = sorted(repositories - set(surface_assignments))
    if missing_surfaces:
        errors.append(f"missing surface assignments: {missing_surfaces}")
    forbidden_model_rows = 0
    invalid_base_rows = 0
    excessive_context_rows = 0
    human_labeled_rows = 0
    audit_only_docs_after_rows = 0
    for row in rows:
        model_input = row.get("classifier_model_input") or {}
        if set(model_input) - SAFE_MODEL_FIELDS:
            forbidden_model_rows += 1
        if not row.get("base_sha") or not row.get("docs_before_excerpt"):
            invalid_base_rows += 1
        contexts = row.get("documentation_context_candidates") or []
        if len(contexts) > 12:
            excessive_context_rows += 1
        if any(row.get(field) not in {None, ""} for field in ("human_docs_update_required", "human_doc_category", "human_label_notes", "review_status", "label_source")):
            human_labeled_rows += 1
        if row.get("docs_after_excerpt"):
            audit_only_docs_after_rows += 1
    if forbidden_model_rows:
        errors.append(f"forbidden model-input fields in {forbidden_model_rows} rows")
    if invalid_base_rows:
        errors.append(f"missing BASE-SHA/docs-before evidence in {invalid_base_rows} rows")
    if excessive_context_rows:
        errors.append(f"more than 12 documentation contexts in {excessive_context_rows} rows")
    if human_labeled_rows:
        errors.append(f"pre-labeled candidate rows: {human_labeled_rows}")
    report = {
        "candidate_count": len(rows),
        "repository_count": len(repositories),
        "language_counts": dict(sorted(Counter(str(row.get("language") or "") for row in rows).items())),
        "repository_counts": dict(sorted(Counter(repo for repo, _ in keys).items())),
        "duplicate_case_id_count": duplicate_case_ids,
        "duplicate_repository_pr_count": duplicate_keys,
        "seen_repository_overlap_count": len(overlap),
        "seen_repository_overlap": overlap,
        "forbidden_model_input_row_count": forbidden_model_rows,
        "missing_base_evidence_row_count": invalid_base_rows,
        "excessive_context_row_count": excessive_context_rows,
        "prelabeled_row_count": human_labeled_rows,
        "audit_only_docs_after_present_count": audit_only_docs_after_rows,
        "audit_only_docs_after_used_for_selection_or_review": False,
        "confirmation_accessed": False,
        "errors": errors,
        "passed": not errors,
    }
    return errors, report


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REVIEW_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            encoded = {key: (json.dumps(row.get(key), ensure_ascii=False, sort_keys=True) if isinstance(row.get(key), (list, dict)) else row.get(key)) for key in REVIEW_COLUMNS}
            writer.writerow(encoded)


def run(*, candidates_path: Path, seen_path: Path, seed_plan_path: Path, output_dir: Path, split_seed: int, batch_size: int) -> dict[str, Any]:
    rows = load_jsonl(candidates_path)
    seen_payload = json.loads(seen_path.read_text(encoding="utf-8"))
    seen = {str(repo).lower() for repo in seen_payload.get("repositories", [])}
    seed_plan = json.loads(seed_plan_path.read_text(encoding="utf-8"))
    surfaces = {str(repo).lower(): str(surface) for repo, surface in (seed_plan.get("repository_surface_assignments") or {}).items()}
    errors, audit = audit_candidates(rows, seen=seen, surface_assignments=surfaces)
    audits_dir = output_dir / "audits"
    write_json(audits_dir / "candidate_quality_audit.json", audit)
    (audits_dir / "candidate_quality_audit.md").write_text("# Natural Diversity Expansion V1 candidate audit\n\n" + "\n".join(f"- {key}: `{value}`" for key, value in audit.items() if key != "repository_counts") + "\n", encoding="utf-8")
    if errors:
        raise RuntimeError("candidate audit failed: " + "; ".join(errors))

    repositories = {str(row["repository"]).lower() for row in rows}
    assignments = deterministic_repo_split(repositories, seed=split_seed)
    review_rows = [make_review_row(row, surface=surfaces[str(row["repository"]).lower()], partition=assignments[str(row["repository"]).lower()]) for row in rows]
    train = [row for row in review_rows if row["partition"] == "development_train"]
    refresh = [row for row in review_rows if row["partition"] == "refresh_validation"]
    partitions_dir = output_dir / "partitions"
    write_jsonl(partitions_dir / "development_train_candidates.jsonl", train)
    write_jsonl(partitions_dir / "refresh_validation_candidates.jsonl", refresh)
    split_manifest = {
        "schema": "natural_diversity_expansion_v1_repository_split",
        "seed": split_seed,
        "policy": "deterministic_repository_hash_80_20_before_labels",
        "repository_assignments": assignments,
        "repository_counts": dict(Counter(assignments.values())),
        "row_counts": {"development_train": len(train), "refresh_validation": len(refresh)},
        "label_fields_used": False,
        "no_label_based_partitioning": True,
        "refresh_validation_excluded_from_future_training": True,
        "seen_repository_overlap_count": 0,
        "confirmation_accessed": False,
        "source_candidates_sha256": sha256_file(candidates_path),
    }
    write_json(partitions_dir / "repository_split_manifest.json", split_manifest)

    review_dir = output_dir / "human_review"
    write_jsonl(review_dir / "prefilled_review.jsonl", review_rows)
    batches_dir = review_dir / "review_batches"
    batch_entries: list[dict[str, Any]] = []
    for start in range(0, len(review_rows), batch_size):
        batch = review_rows[start : start + batch_size]
        number = start // batch_size + 1
        jsonl_path = batches_dir / f"batch_{number:03d}.jsonl"
        csv_path = batches_dir / f"batch_{number:03d}.csv"
        write_jsonl(jsonl_path, batch)
        write_csv(csv_path, batch)
        batch_entries.append({"batch": number, "rows": len(batch), "jsonl": str(jsonl_path), "csv": str(csv_path), "jsonl_sha256": sha256_file(jsonl_path), "csv_sha256": sha256_file(csv_path)})
    review_manifest = {
        "schema": "natural_diversity_expansion_v1_pending_human_review",
        "row_count": len(review_rows),
        "batch_size": batch_size,
        "batch_count": len(batch_entries),
        "review_status_counts": {"pending": len(review_rows)},
        "human_label_fields_populated": 0,
        "label_source": None,
        "forbidden_review_fields": sorted(FORBIDDEN_REVIEW_FIELDS),
        "review_columns": REVIEW_COLUMNS,
        "batches": batch_entries,
        "prefilled_review_sha256": sha256_file(review_dir / "prefilled_review.jsonl"),
    }
    write_json(review_dir / "review_batch_manifest.json", review_manifest)
    (review_dir / "REVIEW_INSTRUCTIONS.md").write_text(
        "# Pending independent human review\n\n"
        "Review `code_changed_files`, `code_diff_excerpt`, and `docs_before_excerpt` first. Use `documentation_context_candidates` only as additional pre-change context. Do not use docs-after, docs-diff, PR outcome, or acquisition stratum as a label. Fill only `human_docs_update_required`, `human_doc_category`, `human_label_notes`, and `review_status`.\n",
        encoding="utf-8",
    )
    result = {"audit": audit, "split": split_manifest, "review": {key: value for key, value in review_manifest.items() if key != "batches"}}
    write_json(output_dir / "FINAL_CHECKPOINT_PRE_REVIEW.json", result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit and prepare Natural Diversity Expansion V1 for independent review.")
    parser.add_argument("--candidates", required=True)
    parser.add_argument("--seen-universe", required=True)
    parser.add_argument("--seed-plan", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--split-seed", type=int, default=20260831)
    parser.add_argument("--batch-size", type=int, default=100)
    args = parser.parse_args()
    result = run(candidates_path=Path(args.candidates), seen_path=Path(args.seen_universe), seed_plan_path=Path(args.seed_plan), output_dir=Path(args.output_dir), split_seed=args.split_seed, batch_size=args.batch_size)
    print(json.dumps({"status": "ok", "candidate_count": result["audit"]["candidate_count"], "repositories": result["audit"]["repository_count"], "split": result["split"]["row_counts"], "review_batches": result["review"]["batch_count"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
