from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


THESIS4_CATEGORIES = {
    "api_reference",
    "configuration",
    "developer_setup",
    "model_contract",
}

TARGET_CATEGORY_ALIASES = {
    "api": "api_reference",
    "api_endpoint": "api_reference",
    "api_endpoint_change": "api_reference",
    "api_reference": "api_reference",
    "endpoint": "api_reference",
    "request_response": "api_reference",
    "request_response_change": "api_reference",

    "configuration": "configuration",
    "configuration_change": "configuration",
    "config": "configuration",
    "settings": "configuration",
    "environment": "configuration",
    "env": "configuration",

    "developer_setup": "developer_setup",
    "setup": "developer_setup",
    "installation": "developer_setup",
    "install": "developer_setup",
    "cli": "developer_setup",
    "command": "developer_setup",
    "commands": "developer_setup",
    "testing": "developer_setup",
    "testing_instructions": "developer_setup",
    "testing_command_change": "developer_setup",
    "workflow": "developer_setup",
    "workflow_change": "developer_setup",
    "workflow_documentation": "developer_setup",
    "project_documentation": "developer_setup",

    "model_contract": "model_contract",
    "model": "model_contract",
    "data_model": "model_contract",
    "request_response_schema_change": "model_contract",
    "schema": "model_contract",
    "schemas": "model_contract",
    "type": "model_contract",
    "types": "model_contract",
    "interface": "model_contract",
    "interfaces": "model_contract",
    "contract": "model_contract",
    "security": "model_contract",
}

SAFE_INPUT_FIELDS = [
    "language",
    "code_changed_files",
    "code_diff_excerpt",
    "docs_before_excerpt",
]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()

            if not stripped:
                continue

            try:
                value = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_number}: {exc}") from exc

            if not isinstance(value, dict):
                raise ValueError(f"JSONL row must be an object at {path}:{line_number}")

            rows.append(value)

    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value

    if value is None:
        return False

    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def normalize_category(value: Any) -> str | None:
    raw = str(value or "").strip().lower()

    if not raw or raw in {"no_update", "not_available", "none", "null"}:
        return None

    normalized = TARGET_CATEGORY_ALIASES.get(raw, raw)

    if normalized in THESIS4_CATEGORIES:
        return normalized

    return None


def stable_hash_float(value: str, *, seed: int) -> float:
    raw = f"{seed}:{value}".encode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()
    integer = int(digest[:16], 16)
    return integer / float(16**16 - 1)


def stable_sort_key(row: dict[str, Any], *, seed: int) -> tuple[float, str]:
    case_id = str(row.get("case_id") or "")
    repository = str(row.get("repository") or "")
    source_url = str(row.get("source_url") or "")
    key = case_id or source_url or repository or json.dumps(row, sort_keys=True)
    return stable_hash_float(key, seed=seed), key


def filter_language(rows: list[dict[str, Any]], language_filter: str | None) -> list[dict[str, Any]]:
    if not language_filter:
        return rows

    wanted = language_filter.strip().lower()

    return [
        row
        for row in rows
        if str(row.get("language") or "").strip().lower() == wanted
    ]


