from __future__ import annotations

import argparse
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path


def count_lines(path: Path) -> int | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        return sum(1 for line in handle if line.strip())


def newest_file_time(path: Path) -> str | None:
    if not path.exists():
        return None
    files = [item for item in path.rglob("*") if item.is_file()]
    if not files:
        return None
    newest = max(files, key=lambda item: item.stat().st_mtime)
    return datetime.fromtimestamp(newest.stat().st_mtime).isoformat(timespec="seconds")


def file_count(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for item in path.rglob("*") if item.is_file())


def python_processes() -> list[str]:
    try:
        completed = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "Get-CimInstance Win32_Process -Filter \"name='python.exe'\" | Select-Object ProcessId,CommandLine | ConvertTo-Json -Compress",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
    except Exception:
        return []

    raw = completed.stdout.strip()
    if not raw:
        return []

    try:
        value = json.loads(raw)
    except json.JSONDecodeError:
        return [raw]

    if isinstance(value, dict):
        value = [value]

    result: list[str] = []
    for item in value:
        if isinstance(item, dict):
            result.append(f"{item.get('ProcessId')}: {item.get('CommandLine')}")
    return result


def snapshot(args: argparse.Namespace) -> dict:
    cache_dir = Path(args.cache_dir)
    seed_path = Path(args.seed_file)
    candidate_path = Path(args.candidates)
    rejects_path = Path(args.rejects)
    report_path = Path(args.report)

    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "python_processes": python_processes(),
        "cache_files": file_count(cache_dir),
        "cache_newest": newest_file_time(cache_dir),
        "seed_rows": count_lines(seed_path),
        "candidate_output_exists": candidate_path.exists(),
        "candidate_rows": count_lines(candidate_path),
        "reject_output_exists": rejects_path.exists(),
        "reject_rows": count_lines(rejects_path),
        "report_exists": report_path.exists(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Watch long-running DocGuard real-case GitHub jobs.")
    parser.add_argument("--cache-dir", default="data/external/project_case_study/cache/github_api")
    parser.add_argument("--seed-file", default="data/external/project_case_study/generated/real_pr_seeds_10k_v1.jsonl")
    parser.add_argument("--candidates", default="data/external/project_case_study/generated/real_pr_candidates_10k_v1.jsonl")
    parser.add_argument("--rejects", default="data/external/project_case_study/generated/real_pr_candidates_10k_v1.rejects.jsonl")
    parser.add_argument("--report", default="reports/real_case_study/generated/real_pr_candidate_dataset_10k_v1.md")
    parser.add_argument("--interval-seconds", type=int, default=60)
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()

    previous_cache_count: int | None = None

    while True:
        snap = snapshot(args)
        cache_delta = None if previous_cache_count is None else snap["cache_files"] - previous_cache_count
        previous_cache_count = int(snap["cache_files"])

        print("=" * 90)
        print(f"Time: {snap['timestamp']}")
        print(f"Python processes: {len(snap['python_processes'])}")
        for process in snap["python_processes"]:
            print(f"  {process[:240]}")
        print(f"Seeds: {snap['seed_rows']}")
        print(f"Cache files: {snap['cache_files']} | delta since last: {cache_delta} | newest: {snap['cache_newest']}")
        print(f"Candidates exists: {snap['candidate_output_exists']} | rows: {snap['candidate_rows']}")
        print(f"Rejects exists: {snap['reject_output_exists']} | rows: {snap['reject_rows']}")
        print(f"Report exists: {snap['report_exists']}")

        if args.once:
            break

        time.sleep(args.interval_seconds)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())