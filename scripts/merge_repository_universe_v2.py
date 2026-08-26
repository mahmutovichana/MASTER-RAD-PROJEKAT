from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def normalize_repo(value: str) -> str:
    return value.strip().lower().replace("https://github.com/", "").strip("/")


def load_rows(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if path.suffix.lower() == ".jsonl":
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    raw = json.loads(line)
                    repo = raw.get("repo") or raw.get("repository")
                    if repo:
                        rows.append(dict(raw, repo=normalize_repo(str(repo))))
        return rows
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip() and not line.strip().startswith("#"):
                parts = [part.strip() for part in line.split(",")]
                rows.append({"repo": normalize_repo(parts[0]), "language_hint": parts[1] if len(parts) > 1 else "", "provenance": [str(path)]})
    return rows


def merge(paths: list[Path]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    duplicates = 0
    source_counts: Counter = Counter()
    for path in paths:
        for row in load_rows(path):
            repo = normalize_repo(str(row["repo"]))
            source_counts[str(path)] += 1
            if repo in merged:
                duplicates += 1
                provenance = list(merged[repo].get("provenance") or [])
                provenance.extend(row.get("provenance") or [str(path)])
                merged[repo]["provenance"] = sorted(set(str(item) for item in provenance))
                continue
            copied = dict(row)
            copied["repo"] = repo
            copied["provenance"] = list(copied.get("provenance") or [str(path)])
            merged[repo] = copied
    rows = sorted(merged.values(), key=lambda row: row["repo"])
    manifest = {
        "total_repositories": len(rows),
        "per_language_repositories": dict(Counter(str(row.get("language_hint") or "") for row in rows)),
        "source_counts": dict(source_counts),
        "duplicates_removed": duplicates,
        "strata_counts": dict(Counter(str(row.get("discovery_stratum") or "historical_or_unspecified") for row in rows)),
        "historical_vs_newly_discovered": {
            "newly_discovered": sum(1 for row in rows if "discovered_repository_universe_v2" in (row.get("provenance") or [])),
            "historical_or_other": sum(1 for row in rows if "discovered_repository_universe_v2" not in (row.get("provenance") or [])),
        },
    }
    return rows, manifest


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_report(path: Path, manifest: dict[str, Any]) -> None:
    lines = [
        "# Final Repository Universe V2",
        "",
        f"- Total repositories: `{manifest['total_repositories']}`",
        f"- Per-language repositories: `{manifest['per_language_repositories']}`",
        f"- Source counts: `{manifest['source_counts']}`",
        f"- Star/activity strata: `{manifest['strata_counts']}`",
        f"- Historical vs newly discovered: `{manifest['historical_vs_newly_discovered']}`",
        f"- Duplicates removed: `{manifest['duplicates_removed']}`",
        "",
        "No labels are used in repository universe merging.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge Final V2 repository universe sources.")
    parser.add_argument("--input", action="append", required=True)
    parser.add_argument("--output", default="data/final_v2/repository_universe/final_repository_universe_v2.jsonl")
    parser.add_argument("--manifest", default="data/final_v2/repository_universe/final_repository_universe_manifest.json")
    parser.add_argument("--report", default="reports/final_v2/final_repository_universe_v2.md")
    args = parser.parse_args()
    rows, manifest = merge([Path(path) for path in args.input])
    write_jsonl(Path(args.output), rows)
    Path(args.manifest).parent.mkdir(parents=True, exist_ok=True)
    Path(args.manifest).write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    write_report(Path(args.report), manifest)
    print(json.dumps({"status": "ok", **manifest}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
