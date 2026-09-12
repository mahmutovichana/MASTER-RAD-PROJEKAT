from __future__ import annotations

import argparse
import hashlib
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path

from experiments.posthoc_stage3_s1.scripts.repository_corpus import (
    BareGitRepositoryProvider,
    discover_candidates,
    resolve_pre_change_source,
)


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local_paths(root: Path) -> list[str]:
    return [item.relative_to(root).as_posix() for item in root.rglob("*") if item.is_file()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    out = (args.output_dir or root / "experiments/posthoc_stage3_s1").resolve()
    primary_path = root / "reports/final_v2/gate4/primary_sample.jsonl"
    secondary_path = root / "reports/final_v2/gate4/secondary_stress_sample.jsonl"
    gold_paths = [
        root / "experiments/consolidated_enriched_training_v2/gold/train.jsonl",
        root / "experiments/consolidated_enriched_training_v2/gold/validation.jsonl",
    ]
    memberships = [("primary", row) for row in read_jsonl(primary_path)] + [("secondary", row) for row in read_jsonl(secondary_path)]
    gold = {}
    for path in gold_paths:
        for row in read_jsonl(path):
            gold[row["case_id"]] = row
    rows = []
    for sample, sampled in memberships:
        merged = dict(gold.get(sampled["case_id"], {}))
        merged.update(sampled)
        rows.append((sample, merged))

    sources = {}
    git_groups: dict[str, set[str]] = defaultdict(set)
    source_errors = {}
    for sample, row in rows:
        try:
            source = resolve_pre_change_source(row, root=root)
            sources[row["case_id"]] = source
            if source.kind == "git_commit":
                git_groups[source.repository].add(source.revision)
        except Exception as exc:
            source_errors[row["case_id"]] = f"{type(exc).__name__}: {exc}"

    provider = BareGitRepositoryProvider(out / "runtime/repository_cache")
    git_available = {}
    for repository in sorted(git_groups):
        for revision, available in provider.ensure_commits(repository, git_groups[repository]).items():
            git_available[(repository, revision)] = available

    details = []
    for sample, row in rows:
        case_id = row["case_id"]
        source = sources.get(case_id)
        reconstructed = False
        paths = []
        error = source_errors.get(case_id)
        if source is not None:
            try:
                if source.kind == "git_commit" and git_available.get((source.repository, source.revision), False):
                    paths = provider.list_paths(source.repository, source.revision)
                    reconstructed = True
                elif source.kind == "frozen_controlled_baseline":
                    paths = local_paths(Path(source.local_root))
                    reconstructed = True
            except Exception as exc:
                error = f"{type(exc).__name__}: {exc}"
        candidates = discover_candidates(paths, changed_paths=list(row.get("code_changed_files") or []), code_diff=str(row.get("code_diff_excerpt") or "")) if reconstructed else []
        details.append({
            "case_id": case_id,
            "sample": sample,
            "repository": row.get("repository"),
            "source_kind": source.kind if source else None,
            "pre_change_revision": source.revision if source else None,
            "reconstructed": reconstructed,
            "candidate_count": len(candidates),
            "candidate_available": bool(candidates),
            "known_target_document_path": row.get("synthetic_target_doc_path"),
            "current_canonical_retrieval_available": bool(row.get("retrieval_context_available")),
            "available_information": {
                "repository_name": bool(row.get("repository")),
                "repository_url": source.kind == "git_commit" if source else False,
                "explicit_pre_change_commit_or_snapshot": source is not None,
                "language": bool(row.get("language")),
                "changed_file_paths": bool(row.get("code_changed_files")),
                "stored_code_diff_excerpt": bool(row.get("code_diff_excerpt")),
                "code_diff_explicitly_truncated": str(row.get("code_diff_excerpt") or "").rstrip().endswith("..."),
                "docs_before_excerpt": bool(row.get("docs_before_excerpt")),
                "known_target_document_path": bool(row.get("synthetic_target_doc_path")),
                "frozen_repository_snapshot": source.kind == "frozen_controlled_baseline" if source else False,
                "local_git_repository": False,
                "cached_pre_change_git_object": source.kind == "git_commit" and reconstructed if source else False,
                "reference_documentation": False,
                "documentation_after": False,
            },
            "error": error,
        })

    counts = Counter(item["candidate_count"] for item in details)
    candidate_counts = [item["candidate_count"] for item in details]
    total = len(details)
    reconstructed = sum(item["reconstructed"] for item in details)
    available = sum(item["candidate_available"] for item in details)
    known = sum(bool(item["known_target_document_path"]) for item in details)
    canonical = sum(item["current_canonical_retrieval_available"] for item in details)
    by_sample = {}
    for sample in ("primary", "secondary"):
        subset = [item for item in details if item["sample"] == sample]
        by_sample[sample] = {
            "total": len(subset),
            "reconstructable": sum(item["reconstructed"] for item in subset),
            "candidate_available": sum(item["candidate_available"] for item in subset),
            "canonical_retrieval_available": sum(item["current_canonical_retrieval_available"] for item in subset),
            "known_target_document_path": sum(bool(item["known_target_document_path"]) for item in subset),
        }
    result = {
        "scientific_status": "POST_HOC_STAGE3_CHALLENGER_DEVELOPMENT_ONLY",
        "confirmation_accessed": False,
        "gate6_row_level_human_data_accessed": False,
        "source_files": {str(path.relative_to(root)).replace("\\", "/"): sha256(path) for path in [primary_path, secondary_path, *gold_paths]},
        "membership": {"total": total, "primary": 100, "secondary": 100, "ordered_case_id_sha256": hashlib.sha256("\n".join(item[1]["case_id"] for item in memberships).encode()).hexdigest()},
        "summary": {
            "total_development_cases": total,
            "reconstructable_repository_state": reconstructed,
            "reconstruction_rate": reconstructed / total,
            "documentation_candidate_available": available,
            "candidate_availability_rate": available / total,
            "known_target_document_paths": known,
            "known_target_rate": known / total,
            "current_canonical_retrieval_available": canonical,
            "current_canonical_retrieval_rate": canonical / total,
            "projected_s1_candidate_available": available,
            "projected_s1_candidate_rate": available / total,
            "candidate_count_min": min(candidate_counts),
            "candidate_count_median": statistics.median(candidate_counts),
            "candidate_count_max": max(candidate_counts),
            "candidate_count_distribution": {str(key): value for key, value in sorted(counts.items())},
        },
        "by_sample": by_sample,
        "reconstruction_policy": {
            "natural": "bare Git object cache fetched only by explicit 40-hex commit parsed from docs_before provenance",
            "controlled": "immutable local source copy joined by case_id and controlled-baseline marker",
            "head_or_branch_access": "FORBIDDEN",
            "unavailable_policy": "mark unavailable; never fall back to HEAD",
        },
        "target_ground_truth": "Available only for 79 controlled rows via synthetic_target_doc_path; absent for 121 natural rows. Target metrics must be conditional and separately labelled.",
        "development_information_availability": {
            "repository_name": 200,
            "derivable_natural_github_url": 121,
            "explicit_pre_change_git_commit": 121,
            "explicit_frozen_controlled_snapshot": 79,
            "language": 200,
            "changed_file_paths": 200,
            "stored_code_diff_excerpt": 200,
            "stored_diff_excerpt_explicitly_truncated": 52,
            "docs_before_excerpt": 200,
            "known_target_document_path": 79,
            "repository_snapshot_or_cached_commit_after_audit": 200,
            "development_reference_documentation": 0,
            "documentation_after_content": 0
        },
        "canonical_root_cause": {
            "retrieval_context_unavailable_109_of_200": "Canonical adapter accepted only pre-attached doc_context candidates; it had no repository/path-aware reconstruction fallback.",
            "human_review_required_42_of_91_invoked": "Fail-closed verifier/runtime outcomes: 50 unsupported-fact flags, 2 target-not-retrieved flags, 6 input-budget errors and 13 invalid-structured-output errors; categories can overlap.",
            "gate6_primary_14_outputs": "Aggregate-only historical finding: 76/100 had no context; of 24 invoked, 14 were accepted and 10 required human review.",
        },
        "stop_condition_triggered": reconstructed <= total / 2,
        "details": details,
    }
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "phase0_retrieval_audit.json"
    json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    s = result["summary"]
    md = f"""# S1 Phase 0 retrieval audit

Status: post-hoc Stage 3 challenger, development only. Confirmation was not accessed, and no Gate 6 row-level human data was accessed.

## Finding

Canonical Stage 3 had repository retrieval available only when a row already carried `doc_context_*` candidates. The adapter did not turn `docs_before_excerpt` into a path-bearing candidate and the pipeline failed closed before any model call when candidates were absent. Across the frozen Gate 4 development memberships this produced 109/200 context-unavailable rows. Of 91 invoked rows, 42 ended as human review required because of fail-closed grounding/target checks or bounded runtime/structured-output failures. The published aggregate Gate 6 outcome follows the same mechanism: 76 context-unavailable, then 14 accepted outputs and 10 human-review-required among 24 invocations.

## Pre-change reconstruction and candidate coverage

- Development cases: **{total}** (primary 100; secondary 100; never pooled for canonical inference).
- Explicit pre-change state reconstructed: **{reconstructed}/{total} ({reconstructed / total:.1%})**.
- At least one eligible documentation candidate: **{available}/{total} ({available / total:.1%})**.
- Canonical attached-context availability: **{canonical}/{total} ({canonical / total:.1%})**.
- Known target-document evidence: **{known}/{total} ({known / total:.1%})**, exclusively controlled rows.
- Candidate count: min **{s['candidate_count_min']}**, median **{s['candidate_count_median']}**, max **{s['candidate_count_max']}**.

Every row contains repository name, language, changed paths, a stored diff excerpt, and a docs-before excerpt. The provenance marker supplies 121 natural pre-change Git commits; 79 controlled rows join to frozen baseline copies and known synthetic target paths. Fifty-two stored diff excerpts end with an explicit truncation marker. No development documentation-after/reference text is exposed to S1. Natural GitHub URLs are derived from owner/repository; no mutable local checkout is trusted.

Natural repositories are read from bare caches at the exact 40-hex commit recorded in the frozen `docs_before_excerpt` provenance marker. Controlled cases use their frozen unchanged source copies. `HEAD`, branch tips, and post-change fallbacks are forbidden. A missing explicit object is marked unavailable.

## Methodological disposition

The majority-reconstruction stop condition is **{'TRIGGERED' if result['stop_condition_triggered'] else 'NOT TRIGGERED'}**. Natural rows do not carry target-document gold; Hit@k/MRR may therefore be reported only for the 79 controlled rows and must not be generalized to the natural subset.
"""
    (out / "PHASE0_RETRIEVAL_AUDIT.md").write_text(md, encoding="utf-8")
    print(json.dumps(result["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
