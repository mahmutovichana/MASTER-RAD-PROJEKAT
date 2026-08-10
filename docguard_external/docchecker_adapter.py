from __future__ import annotations

import csv
import difflib
import json
import pickletools
from collections import Counter
from pathlib import Path
from typing import Any

from docguard_external.schema import ExternalDocGuardRecord, validate_record


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
    "old_code_raw",
    "new_code_raw",
    "old_comment_raw",
    "new_comment_raw",
    "old_docstring_raw",
    "new_docstring_raw",
}
REQUIRED_DEEP_JIT_FIELDS = {"id", "label", "old_code_raw", "new_code_raw", "old_comment_raw", "new_comment_raw"}


def compact_inspection_result(result: dict[str, Any]) -> dict[str, Any]:
    compact = {key: value for key, value in result.items() if key != "file_summaries"}
    if result.get("file_summaries"):
        compact["inspected_files"] = [
            {
                "path": summary.get("path"),
                "kind": summary.get("kind"),
                "record_count_observed": summary.get("record_count_observed"),
                "likely_label_fields": summary.get("likely_label_fields", []),
                "likely_code_comment_fields": summary.get("likely_code_comment_fields", []),
            }
            for summary in result["file_summaries"]
        ]
    compact["report"] = str(REPORT_PATH)
    return compact


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
    if isinstance(data, list):
        records = data[:limit]
        total_count = len(data)
    elif isinstance(data, dict):
        values = list(data.values())
        records = values[:limit] if values and all(isinstance(value, dict) for value in values[:limit]) else [dict(list(data.items())[:limit])]
        total_count = len(data)
    else:
        records = []
        total_count = 0
    keys = sorted({str(key) for row in records[:limit] if isinstance(row, dict) for key in row})
    return {
        "path": str(path),
        "kind": "json",
        "record_count_observed": total_count,
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
        return compact_inspection_result(result)
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
        return compact_inspection_result(result)
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
    return compact_inspection_result(result)


def prepare_docchecker(*_args: Any, **_kwargs: Any) -> dict[str, Any]:
    data_dir = _kwargs.get("data_dir")
    limit = int(_kwargs.get("limit") or 500)
    output = Path(_kwargs.get("output"))
    if data_dir is None or not Path(data_dir).exists():
        return {
            "status": "blocked",
            "dataset": "docchecker",
            "message": "DocChecker preparation requires --data-dir with local Deep-JIT/DocChecker data.",
        }
    rows, warnings = load_deep_jit_records(Path(data_dir), limit)
    if not rows:
        result = {
            "status": "blocked",
            "dataset": "docchecker",
            "message": "No records with explicit Deep-JIT binary fields were found.",
            "warnings": warnings,
        }
        write_prepare_blocked_report(result)
        return result
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(json.dumps(row.to_dict(), ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    dict_rows = [row.to_dict() for row in rows]
    write_binary_sample_audit(dict_rows, warnings)
    result = {
        "status": "ok",
        "dataset": "docchecker",
        "source_dataset": "deep_jit_inconsistency",
        "output": str(output),
        "written_records": len(rows),
        "positive_count": sum(1 for row in rows if row.docs_update_required is True),
        "negative_count": sum(1 for row in rows if row.docs_update_required is False),
        "label_source_counts": dict(Counter(row.label_source for row in rows)),
        "warnings": warnings[:20],
    }
    return result


def build_diff(before: str, after: str, fromfile: str, tofile: str) -> str:
    return "\n".join(difflib.unified_diff(str(before).splitlines(), str(after).splitlines(), fromfile=fromfile, tofile=tofile, lineterm=""))


def infer_split(path: Path) -> str:
    name = path.stem.lower()
    return "validation" if name in {"valid", "validation", "dev"} else name


def deep_jit_json_files(data_dir: Path) -> list[Path]:
    return [
        path
        for path in sorted(data_dir.rglob("*.json"))
        if "resources" not in {part.lower() for part in path.parts}
    ]


def label_to_bool(value: Any) -> bool | None:
    text = str(value).strip().lower()
    if text in {"1", "true", "inconsistent", "outdated", "yes"}:
        return True
    if text in {"0", "false", "consistent", "up_to_date", "no"}:
        return False
    return None


def row_has_required_fields(row: dict[str, Any]) -> bool:
    return REQUIRED_DEEP_JIT_FIELDS <= set(row)


def load_records_from_json(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return [row for row in data if isinstance(row, dict)]
    if isinstance(data, dict):
        return [row for row in data.values() if isinstance(row, dict)]
    return []


def map_deep_jit_row(row: dict[str, Any], source_file: Path, index: int) -> ExternalDocGuardRecord | None:
    docs_update_required = label_to_bool(row.get("label"))
    if docs_update_required is None:
        return None
    record_id = f"deep-jit-{row.get('id') or index}".replace("/", "_").replace("\\", "_")
    code_before = str(row.get("old_code_raw") or "")
    code_after = str(row.get("new_code_raw") or "")
    doc_before = str(row.get("old_comment_raw") or "")
    doc_after = str(row.get("new_comment_raw") or "")
    return ExternalDocGuardRecord(
        record_id=record_id,
        source_dataset="deep_jit_inconsistency",
        repository=str(row.get("id", "")).split("-")[0] if row.get("id") else None,
        commit_hash=None,
        language="java",
        code_before=code_before,
        code_after=code_after,
        code_diff=build_diff(code_before, code_after, "old_code", "new_code"),
        doc_before=doc_before,
        doc_after=doc_after,
        doc_diff=build_diff(doc_before, doc_after, "old_comment", "new_comment"),
        docs_update_required=docs_update_required,
        label_source="strong_external_inconsistent_comment" if docs_update_required else "strong_external_consistent_comment",
        target_kind="comment_or_docstring",
        target_path=None,
        scenario_type="external_comment_inconsistency" if docs_update_required else "external_comment_consistent_no_update",
        split=infer_split(source_file),
        metadata={
            "source_file": str(source_file),
            "source_record_id": row.get("id"),
            "comment_type": row.get("comment_type"),
            "original_label": row.get("label"),
            "mapping_warnings": [],
        },
    )


def load_deep_jit_records(data_dir: Path, limit: int) -> tuple[list[ExternalDocGuardRecord], list[str]]:
    target_positive = limit // 2
    target_negative = limit - target_positive
    candidates: dict[bool, list[ExternalDocGuardRecord]] = {True: [], False: []}
    warnings: list[str] = []
    for path in deep_jit_json_files(data_dir):
        try:
            rows = load_records_from_json(path)
        except Exception as exc:
            warnings.append(f"could not read {path}: {exc}")
            continue
        for row in rows:
            if not row_has_required_fields(row):
                continue
            mapped = map_deep_jit_row(row, path, len(candidates[True]) + len(candidates[False]))
            if mapped is not None:
                candidates[mapped.docs_update_required].append(mapped)
    if len(candidates[True]) < target_positive or len(candidates[False]) < target_negative:
        warnings.append(
            f"requested balanced sample of {limit}, but found {len(candidates[True])} positives and {len(candidates[False])} negatives"
        )
    records = select_balanced_records(candidates[True], min(target_positive, len(candidates[True])))
    records.extend(select_balanced_records(candidates[False], min(target_negative, len(candidates[False]))))
    return records, warnings


def split_rank(record: ExternalDocGuardRecord) -> int:
    return {"test": 0, "validation": 1, "valid": 1, "train": 2}.get(record.split, 3)


def select_balanced_records(records: list[ExternalDocGuardRecord], target: int) -> list[ExternalDocGuardRecord]:
    if target <= 0:
        return []
    by_file: dict[str, list[ExternalDocGuardRecord]] = {}
    for record in sorted(records, key=lambda item: (split_rank(item), str(item.metadata.get("source_file")), item.record_id)):
        by_file.setdefault(str(record.metadata.get("source_file")), []).append(record)
    selected_sources: list[str] = []
    total_available = 0
    for rank in sorted({split_rank(record) for record in records}):
        rank_sources = [
            source
            for source, source_records in by_file.items()
            if source_records and split_rank(source_records[0]) == rank
        ]
        selected_sources.extend(sorted(rank_sources))
        total_available = sum(len(by_file[source]) for source in selected_sources)
        if total_available >= target:
            break
    selected: list[ExternalDocGuardRecord] = []
    positions = {source: 0 for source in selected_sources}
    while len(selected) < target:
        progressed = False
        for source in selected_sources:
            index = positions[source]
            if index < len(by_file[source]):
                selected.append(by_file[source][index])
                positions[source] += 1
                progressed = True
                if len(selected) >= target:
                    break
        if not progressed:
            break
    return selected


def write_prepare_blocked_report(result: dict[str, Any]) -> None:
    REPORTS_DIR.mkdir(exist_ok=True)
    path = REPORTS_DIR / "external_docchecker_binary_sample_audit_2026_08.md"
    lines = [
        "# External DocChecker Binary Sample Audit 2026-08",
        "",
        "No binary sample was created.",
        "",
        f"- Status: `{result.get('status')}`",
        f"- Message: {result.get('message')}",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_binary_sample_audit(rows: list[dict[str, Any]], warnings: list[str]) -> None:
    REPORTS_DIR.mkdir(exist_ok=True)
    path = REPORTS_DIR / "external_docchecker_binary_sample_audit_2026_08.md"
    label_counts = Counter(row.get("label_source") for row in rows)
    source_counts = Counter((row.get("metadata") or {}).get("source_file") for row in rows)
    split_counts = Counter(row.get("split") for row in rows)
    missing_counts: Counter[str] = Counter()
    for row in rows:
        for key in ["code_before", "code_after", "code_diff", "doc_before", "doc_after", "doc_diff", "label_source"]:
            if row.get(key) in {None, ""}:
                missing_counts[key] += 1
    positives = [row for row in rows if row.get("docs_update_required") is True]
    negatives = [row for row in rows if row.get("docs_update_required") is False]
    lines = [
        "# External DocChecker Binary Sample Audit 2026-08",
        "",
        f"- Total records: `{len(rows)}`",
        f"- Positive count: `{len(positives)}`",
        f"- Negative count: `{len(negatives)}`",
        "",
        "## Label Distribution",
        "",
        *[f"- `{key}`: {value}" for key, value in sorted(label_counts.items())],
        "",
        "## Source File Distribution",
        "",
        *[f"- `{key}`: {value}" for key, value in source_counts.most_common(20)],
        "",
        "## Split Distribution",
        "",
        *[f"- `{key}`: {value}" for key, value in sorted(split_counts.items())],
        "",
        "## Language Distribution",
        "",
        "- `java`: " + str(len(rows)),
        "",
        "## Missing Fields",
        "",
        *([f"- `{key}`: {value}" for key, value in sorted(missing_counts.items())] or ["None."]),
        "",
        "## Mapping Warnings",
        "",
        *([f"- {warning}" for warning in warnings] or ["None."]),
        "",
        "## Positive Examples",
        "",
    ]
    for row in positives[:5]:
        lines.extend(example_lines(row))
    lines.extend(["", "## Negative Examples", ""])
    for row in negatives[:5]:
        lines.extend(example_lines(row))
    lines.extend(
        [
            "",
            "## Limitations",
            "",
            "This is a code-comment consistency proxy, not full project-level Markdown documentation update detection.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def example_lines(row: dict[str, Any]) -> list[str]:
    return [
        f"### {row.get('record_id')}",
        "",
        f"- label_source: `{row.get('label_source')}`",
        f"- split: `{row.get('split')}`",
        f"- source id: `{(row.get('metadata') or {}).get('source_record_id')}`",
        f"- code_diff: {truncate(row.get('code_diff'), 280)}",
        f"- doc_diff: {truncate(row.get('doc_diff'), 220)}",
        "",
    ]


def validate_docchecker_binary_sample(input_path: Path) -> dict[str, Any]:
    errors: list[dict[str, Any]] = []
    seen: set[str] = set()
    label_counts: Counter[str] = Counter()
    rows = []
    if not input_path.exists():
        result = {"status": "error", "records_checked": 0, "errors": [{"line": 0, "errors": [f"input not found: {input_path}"]}]}
        write_binary_validation_report(result, input_path)
        return result
    for line_no, line in enumerate(input_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        row = json.loads(line)
        rows.append(row)
        row_errors = validate_record(row)
        if row.get("source_dataset") not in {"docchecker", "deep_jit_inconsistency"}:
            row_errors.append("source_dataset must identify external binary dataset")
        if row.get("label_source") not in {"strong_external_inconsistent_comment", "strong_external_consistent_comment"}:
            row_errors.append("label_source must be explicit external binary label")
        if row.get("docs_update_required") not in {True, False}:
            row_errors.append("docs_update_required must be boolean")
        if not (row.get("code_before") or row.get("code_after") or row.get("code_diff")):
            row_errors.append("missing code fields")
        if not (row.get("doc_before") or row.get("doc_after") or row.get("doc_diff")):
            row_errors.append("missing comment/docstring fields")
        if row.get("record_id") in seen:
            row_errors.append("duplicate record_id")
        seen.add(row.get("record_id"))
        label_counts[row.get("label_source")] += 1
        if row_errors:
            errors.append({"line": line_no, "record_id": row.get("record_id"), "errors": row_errors})
    if not any(row.get("docs_update_required") is True for row in rows):
        errors.append({"line": 0, "errors": ["sample must contain positive records"]})
    if not any(row.get("docs_update_required") is False for row in rows):
        errors.append({"line": 0, "errors": ["sample must contain negative records"]})
    result = {"status": "ok" if not errors else "error", "records_checked": len(rows), "label_source_counts": dict(label_counts), "errors": errors[:100]}
    write_binary_validation_report(result, input_path)
    return result


def write_binary_validation_report(result: dict[str, Any], input_path: Path) -> None:
    REPORTS_DIR.mkdir(exist_ok=True)
    path = REPORTS_DIR / "external_docchecker_binary_sample_validation_2026_08.md"
    lines = [
        "# External DocChecker Binary Sample Validation 2026-08",
        "",
        f"- Input: `{input_path}`",
        f"- Status: `{result.get('status')}`",
        f"- Records checked: `{result.get('records_checked')}`",
        "",
        "## Label Source Counts",
        "",
        *[f"- `{key}`: {value}" for key, value in sorted((result.get("label_source_counts") or {}).items())],
        "",
        "## Errors",
        "",
    ]
    if result.get("errors"):
        for error in result["errors"]:
            lines.append(f"- line {error.get('line')}, record `{error.get('record_id')}`: {'; '.join(error.get('errors', []))}")
    else:
        lines.append("None.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
