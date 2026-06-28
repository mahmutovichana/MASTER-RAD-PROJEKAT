from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
PROJECTS_DIR = ROOT / "generated_projects"
SPLIT_PATHS = {split: DATA_DIR / f"{split}.jsonl" for split in ["train", "validation", "test"]}

DOC_FILES = {
    "docs/api.md",
    "docs/architecture.md",
    "docs/models.md",
    "docs/developer-setup.md",
    "docs/testing.md",
    "docs/configuration.md",
    "docs/workflows.md",
    "CHANGELOG.md",
}
DOC_CATEGORIES_V04 = {
    "api_reference",
    "architecture_flow",
    "model_contract",
    "developer_setup",
    "testing_instructions",
    "configuration",
    "workflow_documentation",
    "changelog",
    "no_update",
}
REQUIRED_FIELDS = {
    "id", "project_id", "split", "scenario_type", "docs_update_required", "change_summary", "changed_files",
    "code_diff", "docs_before_excerpt", "target_doc_file", "target_section", "expected_facts",
    "gold_doc_patch", "generated_doc_patch", "docs_after_gold_excerpt", "negative_reason", "difficulty",
    "tags", "doc_category", "change_level", "affected_documentation_files", "primary_documentation_reason",
    "change_intent_summary",
}


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        raise AssertionError(f"Missing file: {path.relative_to(ROOT)}")
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise AssertionError(f"{path.relative_to(ROOT)}:{line_number} invalid JSON: {exc}") from exc
    return rows


def fingerprint(record: dict) -> str:
    return json.dumps({k: v for k, v in record.items() if k != "id"}, sort_keys=True, ensure_ascii=False)


def assert_shape(record: dict) -> None:
    missing = REQUIRED_FIELDS - set(record)
    if missing:
        raise AssertionError(f"{record.get('id', '<unknown>')} missing fields: {sorted(missing)}")
    if record["doc_category"] not in DOC_CATEGORIES_V04:
        raise AssertionError(f"{record['id']} invalid doc_category: {record['doc_category']}")
    if not isinstance(record["changed_files"], list) or not record["changed_files"]:
        raise AssertionError(f"{record['id']} changed_files must be non-empty")
    for field in ["expected_facts", "tags", "affected_documentation_files"]:
        if not isinstance(record[field], list):
            raise AssertionError(f"{record['id']} {field} must be a list")


def assert_label_rules(record: dict) -> None:
    if record["docs_update_required"]:
        if record["doc_category"] == "no_update":
            raise AssertionError(f"{record['id']} positive record has no_update category")
        if record["target_doc_file"] not in DOC_FILES:
            raise AssertionError(f"{record['id']} positive record has invalid target_doc_file")
        if not record["target_section"]:
            raise AssertionError(f"{record['id']} positive record has empty target_section")
        if not record["gold_doc_patch"] or not record["generated_doc_patch"]:
            raise AssertionError(f"{record['id']} positive record lacks patch")
        if not record["expected_facts"]:
            raise AssertionError(f"{record['id']} positive record lacks expected_facts")
        if record["negative_reason"] is not None:
            raise AssertionError(f"{record['id']} positive record has negative_reason")
    else:
        if record["doc_category"] != "no_update":
            raise AssertionError(f"{record['id']} negative record category must be no_update")
        if record["target_doc_file"] not in (None, ""):
            raise AssertionError(f"{record['id']} negative target_doc_file must be empty")
        if record["target_section"] != "":
            raise AssertionError(f"{record['id']} negative target_section must be empty")
        if record["gold_doc_patch"] is not None or record["generated_doc_patch"] is not None:
            raise AssertionError(f"{record['id']} negative patch must be null")
        if record["expected_facts"]:
            raise AssertionError(f"{record['id']} negative expected_facts must be empty")
        if not record["negative_reason"]:
            raise AssertionError(f"{record['id']} negative_reason must be non-empty")


def assert_files(record: dict) -> None:
    project_root = PROJECTS_DIR / record["project_id"]
    for changed_file in record["changed_files"]:
        if not (project_root / changed_file).exists():
            raise AssertionError(f"{record['id']} missing changed file: {changed_file}")
    if record["docs_update_required"]:
        if not (project_root / record["target_doc_file"]).exists():
            raise AssertionError(f"{record['id']} missing target doc file: {record['target_doc_file']}")
    for doc_file in record["affected_documentation_files"]:
        if doc_file not in DOC_FILES:
            raise AssertionError(f"{record['id']} invalid affected doc file: {doc_file}")
        if not (project_root / doc_file).exists():
            raise AssertionError(f"{record['id']} missing affected doc file: {doc_file}")


def assert_splits(records: list[dict]) -> None:
    by_id = {record["id"]: record for record in records}
    seen_ids: set[str] = set()
    project_split: dict[str, str] = {}
    for split, path in SPLIT_PATHS.items():
        rows = read_jsonl(path)
        for record in rows:
            if record["id"] not in by_id:
                raise AssertionError(f"{split} contains unknown id {record['id']}")
            if record["id"] in seen_ids:
                raise AssertionError(f"{record['id']} appears in multiple splits")
            if fingerprint(record) != fingerprint(by_id[record["id"]]):
                raise AssertionError(f"{record['id']} differs between split and dataset")
            if record.get("split") != split:
                raise AssertionError(f"{record['id']} has split field {record.get('split')} but is in {split}")
            seen_ids.add(record["id"])
            previous = project_split.setdefault(record["project_id"], split)
            if previous != split:
                raise AssertionError(f"Project {record['project_id']} leaks between splits")
    if seen_ids != set(by_id):
        raise AssertionError("Split records do not exactly match dataset records")


def assert_distribution(records: list[dict]) -> None:
    if len(records) != 6000:
        raise AssertionError(f"Expected 6000 v0.4 records, found {len(records)}")
    labels = Counter(bool(r["docs_update_required"]) for r in records)
    if labels[True] != labels[False]:
        raise AssertionError(f"Expected 50/50 labels, got {labels}")
    scenario_counts = Counter(r["scenario_type"] for r in records)
    too_small = {scenario: count for scenario, count in scenario_counts.items() if count < 80}
    if too_small:
        raise AssertionError(f"Scenarios below 80 examples: {too_small}")


def validate_v0_4() -> None:
    records = read_jsonl(DATA_DIR / "docguard_dataset.jsonl")
    ids = [record["id"] for record in records]
    if len(ids) != len(set(ids)):
        raise AssertionError("Duplicate ids exist")
    seen: dict[str, str] = {}
    for record in records:
        fp = fingerprint(record)
        if fp in seen:
            raise AssertionError(f"Duplicate semantic record: {seen[fp]} and {record['id']}")
        seen[fp] = record["id"]
        assert_shape(record)
        assert_label_rules(record)
        assert_files(record)
    assert_distribution(records)
    assert_splits(records)
    print("Dataset validation passed: 6000 v0.4 records, balanced labels, negative schema valid, no split leakage.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", default="v0_4", choices=["v0_4"])
    parser.parse_args()
    validate_v0_4()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"Dataset validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