def prepare_category_rows(
    rows: list[dict[str, Any]],
    *,
    source_split: str,
    language_filter: str | None,
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []

    rows = filter_language(rows, language_filter)

    for row in rows:
        if not bool_value(row.get("gold_docs_update_required")):
            continue

        category = normalize_category(row.get("gold_doc_category"))
        if category is None:
            continue

        copied = dict(row)
        copied["gold_docs_update_required"] = True
        copied["gold_doc_category"] = category
        copied["category_v2_source_split"] = source_split
        copied["category_v2_label_status"] = copied.get("category_review_status") or "not_reviewed_original_label"
        output.append(copied)

    return output


def assert_unique_case_ids(rows: list[dict[str, Any]]) -> None:
    seen: set[str] = set()
    duplicates: list[str] = []

    for row in rows:
        case_id = str(row.get("case_id") or "").strip()
        if not case_id:
            raise ValueError("Every row must have a non-empty case_id.")

        if case_id in seen:
            duplicates.append(case_id)

        seen.add(case_id)

    if duplicates:
        raise ValueError(f"Duplicate case_id values found: {duplicates[:20]}")


def stratified_split(
    rows: list[dict[str, Any]],
    *,
    seed: int,
    train_ratio: float,
    validation_ratio: float,
    locked_test_ratio: float,
) -> dict[str, list[dict[str, Any]]]:
    total_ratio = train_ratio + validation_ratio + locked_test_ratio
    if abs(total_ratio - 1.0) > 1e-9:
        raise ValueError(
            f"Split ratios must sum to 1.0. Got {total_ratio}: "
            f"{train_ratio}, {validation_ratio}, {locked_test_ratio}"
        )

    grouped: dict[str, list[dict[str, Any]]] = {category: [] for category in sorted(THESIS4_CATEGORIES)}

    for row in rows:
        category = normalize_category(row.get("gold_doc_category"))
        if category is None:
            raise ValueError(f"Unexpected unsupported category in prepared row: {row.get('gold_doc_category')}")
        grouped[category].append(row)

    split_rows: dict[str, list[dict[str, Any]]] = {
        "train": [],
        "validation": [],
        "locked_test": [],
    }

    for category, category_rows in grouped.items():
        ordered = sorted(category_rows, key=lambda row: stable_sort_key(row, seed=seed))

        count = len(ordered)
        train_count = int(round(count * train_ratio))
        validation_count = int(round(count * validation_ratio))

        if train_count + validation_count > count:
            validation_count = max(0, count - train_count)

        train_part = ordered[:train_count]
        validation_part = ordered[train_count : train_count + validation_count]
        locked_part = ordered[train_count + validation_count :]

        split_rows["train"].extend(train_part)
        split_rows["validation"].extend(validation_part)
        split_rows["locked_test"].extend(locked_part)

    for split_name in split_rows:
        split_rows[split_name] = sorted(
            split_rows[split_name],
            key=lambda row: stable_sort_key(row, seed=seed + 1000),
        )

        for row in split_rows[split_name]:
            row["category_v2_split"] = split_name
            row["category_v2_seed"] = seed

    return split_rows


def summarize_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "rows": len(rows),
        "category_counts": dict(Counter(str(row.get("gold_doc_category")) for row in rows)),
        "source_split_counts": dict(Counter(str(row.get("category_v2_source_split")) for row in rows)),
        "label_status_counts": dict(Counter(str(row.get("category_v2_label_status")) for row in rows)),
        "repository_counts_top30": dict(Counter(str(row.get("repository")) for row in rows).most_common(30)),
    }


