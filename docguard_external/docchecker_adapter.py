from __future__ import annotations

import csv
import json
import pickletools
from collections import Counter
from pathlib import Path
from typing import Any


REPORTS_DIR = Path(__file__).resolve().parents[1] / "reports"
REPORT_PATH = REPORTS_DIR / "external_docchecker_local_schema_inspection_2026_08.md"
EXPECTED_FILES = [
    "train.jsonl",
    "valid.jsonl",
    "validation.jsonl",
    "test.jsonl",
    "train.csv",
    "valid.csv",
    "test.csv",
    "dataset/just_in_time",
]
DATA_SUFFIXES = {".json", ".jsonl", ".csv", ".tsv", ".pkl", ".pickle", ".txt"}
LABEL_CANDIDATES = {
    "label",
    "target",
    "y",
    "is_consistent",
    "inconsistent",
    "outdated",
    "is_outdated",
    "is_correct",
    "prediction",
    "gold",
}
CODE_COMMENT_CANDIDATES = {
    "code",
    "old_code",
    "new_code",
    "code_diff",
    "comment",
    "old_comment",
    "new_comment",
    "docstring",
    "old_docstring",
    "new_docstring",
    "nl",
    "before",
    "after",
}


def truncate(value: Any, limit: int = 180) -> str:
    text = "" if value is None else str(value)
    text = text.replace("\r", "\\r").replace("\n", "\\n")
    return text if len(text) <= limit else text[:limit] + "...[truncated]"


def detect_fields(keys: list[str]) -> dict[str, list[str]]:
    lowered = {key.lower(): key for key in keys}
    return {
        "likely_label_fields": [lowered[key] for key in sorted(LABEL_CANDIDATES & set(lowered))],
        "likely_code_comment_fields": [lowered[key] for key in sorted(CODE_COMMENT_CANDIDATES & set(lowered))],
    }


def inspect_json_file(path: Path, limit: int) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"path": str(path), "kind": "json", "error": str(exc)}
    records = data if isinstance(data, list) else [data] if isinstance(data, dict) else []
    keys = sorted({str(key) for row in records[:limit] if isinstance(row, dict) for key in row})
    return {
        "path": str(path),
        "kind": "json",
        "record_count_observed": len(records),
        "keys": keys,
        **detect_fields(keys),
        "sample_records": [{key: truncate(value) for key, value in row.items()} for row in records[:limit] if isinstance(row, dict)],
    }


def inspect_jsonl_file(path: Path, limit: int) -> dict[str, Any]:
    records = []
    errors = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            errors.append(f"line {line_no}: {exc}")
        if len(records) >= limit:
            break
    keys = sorted({str(key) for row in records if isinstance(row, dict) for key in row})
    return {
        "path": str(path),
        "kind": "jsonl",
        "record_count_observed": len(records),
        "keys": keys,
        **detect_fields(keys),
        "sample_records": [{key: truncate(value) for key, value in row.items()} for row in records if isinstance(row, dict)],
        "errors": errors[:5],
    }


def inspect_table_file(path: Path, limit: int) -> dict[str, Any]:
    delimiter = "\t" if path.suffix.lower() == ".tsv" else ","
    with path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=delimiter)
        rows = []
        for row in reader:
            rows.append({key: truncate(value) for key, value in row.items()})
            if len(rows) >= limit:
                break
    keys = list(reader.fieldnames or [])
    return {
        "path": str(path),
        "kind": path.suffix.lower().lstrip("."),
        "keys": keys,
        **detect_fields(keys),
        "sample_records": rows,
    }


def inspect_text_file(path: Path, limit: int) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()[:limit]
    return {
        "path": str(path),
        "kind": "txt",
        "line_count_observed": len(lines),
        "sample_lines": [truncate(line) for line in lines],
    }


def inspect_pickle_file(path: Path, limit: int) -> dict[str, Any]:
    op_counts: Counter[str] = Counter()
    error = None
    try:
        with path.open("rb") as handle:
            for index, (opcode, _arg, _pos) in enumerate(pickletools.genops(handle)):
                op_counts[opcode.name] += 1
                if index >= 500:
                    break
    except Exception as exc:
        error = str(exc)
    return {
        "path": str(path),
        "kind": path.suffix.lower().lstrip("."),
        "safe_summary_only": True,
        "note": "Pickle was not loaded to avoid executing custom classes/code; only pickle opcodes were scanned.",
        "top_pickle_opcodes": dict(op_counts.most_common(limit)),
        "error": error,
    }


def inspect_data_file(path: Path, limit: int) -> dict[str, Any]:
    suffix = path.suffix.lower()
    try:
        if suffix == ".json":
            return inspect_json_file(path, limit)
        if suffix == ".jsonl":
            return inspect_jsonl_file(path, limit)
        if suffix in {".csv", ".tsv"}:
            return inspect_table_file(path, limit)
        if suffix in {".pkl", ".pickle"}:
            return inspect_pickle_file(path, limit)
        if suffix == ".txt":
            return inspect_text_file(path, limit)
    except Exception as exc:
        return {"path": str(path), "kind": suffix.lstrip("."), "error": str(exc)}
    return {"path": str(path), "kind": suffix.lstrip("."), "note": "unsupported file suffix"}


