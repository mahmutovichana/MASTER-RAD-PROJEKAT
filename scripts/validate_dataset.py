from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DATASET_PATH = DATA_DIR / "docguard_dataset.jsonl"
SPLIT_PATHS = {"train": DATA_DIR / "train.jsonl", "validation": DATA_DIR / "validation.jsonl", "test": DATA_DIR / "test.jsonl"}

REQUIRED_FIELDS = {
    "id", "project_id", "scenario_type", "docs_update_required", "change_summary", "changed_files", "code_diff",
    "docs_before_excerpt", "target_doc_file", "target_section", "expected_facts", "gold_doc_patch",
    "docs_after_gold_excerpt", "negative_reason", "difficulty", "tags", "doc_category", "change_level",
    "affected_documentation_files", "primary_documentation_reason", "change_intent_summary",
}

DOC_CATEGORIES = {
    "api_reference", "architecture_flow", "model_contract", "developer_setup", "testing_instructions",
    "configuration", "workflow_documentation", "changelog",
}
CHANGE_LEVELS = {"low", "medium", "high"}
POSITIVE_SCENARIOS = {
    "new_endpoint", "removed_endpoint", "changed_endpoint_path", "changed_http_method", "added_request_field",
    "removed_request_field", "changed_validation_min", "changed_validation_max", "changed_enum_values",
    "changed_auth_requirement", "added_response_field", "changed_status_code", "changed_error_response",
    "deprecated_endpoint", "added_middleware_flow", "changed_auth_flow", "added_dto_model",
    "changed_dto_field_semantics", "changed_run_command", "changed_test_command", "added_environment_variable",
    "changed_local_development_flow", "added_background_job_flow", "changed_error_handling_flow",
    "added_service_orchestration_flow", "changed_caching_or_rate_limit_flow",
}
NEGATIVE_SCENARIOS = {
    "internal_refactor", "rename_private_helper", "formatting_only", "test_only_change", "comment_only_change",
    "dependency_config_change", "docs_already_updated", "internal_service_logic_no_api_change",
    "internal_variable_rename_no_behavior_change", "private_helper_refactor_no_flow_change",
    "formatting_only_in_docs_or_code", "dev_dependency_patch_no_command_change",
    "test_assertion_refactor_no_behavior_change", "comments_reworded_no_contract_change",
    "log_message_change_no_user_visible_behavior", "internal_performance_refactor_no_documented_behavior_change",
}


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        raise AssertionError(f"Missing file: {path.relative_to(ROOT)}")
    records = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise AssertionError(f"{path.relative_to(ROOT)}:{line_number} invalid JSON: {exc}") from exc
    return records


def fingerprint(record: dict) -> str:
    return json.dumps({k: v for k, v in record.items() if k != "id"}, sort_keys=True, ensure_ascii=False)


def assert_shape(record: dict) -> None:
    missing = REQUIRED_FIELDS - set(record)
    extra = set(record) - REQUIRED_FIELDS
    if missing:
        raise AssertionError(f"{record.get('id', '<unknown>')} missing fields: {sorted(missing)}")
    if extra:
        raise AssertionError(f"{record['id']} has extra fields: {sorted(extra)}")
    if record["doc_category"] not in DOC_CATEGORIES:
        raise AssertionError(f"{record['id']} invalid doc_category")
    if record["change_level"] not in CHANGE_LEVELS:
        raise AssertionError(f"{record['id']} invalid change_level")
    for field in ["changed_files", "tags", "affected_documentation_files"]:
        if not isinstance(record[field], list) or not record[field]:
            raise AssertionError(f"{record['id']} {field} must be a non-empty list")
    if not isinstance(record["expected_facts"], list):
        raise AssertionError(f"{record['id']} expected_facts must be a list")


