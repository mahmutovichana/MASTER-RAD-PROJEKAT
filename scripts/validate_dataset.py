from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DATASET_PATH = DATA_DIR / "docguard_dataset.jsonl"
SPLIT_PATHS = {
    "train": DATA_DIR / "train.jsonl",
    "validation": DATA_DIR / "validation.jsonl",
    "test": DATA_DIR / "test.jsonl",
}

REQUIRED_FIELDS = {
    "id",
    "project_id",
    "scenario_type",
    "docs_update_required",
    "change_summary",
    "changed_files",
    "code_diff",
    "docs_before_excerpt",
    "target_doc_file",
    "target_section",
    "expected_facts",
    "gold_doc_patch",
    "docs_after_gold_excerpt",
    "negative_reason",
    "difficulty",
    "tags",
}

POSITIVE_SCENARIOS = {
    "new_endpoint",
    "removed_endpoint",
    "changed_endpoint_path",
    "changed_http_method",
    "added_request_field",
    "removed_request_field",
    "changed_validation_min",
    "changed_validation_max",
    "changed_enum_values",
    "changed_auth_requirement",
    "added_response_field",
    "removed_response_field",
    "changed_status_code",
    "changed_error_response",
    "deprecated_endpoint",
}

NEGATIVE_SCENARIOS = {
    "internal_refactor",
    "rename_private_helper",
    "formatting_only",
    "test_only_change",
    "comment_only_change",
    "dependency_config_change",
    "docs_already_updated",
    "internal_service_logic_no_api_change",
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
            raise AssertionError(f"{path.relative_to(ROOT)}:{line_number} is invalid JSON: {exc}") from exc
    return records


def assert_record_shape(record: dict) -> None:
    missing = REQUIRED_FIELDS - record.keys()
    extra = record.keys() - REQUIRED_FIELDS
    if missing:
        raise AssertionError(f"{record.get('id', '<unknown>')} missing fields: {sorted(missing)}")
    if extra:
        raise AssertionError(f"{record.get('id', '<unknown>')} has extra fields: {sorted(extra)}")
    if not isinstance(record["changed_files"], list) or not record["changed_files"]:
        raise AssertionError(f"{record['id']} changed_files must be a non-empty list")
    if not isinstance(record["expected_facts"], list):
        raise AssertionError(f"{record['id']} expected_facts must be a list")
    if any(not isinstance(fact, str) or not fact.strip() for fact in record["expected_facts"]):
        raise AssertionError(f"{record['id']} expected_facts contains an empty or non-string value")
    if record["difficulty"] not in {"easy", "medium", "hard"}:
        raise AssertionError(f"{record['id']} has invalid difficulty")
    if not isinstance(record["docs_update_required"], bool):
        raise AssertionError(f"{record['id']} docs_update_required must be a boolean")
    if not isinstance(record["tags"], list) or not record["tags"]:
        raise AssertionError(f"{record['id']} tags must be a non-empty list")


def assert_label_rules(record: dict) -> None:
    scenario_type = record["scenario_type"]
    if scenario_type in POSITIVE_SCENARIOS and not record["docs_update_required"]:
        raise AssertionError(f"{record['id']} positive scenario has negative label: {scenario_type}")
    if scenario_type in NEGATIVE_SCENARIOS and record["docs_update_required"]:
        raise AssertionError(f"{record['id']} negative scenario has positive label: {scenario_type}")
    if scenario_type not in POSITIVE_SCENARIOS | NEGATIVE_SCENARIOS:
        raise AssertionError(f"{record['id']} has unknown scenario_type: {scenario_type}")

    if record["docs_update_required"]:
        if not record["expected_facts"]:
            raise AssertionError(f"{record['id']} positive record has no expected_facts")
        if len(set(record["expected_facts"])) != len(record["expected_facts"]):
            raise AssertionError(f"{record['id']} positive record has duplicate expected_facts")
        if not record["gold_doc_patch"]:
            raise AssertionError(f"{record['id']} positive record has no gold_doc_patch")
        if record["negative_reason"] not in (None, ""):
            raise AssertionError(f"{record['id']} positive record should not include negative_reason")
    else:
        if record["expected_facts"]:
            raise AssertionError(f"{record['id']} negative record should not include expected_facts")
        if record["gold_doc_patch"] not in (None, ""):
            raise AssertionError(f"{record['id']} negative record has a gold_doc_patch")
        if not record["negative_reason"]:
            raise AssertionError(f"{record['id']} negative record has no negative_reason")
        if record["docs_after_gold_excerpt"] != record["docs_before_excerpt"]:
            raise AssertionError(f"{record['id']} negative record should not change docs_after_gold_excerpt")


def assert_changed_files_exist(record: dict) -> None:
    project_root = ROOT / "generated_projects" / record["project_id"]
    for changed_file in record["changed_files"]:
        if changed_file.startswith("docs/"):
            candidate = project_root / changed_file
        else:
            candidate = project_root / changed_file
        if not candidate.exists():
            raise AssertionError(f"{record['id']} references missing changed file: {changed_file}")


def assert_target_doc_exists(record: dict) -> None:
    target = ROOT / "generated_projects" / record["project_id"] / record["target_doc_file"]
    if not target.exists():
        raise AssertionError(f"{record['id']} references missing target_doc_file: {record['target_doc_file']}")


def assert_no_duplicate_ids(records: list[dict]) -> None:
    seen = set()
    for record in records:
        if record["id"] in seen:
            raise AssertionError(f"Duplicate dataset id: {record['id']}")
        seen.add(record["id"])


def semantic_fingerprint(record: dict) -> str:
    comparable = {
        key: value
        for key, value in record.items()
        if key not in {"id"}
    }
    return json.dumps(comparable, sort_keys=True, ensure_ascii=False)


def assert_no_duplicate_records(records: list[dict]) -> None:
    seen: dict[str, str] = {}
    for record in records:
        fingerprint = semantic_fingerprint(record)
        if fingerprint in seen:
            raise AssertionError(
                f"Duplicate semantic record: {seen[fingerprint]} and {record['id']} "
                "only differ by id"
            )
        seen[fingerprint] = record["id"]


def near_duplicate_fingerprint(record: dict) -> str:
    comparable = {
        key: value
        for key, value in record.items()
        if key not in {"id", "difficulty", "tags"}
    }
    text = json.dumps(comparable, sort_keys=True, ensure_ascii=False).lower()
    text = re.sub(r"\b\d+\b", "<num>", text)
    text = re.sub(r"(code|field|number|token|access|details|summary|history|status|metrics|owner|timeline|attachments|eligibility)<num>", r"\1<num>", text)
    return text


def assert_no_near_duplicate_records(records: list[dict]) -> None:
    seen: dict[str, str] = {}
    for record in records:
        fingerprint = near_duplicate_fingerprint(record)
        if fingerprint in seen:
            raise AssertionError(
                f"Near-duplicate record detected: {seen[fingerprint]} and {record['id']} "
                "share the same normalized contract change"
            )
        seen[fingerprint] = record["id"]


def added_patch_lines(gold_doc_patch: str) -> list[str]:
    lines = []
    for line in gold_doc_patch.splitlines():
        if line.startswith("+++") or not line.startswith("+"):
            continue
        text = line[1:].strip()
        if text:
            lines.append(text)
    return lines


def assert_gold_patch_consistency(record: dict) -> None:
    patch = record["gold_doc_patch"]
    if not record["docs_update_required"]:
        return

    if not isinstance(patch, str) or not patch.strip():
        raise AssertionError(f"{record['id']} positive record has invalid gold_doc_patch")
    if "@@" not in patch:
        raise AssertionError(f"{record['id']} gold_doc_patch must include a hunk header")
    if record["target_section"] not in patch:
        raise AssertionError(f"{record['id']} gold_doc_patch does not mention target_section")
    if record["docs_after_gold_excerpt"] == record["docs_before_excerpt"]:
        raise AssertionError(f"{record['id']} positive record has unchanged docs_after_gold_excerpt")

    additions = added_patch_lines(patch)
    if not additions:
        raise AssertionError(f"{record['id']} gold_doc_patch has no added documentation lines")
    if len(patch.splitlines()) > 30:
        raise AssertionError(f"{record['id']} gold_doc_patch is too large to be minimal")

    after_excerpt = record["docs_after_gold_excerpt"]
    before_excerpt = record["docs_before_excerpt"]
    if not any(addition in after_excerpt for addition in additions):
        raise AssertionError(f"{record['id']} gold_doc_patch additions are not reflected in docs_after_gold_excerpt")
    if all(addition in before_excerpt for addition in additions):
        raise AssertionError(f"{record['id']} gold_doc_patch appears to add only text already present before the change")


def assert_expected_facts_are_useful(record: dict) -> None:
    if not record["docs_update_required"]:
        return
    searchable_text = " ".join(
        [
            record["change_summary"],
            record["code_diff"],
            record["gold_doc_patch"] or "",
            record["docs_after_gold_excerpt"],
        ]
    ).lower()
    for fact in record["expected_facts"]:
        tokens = [
            token
            for token in fact.lower().replace("`", "").replace("/", " ").replace(":", " ").split()
            if len(token) >= 3
        ]
        if tokens and not any(token in searchable_text for token in tokens):
            raise AssertionError(f"{record['id']} expected_fact is not grounded in code or gold docs: {fact}")


def assert_split_integrity(dataset_records: list[dict]) -> None:
    dataset_by_id = {record["id"]: record for record in dataset_records}
    dataset_ids = set(dataset_by_id)
    split_projects: dict[str, set[str]] = {}
    split_ids: set[str] = set()
    project_to_split: dict[str, str] = {}

    for split_name, path in SPLIT_PATHS.items():
        records = read_jsonl(path)
        split_projects[split_name] = {record["project_id"] for record in records}
        for record in records:
            if record["id"] not in dataset_ids:
                raise AssertionError(f"{split_name} contains id not present in dataset: {record['id']}")
            if record["id"] in split_ids:
                raise AssertionError(f"Record appears in multiple splits: {record['id']}")
            if semantic_fingerprint(record) != semantic_fingerprint(dataset_by_id[record["id"]]):
                raise AssertionError(f"{split_name} copy differs from full dataset for id: {record['id']}")
            split_ids.add(record["id"])
            previous_split = project_to_split.setdefault(record["project_id"], split_name)
            if previous_split != split_name:
                raise AssertionError(
                    f"Project {record['project_id']} appears in both {previous_split} and {split_name}"
                )

    if split_ids != dataset_ids:
        missing = sorted(dataset_ids - split_ids)
        extra = sorted(split_ids - dataset_ids)
        raise AssertionError(f"Split ids do not match dataset. Missing={missing}, extra={extra}")

    split_names = list(split_projects)
    for index, left in enumerate(split_names):
        for right in split_names[index + 1 :]:
            overlap = split_projects[left] & split_projects[right]
            if overlap:
                raise AssertionError(f"Project-level split leakage between {left} and {right}: {sorted(overlap)}")


def main() -> int:
    records = read_jsonl(DATASET_PATH)
    if len(records) < 1500:
        raise AssertionError(f"Expected at least 1500 records, found {len(records)}")

    assert_no_duplicate_ids(records)
    assert_no_duplicate_records(records)
    assert_no_near_duplicate_records(records)
    for record in records:
        assert_record_shape(record)
        assert_label_rules(record)
        assert_expected_facts_are_useful(record)
        assert_gold_patch_consistency(record)
        assert_changed_files_exist(record)
        assert_target_doc_exists(record)

    assert_split_integrity(records)
    print(
        f"Dataset validation passed: {len(records)} records, "
        "no duplicate or near-duplicate records, labels consistent, "
        "gold patches consistent, no split leakage."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"Dataset validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
