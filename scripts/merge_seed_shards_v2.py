from __future__ import annotations

import argparse
import json
from collections import Counter
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


def pr_key(row: dict[str, Any]) -> str:
    repo = str(row.get("repo") or row.get("repository") or "").lower()
    pr = row.get("pr_number")
    return f"{repo}#{int(pr)}" if repo and pr is not None else ""


def source_url(row: dict[str, Any]) -> str:
    return str(row.get("url") or row.get("source_url") or "").strip().lower()


def comparable(row: dict[str, Any]) -> dict[str, Any]:
    return {key: row.get(key) for key in ["repo", "repository", "pr_number", "url", "source_url", "language_hint", "collector_bucket", "pr_title", "merged_at"]}


def merge(paths: list[Path]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    index: dict[str, dict[str, Any]] = {}
    conflicts: list[dict[str, Any]] = []
    for path in paths:
        shard_name = path.stem
        for row in load_jsonl(path):
            keys = [key for key in [pr_key(row), source_url(row)] if key]
            existing = next((index[key] for key in keys if key in index), None)
            if existing is None:
                copied = dict(row)
                copied["source_shards"] = [shard_name]
                merged.append(copied)
                for key in keys:
                    index[key] = copied
                continue
            if comparable(existing) != comparable(row):
                conflicts.append({"conflict_reason": "duplicate_pr_or_url_with_inconsistent_metadata", "existing": existing, "incoming": row, "incoming_shard": shard_name})
                continue
            existing["source_shards"] = sorted(set((existing.get("source_shards") or []) + [shard_name]))
    manifest = {
        "input_shards": [str(path) for path in paths],
        "merged_rows": len(merged),
        "conflicts": len(conflicts),
        "language_counts": dict(Counter(str(row.get("language_hint") or "") for row in merged)),
        "collector_bucket_counts": dict(Counter(str(row.get("collector_bucket") or "") for row in merged)),
    }
    return merged, conflicts, manifest


def write_report(path: Path, manifest: dict[str, Any]) -> None:
    lines = [
        "# Final V2 Seed Shard Merge Report",
        "",
        f"- Input shards: `{manifest['input_shards']}`",
        f"- Merged rows: `{manifest['merged_rows']}`",
        f"- Conflicts: `{manifest['conflicts']}`",
        f"- Language counts: `{manifest['language_counts']}`",
        f"- Collector bucket counts: `{manifest['collector_bucket_counts']}`",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge Final V2 PR seed shards with strict duplicate handling.")
    parser.add_argument("--input", action="append", required=True)
    parser.add_argument("--output", default="data/final_v2/merged_pr_seeds_v2.jsonl")
    parser.add_argument("--manifest", default="data/final_v2/merge_manifest.json")
    parser.add_argument("--conflicts", default="data/final_v2/merge_conflicts.jsonl")
    parser.add_argument("--report", default="reports/final_v2/merge_report.md")
    args = parser.parse_args()
    merged, conflicts, manifest = merge([Path(path) for path in args.input])
    write_jsonl(Path(args.output), merged)
    write_jsonl(Path(args.conflicts), conflicts)
    Path(args.manifest).parent.mkdir(parents=True, exist_ok=True)
    Path(args.manifest).write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    write_report(Path(args.report), manifest)
    print(json.dumps({"status": "conflicts" if conflicts else "ok", **manifest}, indent=2))
    return 1 if conflicts else 0


if __name__ == "__main__":
    raise SystemExit(main())
