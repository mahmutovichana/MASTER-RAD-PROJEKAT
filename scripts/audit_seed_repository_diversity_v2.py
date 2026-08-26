from __future__ import annotations

import argparse
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
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


def repo(row: dict[str, Any]) -> str:
    return str(row.get("repo") or row.get("repository") or "").lower()


def language(row: dict[str, Any]) -> str:
    return str(row.get("language_hint") or row.get("language") or "unknown").lower()


def percentile(values: list[int], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, int(round((pct / 100) * (len(ordered) - 1))))
    return float(ordered[index])


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    repo_counts = Counter(repo(row) for row in rows)
    counts = list(repo_counts.values())
    language_repo: dict[str, Counter] = defaultdict(Counter)
    for row in rows:
        language_repo[language(row)][repo(row)] += 1
    total = len(rows)
    top = repo_counts.most_common(20)
    return {
        "total_seeds": total,
        "unique_repositories": len(repo_counts),
        "seeds_per_repository": {
            "min": min(counts) if counts else 0,
            "median": statistics.median(counts) if counts else 0,
            "mean": statistics.mean(counts) if counts else 0,
            "p90": percentile(counts, 90),
            "p95": percentile(counts, 95),
            "max": max(counts) if counts else 0,
        },
        "top_20_repositories": top,
        "top_repository_share": (top[0][1] / total) if total and top else 0,
        "top_10_repository_share": (sum(count for _repo, count in repo_counts.most_common(10)) / total) if total else 0,
        "language_distribution": dict(Counter(language(row) for row in rows)),
        "repositories_per_language": {lang: len(counter) for lang, counter in language_repo.items()},
        "seeds_per_language_per_repository": {lang: dict(counter) for lang, counter in language_repo.items()},
        "collector_bucket_distribution": dict(Counter(str(row.get("collector_bucket") or "") for row in rows)),
        "uses_gold_labels": any(any(key.startswith("gold_") for key in row) for row in rows),
    }


def capped_rows(rows: list[dict[str, Any]], max_per_repository: int) -> list[dict[str, Any]]:
    kept: list[dict[str, Any]] = []
    counts: Counter = Counter()
    for row in sorted(rows, key=lambda item: (repo(item), int(item.get("pr_number") or 0), str(item.get("url") or item.get("source_url") or ""))):
        key = repo(row)
        if counts[key] < max_per_repository:
            kept.append(row)
            counts[key] += 1
    return kept


def ensure_not_overwriting_raw(input_path: Path, output_path: Path) -> None:
    if output_path.resolve() == input_path.resolve():
        raise ValueError("Capped output must not overwrite raw merged input.")


def write_report(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# Final V2 Seed Repository Diversity Audit",
        "",
        f"- Total seeds: `{report['total_seeds']}`",
        f"- Unique repositories: `{report['unique_repositories']}`",
        f"- Seeds per repository: `{report['seeds_per_repository']}`",
        f"- Top 20 repositories: `{report['top_20_repositories']}`",
        f"- Top repository share: `{report['top_repository_share']:.4f}`",
        f"- Top 10 repository share: `{report['top_10_repository_share']:.4f}`",
        f"- Language distribution: `{report['language_distribution']}`",
        f"- Repositories per language: `{report['repositories_per_language']}`",
        f"- Collector bucket distribution: `{report['collector_bucket_distribution']}`",
        f"- Uses gold labels: `{report['uses_gold_labels']}`",
        "",
        "No gold labels are used. Optional repository capping is pre-label sampling design only.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Final V2 seed repository diversity.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--report", default="reports/final_v2/seed_repository_diversity_v2.md")
    parser.add_argument("--json-report", default="reports/final_v2/seed_repository_diversity_v2.json")
    parser.add_argument("--max-per-repository", type=int)
    parser.add_argument("--capped-output")
    parser.add_argument("--capped-manifest")
    args = parser.parse_args()
    rows = load_jsonl(Path(args.input))
    report = summarize(rows)
    if report["uses_gold_labels"]:
        raise ValueError("Diversity audit input contains gold label fields; use pre-label seed rows only.")
    if args.max_per_repository is not None:
        capped = capped_rows(rows, args.max_per_repository)
        capped_output = Path(args.capped_output or "data/final_v2/merged_pr_seeds_v2.capped.jsonl")
        capped_manifest = Path(args.capped_manifest or "data/final_v2/merged_pr_seeds_v2.capped_manifest.json")
        ensure_not_overwriting_raw(Path(args.input), capped_output)
        write_jsonl(capped_output, capped)
        capped_manifest.parent.mkdir(parents=True, exist_ok=True)
        capped_manifest.write_text(json.dumps({"max_per_repository": args.max_per_repository, "raw_rows": len(rows), "capped_rows": len(capped), "raw_input_preserved": True}, indent=2), encoding="utf-8")
        report["capped_output"] = str(capped_output)
    write_report(Path(args.report), report)
    Path(args.json_report).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_report).write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"status": "ok", "report": args.report, "total_seeds": len(rows)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