def write_inspection_report(result: dict[str, Any]) -> None:
    REPORTS_DIR.mkdir(exist_ok=True)
    lines = [
        "# External DocChecker Local Schema Inspection 2026-08",
        "",
        f"- Status: `{result['status']}`",
        f"- Dataset: `{result['dataset']}`",
    ]
    if result.get("data_dir"):
        lines.append(f"- Data directory: `{result['data_dir']}`")
    if result.get("message"):
        lines.extend(["", "## Message", "", result["message"]])
    lines.extend(
        [
            "",
            "## Expected Command",
            "",
            "`python -m docguard_external.cli inspect --dataset docchecker --data-dir data/external/raw/docchecker --limit 10`",
            "",
            "## Expected File Types",
            "",
            ", ".join(f"`{item}`" for item in sorted(DATA_SUFFIXES)),
            "",
        ]
    )
    if result.get("file_count") is not None:
        lines.extend([f"- Total files: `{result['file_count']}`", f"- Candidate data files: `{result.get('candidate_file_count', 0)}`", ""])
    if result.get("detected_label_fields"):
        lines.extend(["## Detected Label Fields", "", *[f"- `{item}`" for item in result["detected_label_fields"]], ""])
    if result.get("detected_code_comment_fields"):
        lines.extend(["## Detected Code/Comment Fields", "", *[f"- `{item}`" for item in result["detected_code_comment_fields"]], ""])
    if result.get("file_summaries"):
        lines.extend(["## File Summaries", ""])
        for summary in result["file_summaries"]:
            lines.extend([f"### `{summary.get('path')}`", "", f"- Kind: `{summary.get('kind')}`"])
            if summary.get("keys"):
                lines.append(f"- Keys/header: {', '.join(f'`{key}`' for key in summary['keys'])}")
            if summary.get("likely_label_fields"):
                lines.append(f"- Likely label fields: {', '.join(f'`{key}`' for key in summary['likely_label_fields'])}")
            if summary.get("likely_code_comment_fields"):
                lines.append(f"- Likely code/comment fields: {', '.join(f'`{key}`' for key in summary['likely_code_comment_fields'])}")
            if summary.get("sample_records"):
                lines.append("- Sample records:")
                for row in summary["sample_records"][:3]:
                    lines.append(f"  - `{json.dumps(row, ensure_ascii=False)}`")
            if summary.get("sample_lines"):
                lines.append("- Sample lines:")
                for line in summary["sample_lines"][:3]:
                    lines.append(f"  - `{line}`")
            if summary.get("top_pickle_opcodes"):
                lines.append(f"- Pickle opcode summary: `{summary['top_pickle_opcodes']}`")
            if summary.get("error"):
                lines.append(f"- Error: `{summary['error']}`")
            lines.append("")
    lines.extend(
        [
            "## Mapping Status",
            "",
            result.get("mapping_status", "No records were created. Explicit binary labels must be confirmed first."),
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def inspect_docchecker(data_dir: Path | None = None, limit: int = 5) -> dict[str, Any]:
    if data_dir is None:
        result = {
            "status": "needs_local_data",
            "dataset": "docchecker",
            "message": "Local data path is required. Automatic download is not implemented.",
            "expected_command": "python -m docguard_external.cli inspect --dataset docchecker --data-dir data/external/raw/docchecker --limit 10",
            "expected_files": EXPECTED_FILES,
            "expected_file_types": sorted(DATA_SUFFIXES),
            "why_no_output": "No records created because no local files were supplied.",
            "mapping_status": "Blocked pending local data download and schema confirmation.",
        }
        write_inspection_report(result)
        return result
    if not data_dir.exists():
        result = {
            "status": "error",
            "dataset": "docchecker",
            "data_dir": str(data_dir),
            "message": f"data directory not found: {data_dir}",
            "expected_files": EXPECTED_FILES,
            "why_no_output": "No local files were available to inspect.",
            "mapping_status": "Blocked pending local data download.",
        }
        write_inspection_report(result)
        return result
    files = [path for path in data_dir.rglob("*") if path.is_file()]
    data_files = [path for path in files if path.suffix.lower() in DATA_SUFFIXES]
    summaries = [inspect_data_file(path, limit) for path in data_files[: max(limit, 1)]]
    detected_labels = sorted({field for summary in summaries for field in summary.get("likely_label_fields", [])})
    detected_code_comment = sorted({field for summary in summaries for field in summary.get("likely_code_comment_fields", [])})
    has_binary_candidates = bool(detected_labels and detected_code_comment)
    result = {
        "status": "local_files_inspected",
        "dataset": "docchecker",
        "data_dir": str(data_dir),
        "file_count": len(files),
        "candidate_file_count": len(data_files),
        "file_summaries": summaries,
        "detected_label_fields": detected_labels,
        "detected_code_comment_fields": detected_code_comment,
        "expected_files": EXPECTED_FILES,
        "mapping_status": (
            "Potential binary mapping fields detected; manually confirm label semantics before prepare."
            if has_binary_candidates
            else "No confirmed binary mapping. No records were created."
        ),
        "next_step": "Confirm label values mean consistent/inconsistent or outdated/up-to-date before implementing prepare.",
    }
    write_inspection_report(result)
    return result


def prepare_docchecker(*_args: Any, **_kwargs: Any) -> dict[str, Any]:
    return {
        "status": "blocked",
        "dataset": "docchecker",
        "message": "DocChecker preparation is blocked until local dataset format and explicit binary labels are confirmed by inspection.",
    }
