from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


PARTITIONS = ["development_train", "development_validation", "confirmation"]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


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


def case_id(row: dict[str, Any], index: int) -> str:
    return str(row.get("case_id") or row.get("id") or f"row_{index}")


def stable_score(repo: str, seed: int) -> str:
    return hashlib.sha256(f"{seed}:{repo}".encode("utf-8")).hexdigest()


def seen_repositories(paths: list[Path]) -> set[str]:
    seen: set[str] = set()
    for path in paths:
        for row in load_jsonl(path):
            seen.add(repo_id(row))
    return seen


def assign_partitions(rows: list[dict[str, Any]], *, seed: int, confirmation_fraction: float, previously_seen: set[str]) -> dict[str, str]:
    repos = sorted({repo_id(row) for row in rows}, key=lambda repo: stable_score(repo, seed))
    eligible_confirmation = [repo for repo in repos if repo not in previously_seen]
    confirmation_count = min(int(round(len(repos) * confirmation_fraction)), len(eligible_confirmation))
    confirmation = set(eligible_confirmation[:confirmation_count])
    development = [repo for repo in repos if repo not in confirmation]
    validation_count = max(1, int(round(len(development) * 0.2))) if len(development) > 1 else 0
    validation = set(development[:validation_count])
    return {
        repo: "confirmation" if repo in confirmation else "development_validation" if repo in validation else "development_train"
        for repo in repos
    }


def counts(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    return dict(Counter(str(row.get(key) or "") for row in rows))


def audit(rows_by_split: dict[str, list[dict[str, Any]]], previously_seen: set[str]) -> dict[str, Any]:
    repos_by_split = {split: {repo_id(row) for row in rows} for split, rows in rows_by_split.items()}
    ids_by_split = {split: {case_id(row, i) for i, row in enumerate(rows, 1)} for split, rows in rows_by_split.items()}
    urls = [str(row.get("source_url") or row.get("url") or "") for rows in rows_by_split.values() for row in rows if row.get("source_url") or row.get("url")]
    repo_overlap: set[str] = set()
    case_overlap: set[str] = set()
    for i, left in enumerate(PARTITIONS):
        for right in PARTITIONS[i + 1 :]:
            repo_overlap |= repos_by_split.get(left, set()) & repos_by_split.get(right, set())
            case_overlap |= ids_by_split.get(left, set()) & ids_by_split.get(right, set())
    duplicate_urls = [url for url, count in Counter(urls).items() if count > 1]
    confirmation_seen = sorted(repos_by_split.get("confirmation", set()) & previously_seen)
    return {
        "repository_overlap_count": len(repo_overlap),
        "case_id_overlap_count": len(case_overlap),
        "source_url_duplicate_count": len(duplicate_urls),
        "confirmation_previously_seen_count": len(confirmation_seen),
        "confirmation_previously_seen_repositories": confirmation_seen,
        "confirmation_sealed": True,
    }


def write_report(path: Path, manifest: dict[str, Any], audit_payload: dict[str, Any]) -> None:
    lines = [
        "# Final V2 Repository Partition Report",
        "",
        f"- Seed: `{manifest['seed']}`",
        f"- Confirmation repository fraction: `{manifest['confirmation_repository_fraction']}`",
        f"- Confirmation sealed: `{manifest['confirmation_sealed']}`",
        f"- Partition row counts: `{manifest['partition_row_counts']}`",
        f"- Partition repository counts: `{manifest['partition_repository_counts']}`",
        f"- Natural class counts if labels are present: `{manifest['natural_class_counts_if_present']}`",
        f"- Category counts if labels are present: `{manifest['category_counts_if_present']}`",
        "",
        "NO CLASS BALANCING / OVERSAMPLING / UNDERSAMPLING / SMOTE.",
        "",
        "## Audit",
        "",
        f"- Repository overlap: `{audit_payload['repository_overlap_count']}`",
        f"- Case ID overlap: `{audit_payload['case_id_overlap_count']}`",
        f"- Source URL duplicates: `{audit_payload['source_url_duplicate_count']}`",
        f"- Confirmation repositories previously seen: `{audit_payload['confirmation_previously_seen_count']}`",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def build(rows: list[dict[str, Any]], *, seed: int, confirmation_fraction: float, previously_seen: set[str]) -> tuple[dict[str, Any], dict[str, list[dict[str, Any]]], dict[str, Any]]:
    assignments = assign_partitions(rows, seed=seed, confirmation_fraction=confirmation_fraction, previously_seen=previously_seen)
    rows_by_split: dict[str, list[dict[str, Any]]] = {partition: [] for partition in PARTITIONS}
    for row in rows:
        copied = dict(row)
        copied["partition"] = assignments[repo_id(row)]
        rows_by_split[copied["partition"]].append(copied)
    audit_payload = audit(rows_by_split, previously_seen)
    manifest = {
        "seed": seed,
        "confirmation_repository_fraction": confirmation_fraction,
        "confirmation_sealed": True,
        "repository_assignments": assignments,
        "previously_seen_repository_count": len(previously_seen),
        "partition_row_counts": {split: len(split_rows) for split, split_rows in rows_by_split.items()},
        "partition_repository_counts": {split: len({repo_id(row) for row in split_rows}) for split, split_rows in rows_by_split.items()},
        "natural_class_counts_if_present": counts(rows, "gold_docs_update_required") if any("gold_docs_update_required" in row for row in rows) else {},
        "category_counts_if_present": counts(rows, "gold_doc_category") if any("gold_doc_category" in row for row in rows) else {},
        "no_class_balancing_performed": True,
    }
    return manifest, rows_by_split, audit_payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Build label-independent canonical Final V2 repository partitions.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--previously-seen-dataset", action="append", default=[])
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--confirmation-repository-fraction", type=float, default=0.2)
    args = parser.parse_args()
    rows = load_jsonl(Path(args.input))
    seen = seen_repositories([Path(path) for path in args.previously_seen_dataset])
    manifest, rows_by_split, audit_payload = build(rows, seed=args.seed, confirmation_fraction=args.confirmation_repository_fraction, previously_seen=seen)
    if any(audit_payload[key] for key in ["repository_overlap_count", "case_id_overlap_count", "source_url_duplicate_count", "confirmation_previously_seen_count"]):
        raise ValueError(f"Partition audit failed: {audit_payload}")
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(out_dir / "candidate_train.jsonl", rows_by_split["development_train"])
    write_jsonl(out_dir / "candidate_validation.jsonl", rows_by_split["development_validation"])
    write_jsonl(out_dir / "candidate_confirmation.jsonl", rows_by_split["confirmation"])
    (out_dir / "repository_partition_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    (out_dir / "partition_audit.json").write_text(json.dumps(audit_payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    write_report(out_dir / "partition_report.md", manifest, audit_payload)
    print(json.dumps({"status": "ok", "output_dir": str(out_dir), "rows": len(rows)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