def assert_label_rules(record: dict) -> None:
    scenario = record["scenario_type"]
    if scenario not in POSITIVE_SCENARIOS | NEGATIVE_SCENARIOS:
        raise AssertionError(f"{record['id']} unknown scenario_type: {scenario}")
    if scenario in POSITIVE_SCENARIOS and not record["docs_update_required"]:
        raise AssertionError(f"{record['id']} positive scenario has negative label")
    if scenario in NEGATIVE_SCENARIOS and record["docs_update_required"]:
        raise AssertionError(f"{record['id']} negative scenario has positive label")
    if record["docs_update_required"]:
        if not record["expected_facts"]:
            raise AssertionError(f"{record['id']} positive record has no expected_facts")
        if not record["gold_doc_patch"]:
            raise AssertionError(f"{record['id']} positive record has no gold_doc_patch")
        if record["negative_reason"] not in (None, ""):
            raise AssertionError(f"{record['id']} positive record has negative_reason")
        if "@@" not in record["gold_doc_patch"] or record["target_section"] not in record["gold_doc_patch"]:
            raise AssertionError(f"{record['id']} gold patch lacks hunk or target section")
        if record["docs_after_gold_excerpt"] == record["docs_before_excerpt"]:
            raise AssertionError(f"{record['id']} positive after excerpt did not change")
    else:
        if record["expected_facts"]:
            raise AssertionError(f"{record['id']} negative record has expected_facts")
        if record["gold_doc_patch"] not in (None, ""):
            raise AssertionError(f"{record['id']} negative record has gold patch")
        if not record["negative_reason"]:
            raise AssertionError(f"{record['id']} negative record has no reason")
        if record["docs_after_gold_excerpt"] != record["docs_before_excerpt"]:
            raise AssertionError(f"{record['id']} negative docs_after differs")


def assert_files(record: dict) -> None:
    project_root = ROOT / "generated_projects" / record["project_id"]
    for changed_file in record["changed_files"]:
        if not (project_root / changed_file).exists():
            raise AssertionError(f"{record['id']} missing changed file: {changed_file}")
    for doc_file in set(record["affected_documentation_files"] + [record["target_doc_file"]]):
        if not (project_root / doc_file).exists():
            raise AssertionError(f"{record['id']} missing documentation file: {doc_file}")


def assert_splits(dataset_records: list[dict]) -> None:
    by_id = {record["id"]: record for record in dataset_records}
    seen_ids: set[str] = set()
    project_split: dict[str, str] = {}
    for split, path in SPLIT_PATHS.items():
        for record in read_jsonl(path):
            if record["id"] not in by_id:
                raise AssertionError(f"{split} contains unknown id {record['id']}")
            if record["id"] in seen_ids:
                raise AssertionError(f"{record['id']} appears in multiple splits")
            if fingerprint(record) != fingerprint(by_id[record["id"]]):
                raise AssertionError(f"{record['id']} differs between split and dataset")
            seen_ids.add(record["id"])
            previous = project_split.setdefault(record["project_id"], split)
            if previous != split:
                raise AssertionError(f"Project {record['project_id']} leaks between splits")
    if seen_ids != set(by_id):
        raise AssertionError("Split records do not exactly match dataset records")


def main() -> int:
    records = read_jsonl(DATASET_PATH)
    if len(records) < 2500:
        raise AssertionError(f"Expected at least 2500 records, found {len(records)}")
    ids = [record["id"] for record in records]
    if len(ids) != len(set(ids)):
        raise AssertionError("Duplicate ids exist")
    seen = {}
    for record in records:
        fp = fingerprint(record)
        if fp in seen:
            raise AssertionError(f"Duplicate semantic record: {seen[fp]} and {record['id']}")
        seen[fp] = record["id"]
        assert_shape(record)
        assert_label_rules(record)
        assert_files(record)
    assert_splits(records)
    print(f"Dataset validation passed: {len(records)} v0.3 records, labels consistent, documentation targets valid, no split leakage.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"Dataset validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
