from __future__ import annotations

import difflib
import json
import random
from collections import Counter
from pathlib import Path
from typing import Any

from docguard_external.schema import ExternalDocGuardRecord


REPORTS_DIR = Path(__file__).resolve().parents[1] / "reports"
RAW_REQUIRED_FIELDS = {"id", "label", "old_code_raw", "new_code_raw", "old_comment_raw", "new_comment_raw"}
EVALUATED_SUBSETS = {"Return", "Summary"}
LABEL_POLARITY_STATUS = "plausible_manual_verification_needed"


def read_raw_json(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return [row for row in data if isinstance(row, dict)]
    if isinstance(data, dict):
        return [row for row in data.values() if isinstance(row, dict)]
    return []


def raw_data_files(data_dir: Path) -> list[Path]:
    return [
        path
        for path in sorted(data_dir.rglob("*.json"))
        if "resources" not in {part.lower() for part in path.parts}
    ]


def subset_for(path: Path, data_dir: Path) -> str:
    try:
        rel = path.relative_to(data_dir)
        return rel.parts[0] if len(rel.parts) > 1 else "unknown"
    except ValueError:
        return path.parent.name or "unknown"


def split_for(path: Path) -> str:
    stem = path.stem.lower()
    if stem in {"valid", "validation", "dev"}:
        return "validation"
    return stem


def label_to_bool(value: Any) -> bool | None:
    text = str(value).strip().lower()
    if text in {"1", "true", "inconsistent", "outdated", "yes"}:
        return True
    if text in {"0", "false", "consistent", "up_to_date", "no"}:
        return False
    return None


def build_diff(before: str, after: str, fromfile: str, tofile: str) -> str:
    return "\n".join(difflib.unified_diff(str(before).splitlines(), str(after).splitlines(), fromfile=fromfile, tofile=tofile, lineterm=""))


def normalize_record(row: dict[str, Any], source_file: Path, data_dir: Path) -> dict[str, Any] | None:
    mapped = label_to_bool(row.get("label"))
    if mapped is None or not RAW_REQUIRED_FIELDS <= set(row):
        return None
    subset = subset_for(source_file, data_dir)
    split = split_for(source_file)
    old_code = str(row.get("old_code_raw") or "")
    new_code = str(row.get("new_code_raw") or "")
    old_comment = str(row.get("old_comment_raw") or "")
    new_comment = str(row.get("new_comment_raw") or "")
    record = ExternalDocGuardRecord(
        record_id=f"deep-jit-{row.get('id')}".replace("/", "_").replace("\\", "_"),
        source_dataset="deep_jit_inconsistency",
        repository=str(row.get("id", "")).split("-")[0] if row.get("id") else None,
        commit_hash=None,
        language="java",
        code_before=old_code,
        code_after=new_code,
        code_diff=build_diff(old_code, new_code, "old_code", "new_code"),
        doc_before=old_comment,
        doc_after=new_comment,
        doc_diff=build_diff(old_comment, new_comment, "old_comment", "new_comment"),
        docs_update_required=mapped,
        label_source="strong_external_inconsistent_comment" if mapped else "strong_external_consistent_comment",
        target_kind="comment_or_docstring",
        target_path=None,
        scenario_type="external_comment_inconsistency" if mapped else "external_comment_consistent_no_update",
        split=split,
        metadata={
            "subset": subset,
            "source_file": str(source_file),
            "source_record_id": row.get("id"),
            "raw_label": row.get("label"),
            "comment_type": row.get("comment_type"),
            "label_polarity_status": LABEL_POLARITY_STATUS,
        },
    ).to_dict()
    record.update(
        {
            "subset": subset,
            "raw_label": row.get("label"),
            "old_code_raw": old_code,
            "new_code_raw": new_code,
            "old_comment_raw": old_comment,
            "new_comment_raw": new_comment,
        }
    )
    return record


def file_summary(path: Path, data_dir: Path) -> dict[str, Any]:
    rows = read_raw_json(path)
    labels = Counter(str(row.get("label")) for row in rows if isinstance(row, dict))
    key_sample = sorted({str(key) for row in rows[:20] for key in row})
    return {
        "path": str(path),
        "subset": subset_for(path, data_dir),
        "split": split_for(path),
        "records": len(rows),
        "label_distribution": dict(labels),
        "fields": key_sample,
        "has_required_fields": all(RAW_REQUIRED_FIELDS <= set(row) for row in rows[: min(20, len(rows))]) if rows else False,
        "balanced_labels": len(labels) == 2 and len(set(labels.values())) == 1,
    }


def inspect_splits(data_dir: Path) -> dict[str, Any]:
    files = raw_data_files(data_dir)
    summaries = [file_summary(path, data_dir) for path in files]
    split_by_subset: dict[str, set[str]] = {}
    for summary in summaries:
        split_by_subset.setdefault(summary["subset"], set()).add(summary["split"])
    return {
        "status": "ok" if data_dir.exists() else "error",
        "data_dir": str(data_dir),
        "files": summaries,
        "split_by_subset": {key: sorted(value) for key, value in sorted(split_by_subset.items())},
        "label_polarity_status": LABEL_POLARITY_STATUS,
    }


def write_split_audit(result: dict[str, Any]) -> None:
    REPORTS_DIR.mkdir(exist_ok=True)
    path = REPORTS_DIR / "external_deep_jit_split_audit_2026_08.md"
    lines = [
        "# External Deep-JIT Split Audit 2026-08",
        "",
        f"- Data directory: `{result.get('data_dir')}`",
        f"- Status: `{result.get('status')}`",
        f"- Label polarity status: `{result.get('label_polarity_status')}`",
        "",
        "## Available Files",
        "",
        "| File | Subset | Split | Records | Label distribution | Balanced | Required fields |",
        "| --- | --- | --- | ---: | --- | --- | --- |",
    ]
    for summary in result.get("files", []):
        lines.append(
            f"| `{summary['path']}` | `{summary['subset']}` | `{summary['split']}` | {summary['records']} | "
            f"`{summary['label_distribution']}` | `{summary['balanced_labels']}` | `{summary['has_required_fields']}` |"
        )
    lines.extend(
        [
            "",
            "## Split Availability",
            "",
            *[f"- `{subset}`: {', '.join(f'`{split}`' for split in splits)}" for subset, splits in result.get("split_by_subset", {}).items()],
            "",
            "## Evaluation Policy",
            "",
            "Return and Summary should be evaluated both separately and combined because they represent different comment types and both have test files. Return has train/validation/test. Summary has train/test but no validation file. Param has train only and is excluded from the normalized classifier benchmark to avoid introducing a train-only subset without validation/test coverage.",
            "",
            "The normalized benchmark uses original splits where available. It does not randomly mix train and test.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def split_audit(data_dir: Path) -> dict[str, Any]:
    if not data_dir.exists():
        result = {"status": "error", "data_dir": str(data_dir), "files": [], "split_by_subset": {}, "label_polarity_status": "unclear"}
    else:
        result = inspect_splits(data_dir)
    write_split_audit(result)
    result["report"] = str(REPORTS_DIR / "external_deep_jit_split_audit_2026_08.md")
    return result


def export_normalized(data_dir: Path, output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    records_by_split: dict[str, list[dict[str, Any]]] = {"train": [], "validation": [], "test": []}
    skipped_files: list[str] = []
    for path in raw_data_files(data_dir):
        subset = subset_for(path, data_dir)
        split = split_for(path)
        if subset not in EVALUATED_SUBSETS or split not in records_by_split:
            skipped_files.append(str(path))
            continue
        for row in read_raw_json(path):
            record = normalize_record(row, path, data_dir)
            if record is not None:
                records_by_split[split].append(record)
    written = {}
    for split, records in records_by_split.items():
        out = output_dir / f"{split}.jsonl"
        out.write_text("\n".join(json.dumps(row, ensure_ascii=True) for row in records) + ("\n" if records else ""), encoding="utf-8")
        written[split] = {"path": str(out), "records": len(records), "label_distribution": dict(Counter(str(row["docs_update_required"]) for row in records))}
    result = {
        "status": "ok",
        "data_dir": str(data_dir),
        "output_dir": str(output_dir),
        "written": written,
        "skipped_files": skipped_files,
        "label_polarity_status": LABEL_POLARITY_STATUS,
    }
    write_export_report(result)
    return result


def export_combined_validation(data_dir: Path, output_dir: Path, seed: int = 42, summary_validation_per_label: int = 420) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    records_by_split: dict[str, list[dict[str, Any]]] = {"train": [], "validation": [], "test": []}
    summary_train_by_label: dict[bool, list[dict[str, Any]]] = {True: [], False: []}
    skipped_files: list[str] = []
    summary_test_source_count = 0
    for path in raw_data_files(data_dir):
        subset = subset_for(path, data_dir)
        split = split_for(path)
        if subset == "Param":
            skipped_files.append(str(path))
            continue
        if subset not in EVALUATED_SUBSETS or split not in records_by_split:
            skipped_files.append(str(path))
            continue
        normalized = [record for row in read_raw_json(path) if (record := normalize_record(row, path, data_dir)) is not None]
        if subset == "Summary" and split == "train":
            for record in normalized:
                summary_train_by_label[bool(record["docs_update_required"])].append(record)
            continue
        if subset == "Summary" and split == "test":
            summary_test_source_count = len(normalized)
        records_by_split[split].extend(normalized)
    rng = random.Random(seed)
    carve_out: list[dict[str, Any]] = []
    remaining_summary_train: list[dict[str, Any]] = []
    for label_value, records in summary_train_by_label.items():
        ordered = sorted(records, key=lambda row: row["record_id"])
        selected_ids = {row["record_id"] for row in rng.sample(ordered, min(summary_validation_per_label, len(ordered)))}
        for record in ordered:
            if record["record_id"] in selected_ids:
                record = dict(record)
                record["split"] = "validation"
                record["metadata"] = dict(record.get("metadata") or {})
                record["metadata"]["validation_carve_out"] = "summary_train_seed_42_balanced"
                carve_out.append(record)
            else:
                remaining_summary_train.append(record)
    records_by_split["train"].extend(remaining_summary_train)
    records_by_split["validation"].extend(sorted(carve_out, key=lambda row: row["record_id"]))
    written = {}
    for split, records in records_by_split.items():
        records = sorted(records, key=lambda row: (str(row.get("subset")), str(row.get("record_id"))))
        out = output_dir / f"{split}.jsonl"
        out.write_text("\n".join(json.dumps(row, ensure_ascii=True) for row in records) + ("\n" if records else ""), encoding="utf-8")
        written[split] = {
            "path": str(out),
            "records": len(records),
            "label_distribution": dict(Counter(str(row["docs_update_required"]) for row in records)),
            "subset_distribution": dict(Counter(str(row.get("subset") or (row.get("metadata") or {}).get("subset")) for row in records)),
        }
    result = {
        "status": "ok",
        "data_dir": str(data_dir),
        "output_dir": str(output_dir),
        "seed": seed,
        "summary_validation_per_label": summary_validation_per_label,
        "written": written,
        "skipped_files": skipped_files,
        "summary_validation_source": "Summary/train.json",
        "summary_test_source": "Summary/test.json",
        "summary_test_records_preserved": summary_test_source_count,
        "label_polarity_status": LABEL_POLARITY_STATUS,
    }
    write_combined_validation_split_audit(result)
    return result


def write_combined_validation_split_audit(result: dict[str, Any]) -> None:
    REPORTS_DIR.mkdir(exist_ok=True)
    path = REPORTS_DIR / "external_deep_jit_combined_validation_split_audit_2026_08.md"
    lines = [
        "# External Deep-JIT Combined-Validation Split Audit 2026-08",
        "",
        "## Reason",
        "",
        "The previous Deep-JIT model-selection setup used Return validation only while the combined test set contained Return and Summary. This robustness export adds a deterministic balanced Summary validation carve-out from Summary train while keeping Summary test untouched.",
        "",
        "## Old Split Setup",
        "",
        "- Train: Return train + Summary train",
        "- Validation: Return validation only",
        "- Test: Return test + Summary test",
        "- Param: excluded/audit-only",
        "",
        "## New Split Setup",
        "",
        f"- Seed: `{result['seed']}`",
        f"- Summary validation carve-out: `{result['summary_validation_per_label']}` positive + `{result['summary_validation_per_label']}` negative from Summary train",
        "- Return train/validation/test preserved exactly as before.",
        "- Summary test preserved untouched.",
        "- Param remains excluded/audit-only.",
        "",
        "## Written Files",
        "",
        "| Split | Path | Records | Label distribution | Subset distribution |",
        "| --- | --- | ---: | --- | --- |",
    ]
    for split, info in result["written"].items():
        lines.append(
            f"| `{split}` | `{info['path']}` | {info['records']} | `{info['label_distribution']}` | `{info['subset_distribution']}` |"
        )
    lines.extend(
        [
            "",
            "## Confirmations",
            "",
            f"- Summary validation came only from `{result['summary_validation_source']}`.",
            f"- Summary test source `{result['summary_test_source']}` remains untouched with `{result['summary_test_records_preserved']}` records.",
            "- No Summary test records were used for train or validation.",
            "- No Param records were used in the classifier benchmark.",
            "",
            "## Skipped Files",
            "",
            *([f"- `{item}`" for item in result["skipped_files"]] or ["None."]),
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_export_report(result: dict[str, Any]) -> None:
    REPORTS_DIR.mkdir(exist_ok=True)
    path = REPORTS_DIR / "external_deep_jit_normalized_export_2026_08.md"
    lines = [
        "# External Deep-JIT Normalized Export 2026-08",
        "",
        f"- Raw data directory: `{result['data_dir']}`",
        f"- Output directory: `{result['output_dir']}`",
        f"- Label polarity status: `{result['label_polarity_status']}`",
        "",
        "## Written Files",
        "",
        "| Split | Path | Records | Label distribution |",
        "| --- | --- | ---: | --- |",
    ]
    for split, info in result["written"].items():
        lines.append(f"| `{split}` | `{info['path']}` | {info['records']} | `{info['label_distribution']}` |")
    lines.extend(
        [
            "",
            "## Leakage Rule",
            "",
            "The normalized records retain `new_comment_raw` / `doc_after` only for audit. The training module input builders do not include `new_comment_raw`, `doc_after`, or `doc_diff`.",
            "",
            "## Skipped Files",
            "",
            *([f"- `{item}`" for item in result["skipped_files"]] or ["None."]),
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
