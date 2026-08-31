"""Prepare a deterministic, repository-diverse seed plan before labeling.

The strata are acquisition targets derived only from repository documentation
path metadata.  They are not gold labels and are never copied into human label
fields.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


SURFACE_TARGETS = {
    "developer_setup": 8,
    "model_contract": 5,
    "configuration": 4,
    "api_reference": 3,
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def assign_surface_strata(shortlist: list[dict[str, Any]]) -> dict[str, str]:
    if len(shortlist) != sum(SURFACE_TARGETS.values()):
        raise ValueError(f"expected {sum(SURFACE_TARGETS.values())} shortlisted repositories, got {len(shortlist)}")
    available = {str(row["repository"]).lower(): row for row in shortlist}
    assignments: dict[str, str] = {}
    # Scarcer strata are assigned first so API/model coverage is preserved.
    order = ["api_reference", "configuration", "model_contract", "developer_setup"]
    for surface in order:
        target = SURFACE_TARGETS[surface]
        ranked = sorted(
            (row for repo, row in available.items() if repo not in assignments),
            key=lambda row: (
                int((row.get("documentation_surface_signals") or {}).get(surface) or 0),
                int(row.get("surface_coverage") or 0),
                int(row.get("documentation_file_count") or 0),
                str(row.get("repository") or ""),
            ),
            reverse=True,
        )
        chosen = [row for row in ranked if int((row.get("documentation_surface_signals") or {}).get(surface) or 0) > 0][:target]
        if len(chosen) != target:
            raise ValueError(f"insufficient repositories with {surface} signal: {len(chosen)}/{target}")
        for row in chosen:
            assignments[str(row["repository"]).lower()] = surface
    return assignments


def round_robin_seeds(seeds: list[dict[str, Any]], repositories: list[str], *, per_repo: int, minimum_per_repo: int) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in seeds:
        grouped[str(row.get("repo") or row.get("repository") or "").lower()].append(row)
    missing = {repo: minimum_per_repo - len(grouped.get(repo, [])) for repo in repositories if len(grouped.get(repo, [])) < minimum_per_repo}
    if missing:
        raise ValueError(f"insufficient seeds per repository: {missing}")
    ordered: list[dict[str, Any]] = []
    for index in range(per_repo):
        for repo in repositories:
            if index >= len(grouped[repo]):
                continue
            copied = dict(grouped[repo][index])
            copied["candidate_surface_stratum"] = copied.get("candidate_surface_stratum")
            ordered.append(copied)
    return ordered


def choose_feasible_shortlist(shortlist: list[dict[str, Any]], profiles: list[dict[str, Any]], seed_counts: Counter[str], *, minimum_per_repo: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    selected = list(shortlist)
    selected_names = {str(row["repository"]).lower() for row in selected}
    replacements: list[dict[str, Any]] = []
    for index, row in enumerate(list(selected)):
        repo = str(row["repository"]).lower()
        if seed_counts[repo] >= minimum_per_repo:
            continue
        group = str(row.get("language_group") or "")
        alternatives = sorted(
            (
                candidate for candidate in profiles
                if str(candidate.get("language_group") or "") == group
                and str(candidate.get("repository") or "").lower() not in selected_names
                and seed_counts[str(candidate.get("repository") or "").lower()] >= minimum_per_repo
            ),
            key=lambda candidate: (
                int(candidate.get("surface_coverage") or 0),
                seed_counts[str(candidate.get("repository") or "").lower()],
                int(candidate.get("expected_pr_volume_proxy") or 0),
                int(candidate.get("documentation_file_count") or 0),
            ),
            reverse=True,
        )
        if not alternatives:
            raise ValueError(f"no feasible replacement for {repo} ({group})")
        replacement = dict(alternatives[0])
        replacement_repo = str(replacement["repository"]).lower()
        selected[index] = replacement
        selected_names.remove(repo)
        selected_names.add(replacement_repo)
        replacements.append({"removed_repository": repo, "removed_seed_count": seed_counts[repo], "replacement_repository": replacement_repo, "replacement_seed_count": seed_counts[replacement_repo], "reason": "insufficient_natural_seed_volume"})
    for rank, row in enumerate(selected, start=1):
        row["shortlist_rank"] = rank
    return selected, replacements


def run(*, seeds_paths: list[Path], shortlist_path: Path, profile_candidates_path: Path, feasible_shortlist_path: Path, output_path: Path, manifest_path: Path, report_path: Path, per_repo: int, minimum_per_repo: int) -> dict[str, Any]:
    combined: dict[tuple[str, int], dict[str, Any]] = {}
    for seeds_path in seeds_paths:
        for row in load_jsonl(seeds_path):
            repo = str(row.get("repo") or row.get("repository") or "").lower()
            key = (repo, int(row.get("pr_number") or 0))
            combined.setdefault(key, row)
    seeds = list(combined.values())
    shortlist = load_jsonl(shortlist_path)
    profiles = load_jsonl(profile_candidates_path)
    seed_counts = Counter(str(row.get("repo") or row.get("repository") or "").lower() for row in seeds)
    shortlist, replacements = choose_feasible_shortlist(shortlist, profiles, seed_counts, minimum_per_repo=minimum_per_repo)
    write_jsonl(feasible_shortlist_path, shortlist)
    assignments = assign_surface_strata(shortlist)
    repositories = [str(row["repository"]).lower() for row in shortlist]
    planned = round_robin_seeds(seeds, repositories, per_repo=per_repo, minimum_per_repo=minimum_per_repo)
    for row in planned:
        repo = str(row.get("repo") or row.get("repository") or "").lower()
        row["candidate_surface_stratum"] = assignments[repo]
        row["candidate_surface_stratum_is_gold_label"] = False
    write_jsonl(output_path, planned)
    repo_counts = Counter(str(row.get("repo") or row.get("repository") or "").lower() for row in planned)
    surface_counts = Counter(str(row["candidate_surface_stratum"]) for row in planned)
    manifest = {
        "schema": "natural_diversity_expansion_v1_seed_plan",
        "input_seed_sha256": {str(path): sha256(path) for path in seeds_paths},
        "shortlist_sha256": sha256(shortlist_path),
        "output_sha256": sha256(output_path),
        "repository_count": len(repositories),
        "seed_count": len(planned),
        "per_repository_seed_cap": per_repo,
        "minimum_per_repository_required": minimum_per_repo,
        "repository_counts": dict(sorted(repo_counts.items())),
        "repository_surface_assignments": dict(sorted(assignments.items())),
        "surface_stratum_counts": dict(sorted(surface_counts.items())),
        "selection_uses_labels": False,
        "strata_are_gold_labels": False,
        "confirmation_accessed": False,
        "processing_order": "round_robin_by_repository",
        "feasibility_replacements": replacements,
        "feasible_shortlist_sha256": sha256(feasible_shortlist_path),
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# Natural Diversity Expansion V1 seed plan",
        "",
        f"- Repositories: **{len(repositories)}**",
        f"- Planned seeds: **{len(planned)}** (up to {per_repo} per repository)",
        "- Ordering: deterministic round-robin by repository",
        f"- Surface strata: `{dict(sorted(surface_counts.items()))}`",
        f"- Feasibility replacements: `{replacements}`",
        "- Labels used: **False**",
        "- Confirmation accessed: **False**",
        "",
        "Surface strata are pre-label acquisition targets inferred from documentation path metadata. They are not human or gold labels.",
    ]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare a round-robin natural diversity pilot seed plan.")
    parser.add_argument("--seeds", required=True, action="append")
    parser.add_argument("--shortlist", required=True)
    parser.add_argument("--profile-candidates", required=True)
    parser.add_argument("--feasible-shortlist-output", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--per-repo", type=int, default=50)
    parser.add_argument("--minimum-per-repo", type=int, default=10)
    args = parser.parse_args()
    result = run(seeds_paths=[Path(path) for path in args.seeds], shortlist_path=Path(args.shortlist), profile_candidates_path=Path(args.profile_candidates), feasible_shortlist_path=Path(args.feasible_shortlist_output), output_path=Path(args.output), manifest_path=Path(args.manifest), report_path=Path(args.report), per_repo=args.per_repo, minimum_per_repo=args.minimum_per_repo)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
