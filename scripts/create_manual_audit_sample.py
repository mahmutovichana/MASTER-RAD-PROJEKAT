from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT / "data" / "docguard_dataset.jsonl"
OUTPUT_PATH = ROOT / "reports" / "manual_audit_sample.jsonl"

SCENARIO_TYPES = [
    "new_endpoint",
    "changed_validation_min",
    "changed_auth_requirement",
    "added_response_field",
    "internal_refactor",
]
RECORDS_PER_SCENARIO = 10


def read_jsonl(path: Path) -> list[dict]:
    records = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number} is invalid JSON: {exc}") from exc
    return records


def select_records(records: list[dict]) -> list[dict]:
    by_scenario: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        by_scenario[record["scenario_type"]].append(record)

    selected: list[dict] = []
    for scenario_type in SCENARIO_TYPES:
        candidates = by_scenario[scenario_type]
        if len(candidates) < RECORDS_PER_SCENARIO:
            raise ValueError(
                f"Need {RECORDS_PER_SCENARIO} records for {scenario_type}, found {len(candidates)}"
            )

        project_buckets: dict[str, list[dict]] = defaultdict(list)
        for record in candidates:
            project_buckets[record["project_id"]].append(record)

        scenario_selection: list[dict] = []
        project_ids = sorted(project_buckets)
        while len(scenario_selection) < RECORDS_PER_SCENARIO:
            made_progress = False
            for project_id in project_ids:
                bucket = project_buckets[project_id]
                if bucket:
                    scenario_selection.append(bucket.pop(0))
                    made_progress = True
                    if len(scenario_selection) == RECORDS_PER_SCENARIO:
                        break
            if not made_progress:
                break

        selected.extend(scenario_selection)

    return selected


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    records = read_jsonl(DATASET_PATH)
    selected = select_records(records)
    write_jsonl(OUTPUT_PATH, selected)

    counts = Counter(record["scenario_type"] for record in selected)
    print(f"Wrote {len(selected)} records to {OUTPUT_PATH.relative_to(ROOT)}")
    for scenario_type in SCENARIO_TYPES:
        print(f"{scenario_type}: {counts[scenario_type]}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Failed to create manual audit sample: {exc}", file=sys.stderr)
        raise SystemExit(1)