def write_protocol_md(path: Path, summary: dict[str, Any]) -> None:
    lines = [
        "# Category Reviewed Split V2 Protocol",
        "",
        "## Purpose",
        "",
        "This protocol creates a new documentation-category dataset split after train/validation label review.",
        "",
        "The goal is to improve category-label consistency without introducing rule-based routing or manual model steering.",
        "",
        "## Leakage boundary",
        "",
        "- The previous locked-test split is not used as input.",
        "- The reviewed dataset is built only from the reviewed train and validation files.",
        "- A new locked-test split is created only after labels are fixed.",
        "- The new locked-test split must be used only for final reporting under this V2 category protocol.",
        "",
        "## Model-facing fields",
        "",
    ]

    for field in SAFE_INPUT_FIELDS:
        lines.append(f"- `{field}`")

    lines.extend(
        [
            "",
            "No gold labels, manual notes, target document files, source URLs, PR titles, docs-after text, or docs diffs are model-facing fields.",
            "",
            "## Category schema",
            "",
        ]
    )

    for category in sorted(THESIS4_CATEGORIES):
        lines.append(f"- `{category}`")

    lines.extend(
        [
            "",
            "## Split summary",
            "",
            "```json",
            json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True),
            "```",
            "",
            "## Methodological interpretation",
            "",
            "This V2 split may be used as a new frozen category-classification benchmark.",
            "It should not be mixed with the older V1 locked-test result as if both were the same test set.",
            "",
            "The correct comparison is within this protocol: validation is used for model selection and V2 locked-test is used only for final reporting.",
            "",
        ]
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def run(
    *,
    reviewed_train: Path,
    reviewed_validation: Path,
    output_dir: Path,
    language_filter: str | None,
    seed: int,
    train_ratio: float,
    validation_ratio: float,
    locked_test_ratio: float,
) -> dict[str, Any]:
    train_rows_raw = load_jsonl(reviewed_train)
    validation_rows_raw = load_jsonl(reviewed_validation)

    train_rows = prepare_category_rows(
        train_rows_raw,
        source_split="reviewed_train",
        language_filter=language_filter,
    )
    validation_rows = prepare_category_rows(
        validation_rows_raw,
        source_split="reviewed_validation",
        language_filter=language_filter,
    )

    combined = train_rows + validation_rows
    assert_unique_case_ids(combined)

    split_rows = stratified_split(
        combined,
        seed=seed,
        train_ratio=train_ratio,
        validation_ratio=validation_ratio,
        locked_test_ratio=locked_test_ratio,
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    output_paths = {
        "train": output_dir / "real_pr_category_reviewed_v2_train.jsonl",
        "validation": output_dir / "real_pr_category_reviewed_v2_validation.jsonl",
        "locked_test": output_dir / "real_pr_category_reviewed_v2_locked_test.jsonl",
    }

    for split_name, path in output_paths.items():
        write_jsonl(path, split_rows[split_name])

    summary = {
        "status": "ok",
        "protocol": "category_reviewed_split_v2",
        "language_filter": language_filter,
        "seed": seed,
        "ratios": {
            "train": train_ratio,
            "validation": validation_ratio,
            "locked_test": locked_test_ratio,
        },
        "source_inputs": {
            "reviewed_train": str(reviewed_train),
            "reviewed_validation": str(reviewed_validation),
            "previous_locked_test_used": False,
        },
        "outputs": {key: str(path) for key, path in output_paths.items()},
        "combined": summarize_rows(combined),
        "splits": {
            split_name: summarize_rows(rows)
            for split_name, rows in split_rows.items()
        },
        "methodology": {
            "model_facing_fields": SAFE_INPUT_FIELDS,
            "manual_path_flags_added": False,
            "category_specific_prediction_rules_added": False,
            "target_label_review_used": True,
            "old_locked_test_excluded": True,
            "new_locked_test_policy": "final_reporting_only_after_this_split_is_frozen",
        },
    }

    write_json(output_dir / "category_reviewed_split_v2_summary.json", summary)
    write_protocol_md(output_dir / "category_reviewed_split_v2_protocol.md", summary)

    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a new frozen reviewed category split from reviewed train/validation labels."
    )
    parser.add_argument("--reviewed-train", required=True)
    parser.add_argument("--reviewed-validation", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--language-filter", default="typescript")
    parser.add_argument("--seed", type=int, default=20260824)
    parser.add_argument("--train-ratio", type=float, default=0.70)
    parser.add_argument("--validation-ratio", type=float, default=0.15)
    parser.add_argument("--locked-test-ratio", type=float, default=0.15)

    args = parser.parse_args()

    run(
        reviewed_train=Path(args.reviewed_train),
        reviewed_validation=Path(args.reviewed_validation),
        output_dir=Path(args.output_dir),
        language_filter=args.language_filter,
        seed=args.seed,
        train_ratio=args.train_ratio,
        validation_ratio=args.validation_ratio,
        locked_test_ratio=args.locked_test_ratio,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())