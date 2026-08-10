from __future__ import annotations

import difflib
import ast
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from docguard_external.schema import ExternalDocGuardRecord

DATASET_ID = "guineapig/codocbench"
INSTALL_COMMAND = "python -m pip install datasets huggingface_hub pandas pyarrow"
REPORTS_DIR = Path(__file__).resolve().parents[1] / "reports"

FIELD_CANDIDATES = {
    "repository": ["repo", "repository", "project", "repo_name", "project_name", "github_repo"],
    "commit_hash": ["commit", "commit_hash", "sha", "commit_sha", "revision"],
    "language": ["language", "lang", "programming_language"],
    "code_before": ["old_code", "code_before", "before_code", "original_code", "src_before", "method_before", "function_before"],
    "code_after": ["new_code", "code_after", "after_code", "updated_code", "src_after", "method_after", "function_after"],
    "code_diff": ["code_diff", "diff_code", "diff", "patch", "src_diff", "method_diff", "function_diff"],
    "doc_before": ["old_docstring", "doc_before", "documentation_before", "old_comment", "comment_before", "docstring_before", "old_doc"],
    "doc_after": ["new_docstring", "doc_after", "documentation_after", "new_comment", "comment_after", "docstring_after", "new_doc"],
    "doc_diff": ["doc_diff", "diff_docstring", "comment_diff", "documentation_diff", "docstring_diff"],
    "target_path": ["file_path", "path", "filename", "target_path", "code_path", "doc_path"],
    "function_name": ["function", "function_name", "method", "method_name", "name"],
    "split": ["split", "partition"],
}


def optional_import(module: str):
    try:
        return __import__(module)
    except Exception as exc:
        raise RuntimeError(f"Optional dependency `{module}` is required. Install with: {INSTALL_COMMAND}") from exc


def truncate_for_report(value: Any, limit: int = 240) -> str:
    text = "" if value is None else str(value)
    text = text.replace("\r", "\\r").replace("\n", "\\n")
    return text if len(text) <= limit else text[:limit] + "...[truncated]"


def first_present(record: dict[str, Any], candidates: Iterable[str]) -> Any:
    lowered = {str(key).lower(): key for key in record}
    for candidate in candidates:
        key = lowered.get(candidate.lower())
        if key is not None and record.get(key) not in {None, ""}:
            return record[key]
    return None


def build_diff(before: Any, after: Any, fromfile: str = "before", tofile: str = "after") -> str | None:
    if before in {None, ""} or after in {None, ""}:
        return None
    before_lines = str(before).splitlines()
    after_lines = str(after).splitlines()
    return "\n".join(difflib.unified_diff(before_lines, after_lines, fromfile=fromfile, tofile=tofile, lineterm=""))


def reconstruct_from_ndiff(diff_text: Any) -> tuple[str | None, str | None, list[str]]:
    if diff_text in {None, ""}:
        return None, None, ["empty ndiff text"]
    before: list[str] = []
    after: list[str] = []
    recognized = 0
    warnings: list[str] = []
    for line in str(diff_text).splitlines():
        if line.startswith("? "):
            recognized += 1
            continue
        if line.startswith("- "):
            before.append(line[2:])
            recognized += 1
            continue
        if line.startswith("+ "):
            after.append(line[2:])
            recognized += 1
            continue
        if line.startswith("  "):
            before.append(line[2:])
            after.append(line[2:])
            recognized += 1
            continue
        if line.strip():
            warnings.append("unrecognized ndiff line format")
    if not recognized or warnings:
        return None, None, sorted(set(warnings or ["unrecognized ndiff format"]))
    return "\n".join(before), "\n".join(after), []


def infer_language(target_path: Any, filename: Any) -> str | None:
    path_text = str(target_path or filename or "").lower()
    suffix_map = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".java": "java",
        ".go": "go",
        ".rb": "ruby",
        ".php": "php",
        ".cs": "csharp",
        ".cpp": "cpp",
        ".cc": "cpp",
        ".cxx": "cpp",
        ".c": "c",
        ".rs": "rust",
        ".kt": "kotlin",
        ".swift": "swift",
    }
    for suffix, language in suffix_map.items():
        if path_text.endswith(suffix):
            return language
    return None


def dataset_module():
    return optional_import("datasets")


def hub_module():
    return optional_import("huggingface_hub")


def get_dataset_configs() -> list[str | None]:
    datasets = dataset_module()
    try:
        configs = datasets.get_dataset_config_names(DATASET_ID)
        return configs or [None]
    except Exception:
        return [None]


def load_dataset_split(split: str = "train", limit: int | None = None, config: str | None = None):
    datasets = dataset_module()
    split_expr = split if limit is None else f"{split}[:{max(limit, 1)}]"
    try:
        return datasets.load_dataset(DATASET_ID, data_files={split: f"jsonl/{split}.jsonl"}, split=split_expr)
    except Exception:
        kwargs: dict[str, Any] = {"split": split_expr}
        if config:
            kwargs["name"] = config
        return datasets.load_dataset(DATASET_ID, **kwargs)


def load_small_dataset(limit: int, config: str | None = None):
    return load_dataset_split("train", limit, config)


def coerce_version_data(value: Any) -> tuple[list[dict[str, Any]], Any, list[str]]:
    warnings: list[str] = []
    raw = value
    parsed = value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            try:
                parsed = ast.literal_eval(value)
            except (SyntaxError, ValueError):
                warnings.append("malformed version_data")
                return [], raw, warnings
    if isinstance(parsed, dict):
        return [parsed], raw, warnings
    if isinstance(parsed, list):
        entries = [entry for entry in parsed if isinstance(entry, dict)]
        if len(entries) != len(parsed):
            warnings.append("version_data contains non-dict entries")
        return entries, raw, warnings
    if parsed not in {None, ""}:
        warnings.append("unsupported version_data type")
    return [], raw, warnings


def version_id(entry: dict[str, Any]) -> str | None:
    metadata_keys = {"commit_date_time", "commit_sha", "commit_message", "code", "docstring"}
    for key, value in entry.items():
        if key not in metadata_keys and isinstance(value, dict):
            return str(key)
    return None


def version_block(entry: dict[str, Any]) -> dict[str, Any]:
    vid = version_id(entry)
    if vid and isinstance(entry.get(vid), dict):
        return entry[vid]
    return {}


def version_lines(entry: dict[str, Any], kind: str) -> Any:
    block = version_block(entry)
    return block.get(kind) or entry.get(kind)


def version_pair(record: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], Any, list[str]]:
    entries, raw, warnings = coerce_version_data(record.get("version_data"))
    if entries:
        return entries[0], entries[-1], raw, warnings
    return {}, {}, raw, warnings


def truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def audit_path_for_output(output: Path) -> Path:
    return REPORTS_DIR / f"external_{output.stem}_audit_2026_08.md"


def inspect_codocbench(limit: int = 5) -> dict[str, Any]:
    REPORTS_DIR.mkdir(exist_ok=True)
    report_path = REPORTS_DIR / "external_codocbench_schema_inspection_2026_08.md"
    result: dict[str, Any] = {
        "status": "ok",
        "dataset": DATASET_ID,
        "available_configs": [],
        "available_splits": [],
        "column_names": [],
        "approx_record_count": None,
        "sample_records": [],
        "fallback_files": [],
        "error_message": None,
    }
    try:
        configs = get_dataset_configs()
        result["available_configs"] = [cfg or "default" for cfg in configs]
        config = configs[0]
        ds = load_small_dataset(limit, config)
        result["available_splits"] = ["train"]
        result["column_names"] = list(getattr(ds, "column_names", []) or [])
        try:
            result["approx_record_count"] = getattr(ds, "num_rows", None)
        except Exception:
            pass
        for row in list(ds)[:limit]:
            result["sample_records"].append({
                "keys": list(row.keys()),
                "values": {key: truncate_for_report(value) for key, value in row.items()},
            })
    except Exception as exc:
        result["status"] = "fallback"
        result["error_message"] = str(exc)
        try:
            hub = hub_module()
            files = hub.list_repo_files(DATASET_ID, repo_type="dataset")
            result["fallback_files"] = files
        except Exception as hub_exc:
            result["status"] = "error"
            result["error_message"] += f" | Hugging Face Hub fallback failed: {hub_exc}"
    write_inspection_report(result, report_path)
    return result


def write_inspection_report(result: dict[str, Any], path: Path) -> None:
    lines = [
        "# CoDocBench Schema Inspection 2026-08",
        "",
        f"- Dataset: `{result['dataset']}`",
        f"- Status: `{result['status']}`",
        f"- Available configs: {', '.join(result.get('available_configs') or []) or 'unknown'}",
        f"- Available splits: {', '.join(result.get('available_splits') or []) or 'unknown'}",
        f"- Column names: {', '.join(result.get('column_names') or []) or 'unknown'}",
        f"- Approximate inspected rows: `{result.get('approx_record_count')}`",
        "",
    ]
    if result.get("error_message"):
        lines.extend(["## Loader/Fallback Error", "", result["error_message"], ""])
    if result.get("fallback_files"):
        lines.extend(["## Repository Files", ""])
        lines.extend(f"- `{item}`" for item in result["fallback_files"][:200])
        lines.append("")
    if result.get("sample_records"):
        lines.extend(["## Sample Records", ""])
        for index, sample in enumerate(result["sample_records"], start=1):
            lines.append(f"### Sample {index}")
            lines.append("")
            lines.append(f"Keys: `{', '.join(sample['keys'])}`")
            lines.append("")
            for key, value in sample["values"].items():
                lines.append(f"- `{key}`: {value}")
            lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def map_record(record: dict[str, Any], index: int, split: str | None = None) -> ExternalDocGuardRecord:
    warnings: list[str] = []
    reconstruction_warnings: list[str] = []
    before_version, after_version, version_data_raw, version_warnings = version_pair(record)
    warnings.extend(version_warnings)
    code_before = first_present(record, FIELD_CANDIDATES["code_before"]) or before_version.get("code")
    code_after = first_present(record, FIELD_CANDIDATES["code_after"]) or after_version.get("code")
    code_diff = first_present(record, FIELD_CANDIDATES["code_diff"]) or build_diff(code_before, code_after, "code_before", "code_after")
    doc_before = first_present(record, FIELD_CANDIDATES["doc_before"]) or before_version.get("docstring")
    doc_after = first_present(record, FIELD_CANDIDATES["doc_after"]) or after_version.get("docstring")
    doc_diff = first_present(record, FIELD_CANDIDATES["doc_diff"]) or build_diff(doc_before, doc_after, "doc_before", "doc_after")
    reconstructed_code_before = False
    reconstructed_code_after = False
    reconstructed_doc_before = False
    reconstructed_doc_after = False
    if (code_before in {None, ""} or code_after in {None, ""}) and code_diff not in {None, ""}:
        reconstructed_before, reconstructed_after, ndiff_warnings = reconstruct_from_ndiff(code_diff)
        reconstruction_warnings.extend(f"code_diff: {warning}" for warning in ndiff_warnings)
        if code_before in {None, ""} and reconstructed_before not in {None, ""}:
            code_before = reconstructed_before
            reconstructed_code_before = True
        if code_after in {None, ""} and reconstructed_after not in {None, ""}:
            code_after = reconstructed_after
            reconstructed_code_after = True
    if (doc_before in {None, ""} or doc_after in {None, ""}) and doc_diff not in {None, ""}:
        reconstructed_before, reconstructed_after, ndiff_warnings = reconstruct_from_ndiff(doc_diff)
        reconstruction_warnings.extend(f"doc_diff: {warning}" for warning in ndiff_warnings)
        if doc_before in {None, ""} and reconstructed_before not in {None, ""}:
            doc_before = reconstructed_before
            reconstructed_doc_before = True
        if doc_after in {None, ""} and reconstructed_after not in {None, ""}:
            doc_after = reconstructed_after
            reconstructed_doc_after = True
    warnings.extend(reconstruction_warnings)
    for field_name, value in {
        "code_diff_or_before_after": code_diff or (code_before and code_after),
        "doc_diff_or_before_after": doc_diff or (doc_before and doc_after),
    }.items():
        if not value:
            warnings.append(f"missing {field_name}")
    docs_update_required = bool((code_diff or (code_before and code_after)) and (doc_diff or (doc_before and doc_after)))
    label_source = "strong_positive_code_doc_cochange" if docs_update_required and not warnings else "incomplete_mapping"
    repository = first_present(record, FIELD_CANDIDATES["repository"])
    commit_hash = first_present(record, FIELD_CANDIDATES["commit_hash"]) or after_version.get("commit_sha") or before_version.get("commit_sha")
    commit_date_time = after_version.get("commit_date_time") or before_version.get("commit_date_time")
    commit_message = after_version.get("commit_message") or before_version.get("commit_message")
    function_name = first_present(record, FIELD_CANDIDATES["function_name"])
    target_path = first_present(record, FIELD_CANDIDATES["target_path"])
    language = first_present(record, FIELD_CANDIDATES["language"]) or infer_language(target_path, record.get("filename"))
    for field_name, value in {
        "repository": repository,
        "commit_hash": commit_hash,
        "target_path": target_path,
        "language": language,
    }.items():
        if value in {None, ""}:
            warnings.append(f"missing {field_name}")
    if warnings:
        label_source = "incomplete_mapping"
    record_id_parts = [str(part) for part in [repository, commit_hash, function_name, index] if part not in {None, ""}]
    record_id = "codocbench-" + "-".join(record_id_parts).replace("/", "_").replace("\\", "_")[:180]
    return ExternalDocGuardRecord(
        record_id=record_id,
        source_dataset="codocbench",
        repository=str(repository) if repository is not None else None,
        commit_hash=str(commit_hash) if commit_hash is not None else None,
        language=str(language) if language is not None else None,
        code_before=str(code_before) if code_before is not None else None,
        code_after=str(code_after) if code_after is not None else None,
        code_diff=str(code_diff) if code_diff is not None else None,
        doc_before=str(doc_before) if doc_before is not None else None,
        doc_after=str(doc_after) if doc_after is not None else None,
        doc_diff=str(doc_diff) if doc_diff is not None else None,
        docs_update_required=docs_update_required,
        label_source=label_source,
        target_kind="docstring_or_comment" if docs_update_required else None,
        target_path=str(target_path) if target_path is not None else None,
        scenario_type="external_code_doc_cochange",
        split=str(first_present(record, FIELD_CANDIDATES["split"]) or split or "unknown"),
        metadata={
            "function_name": str(function_name) if function_name is not None else None,
            "owner": record.get("owner"),
            "filename": record.get("filename"),
            "commit_date_time": commit_date_time,
            "commit_message": commit_message,
            "old_version_id": version_id(before_version),
            "new_version_id": version_id(after_version),
            "before_commit_sha": before_version.get("commit_sha"),
            "after_commit_sha": after_version.get("commit_sha"),
            "version_data_raw": version_data_raw,
            "code_lines": {
                "before": version_lines(before_version, "code_lines"),
                "after": version_lines(after_version, "code_lines"),
            },
            "docstring_lines": {
                "before": version_lines(before_version, "docstring_lines"),
                "after": version_lines(after_version, "docstring_lines"),
            },
            "reconstructed_code_before": reconstructed_code_before,
            "reconstructed_code_after": reconstructed_code_after,
            "reconstructed_doc_before": reconstructed_doc_before,
            "reconstructed_doc_after": reconstructed_doc_after,
            "reconstruction_warnings": reconstruction_warnings,
            "mapping_warnings": warnings,
            "original_keys": list(record.keys()),
        },
    )


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + ("\n" if rows else ""), encoding="utf-8")


def prepare_codocbench(
    limit: int,
    output: Path,
    split: str = "train",
    exclude_whitespace_only: bool = False,
    max_per_project: int | None = None,
    seed: int = 42,
    shuffle: bool = False,
) -> dict[str, Any]:
    REPORTS_DIR.mkdir(exist_ok=True)
    try:
        configs = get_dataset_configs()
        load_limit = None if shuffle or max_per_project else limit
        ds = load_dataset_split(split, load_limit, configs[0])
    except Exception as exc:
        result = {
            "status": "error",
            "dataset": "codocbench",
            "output": str(output),
            "requested_limit": limit,
            "written_records": 0,
            "skipped_records": 0,
            "whitespace_only_skipped_count": 0,
            "label_source_counts": {},
            "warnings": [f"Could not load `{DATASET_ID}`: {exc}", f"Install/check dependencies with: {INSTALL_COMMAND}"],
        }
        write_prepare_failure_report(result)
        return result
    normalized: list[ExternalDocGuardRecord] = []
    skipped = 0
    whitespace_only_skipped = 0
    per_project: Counter[str] = Counter()
    rows_to_consider = [dict(row) for row in ds]
    if shuffle:
        random.Random(seed).shuffle(rows_to_consider)
    for index, row in enumerate(rows_to_consider):
        if len(normalized) >= limit:
            break
        project = str(first_present(row, FIELD_CANDIDATES["repository"]) or "unknown")
        if exclude_whitespace_only and (truthy(row.get("whitespace_only_code")) or truthy(row.get("whitespace_only_docstring"))):
            skipped += 1
            whitespace_only_skipped += 1
            continue
        if max_per_project is not None and per_project[project] >= max_per_project:
            skipped += 1
            continue
        try:
            normalized.append(map_record(row, index=index, split=split))
            per_project[project] += 1
        except Exception:
            skipped += 1
    rows = [record.to_dict() for record in normalized]
    write_jsonl(output, rows)
    label_counts = Counter(row["label_source"] for row in rows)
    warnings = sorted({warning for row in rows for warning in row.get("metadata", {}).get("mapping_warnings", [])})
    result = {
        "status": "ok",
        "dataset": "codocbench",
        "output": str(output),
        "requested_limit": limit,
        "written_records": len(rows),
        "skipped_records": skipped,
        "split": split,
        "exclude_whitespace_only": exclude_whitespace_only,
        "whitespace_only_skipped_count": whitespace_only_skipped,
        "max_per_project": max_per_project,
        "shuffle": shuffle,
        "seed": seed,
        "label_source_counts": dict(label_counts),
        "warnings": warnings,
    }
    write_sample_audit(rows, result, audit_path_for_output(output))
    write_label_quality_notes()
    return result


def write_prepare_failure_report(result: dict[str, Any]) -> None:
    path = REPORTS_DIR / "external_codocbench_sample_audit_2026_08.md"
    lines = [
        "# External CoDocBench Sample Audit 2026-08",
        "",
        "No sample was written because loading failed.",
        "",
        "## Error",
        "",
        *[f"- {warning}" for warning in result.get("warnings", [])],
        "",
        "## Next Manual Step",
        "",
        "Inspect the Hugging Face dataset page or clone/download a small release file, then update field mapping if needed.",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_sample_audit(rows: list[dict[str, Any]], summary: dict[str, Any], path: Path | None = None) -> None:
    path = path or REPORTS_DIR / "external_codocbench_sample_audit_2026_08.md"
    split_counts = Counter(row.get("split") for row in rows)
    language_counts = Counter(row.get("language") or "unknown" for row in rows)
    repo_counts = Counter(row.get("repository") or "unknown" for row in rows)
    owner_counts = Counter((row.get("metadata") or {}).get("owner") or "unknown" for row in rows)
    label_counts = Counter(row.get("label_source") for row in rows)
    missing_counts: Counter[str] = Counter()
    warning_counts: Counter[str] = Counter()
    commit_dates = [
        str((row.get("metadata") or {}).get("commit_date_time"))
        for row in rows
        if (row.get("metadata") or {}).get("commit_date_time") not in {None, ""}
    ]
    for row in rows:
        for key in ["repository", "commit_hash", "language", "code_diff", "doc_diff", "code_before", "code_after", "doc_before", "doc_after", "target_path"]:
            if row.get(key) in {None, ""}:
                missing_counts[key] += 1
        for warning in row.get("metadata", {}).get("mapping_warnings", []):
            warning_counts[warning] += 1
    lines = [
        "# External CoDocBench Sample Audit 2026-08",
        "",
        f"- Records written: `{len(rows)}`",
        f"- Skipped records: `{summary.get('skipped_records', 0)}`",
        "- Source dataset: `codocbench` / `guineapig/codocbench`",
        f"- Output: `{summary.get('output')}`",
        f"- Requested limit: `{summary.get('requested_limit')}`",
        f"- Shuffle: `{summary.get('shuffle')}`",
        f"- Seed: `{summary.get('seed')}`",
        f"- Max per project: `{summary.get('max_per_project')}`",
        f"- Exclude whitespace-only: `{summary.get('exclude_whitespace_only')}`",
        f"- Whitespace-only skipped count: `{summary.get('whitespace_only_skipped_count', 0)}`",
        f"- Commit date range: `{min(commit_dates) if commit_dates else 'unknown'}` to `{max(commit_dates) if commit_dates else 'unknown'}`",
        "",
        "## Split Distribution",
        "",
        *[f"- `{key}`: {value}" for key, value in sorted(split_counts.items())],
        "",
        "## Language Distribution",
        "",
        *[f"- `{key}`: {value}" for key, value in language_counts.most_common(20)],
        "",
        "## Repository Distribution",
        "",
        *[f"- `{key}`: {value}" for key, value in repo_counts.most_common(20)],
        "",
        "## Owner Distribution",
        "",
        *[f"- `{key}`: {value}" for key, value in owner_counts.most_common(20)],
        "",
        "## Top 10 Repositories",
        "",
        *[f"- `{key}`: {value}" for key, value in repo_counts.most_common(10)],
        "",
        "## Label Source Distribution",
        "",
        *[f"- `{key}`: {value}" for key, value in sorted(label_counts.items())],
        "",
        "## Missing Field Counts",
        "",
        *([f"- `{key}`: {value}" for key, value in sorted(missing_counts.items())] or ["None."]),
        "",
        "## Mapping Warnings",
        "",
        *([f"- `{key}`: {value}" for key, value in sorted(warning_counts.items())] or ["None."]),
        "",
        "## Truncated Examples",
        "",
    ]
    for row in rows[:5]:
        lines.extend([
            f"### {row['record_id']}",
            "",
            f"- repository: `{row.get('repository')}`",
            f"- commit: `{row.get('commit_hash')}`",
            f"- label_source: `{row.get('label_source')}`",
            f"- code_diff: {truncate_for_report(row.get('code_diff'))}",
            f"- doc_diff: {truncate_for_report(row.get('doc_diff'))}",
            "",
        ])
    lines.extend([
        "## Difference From Synthetic v0.4",
        "",
        "CoDocBench records are real code/documentation or code/docstring co-changes. They should be used as real-world validation for code-comment/docstring update behavior, not as a direct replacement for DocGuard's synthetic project-level Markdown documentation benchmark.",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def write_label_quality_notes() -> None:
    path = REPORTS_DIR / "external_codocbench_label_quality_notes_2026_08.md"
    lines = [
        "# External CoDocBench Label Quality Notes 2026-08",
        "",
        "- CoDocBench positive labels are code-documentation co-change labels.",
        "- These labels are stronger than synthetic labels for real-world validation because they come from mined maintenance history.",
        "- They are not identical to broad project-level Markdown documentation update labels.",
        "- Negative labels should not be inferred from code-only commits without careful rules.",
        "- The first pilot should evaluate whether DocGuard can process real code-doc changes, not whether it can fully patch project documentation files.",
        "- Keep strong positive labels and any future weak negative labels separated in reports.",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def validate_codocbench_sample(input_path: Path) -> dict[str, Any]:
    from docguard_external.schema import validate_record

    REPORTS_DIR.mkdir(exist_ok=True)
    errors: list[dict[str, Any]] = []
    seen: set[str] = set()
    counts = Counter()
    records = 0
    if not input_path.exists():
        result = {"status": "error", "records_checked": 0, "errors": [{"line": 0, "errors": [f"input not found: {input_path}"]}]}
        write_validation_report(result, input_path)
        return result
    for line_no, line in enumerate(input_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append({"line": line_no, "errors": [f"invalid json: {exc}"]})
            continue
        records += 1
        row_errors = validate_record(row)
        if row.get("docs_update_required") is not True:
            row_errors.append("CoDocBench pilot should not create automatic negative labels")
        if row.get("source_dataset") != "codocbench":
            row_errors.append("source_dataset must be codocbench")
        if row.get("scenario_type") != "external_code_doc_cochange":
            row_errors.append("scenario_type must be external_code_doc_cochange")
        if row.get("label_source") not in {"strong_positive_code_doc_cochange", "incomplete_mapping"}:
            row_errors.append("invalid CoDocBench pilot label_source")
        if row.get("label_source") == "strong_positive_code_doc_cochange" and row.get("metadata", {}).get("mapping_warnings"):
            row_errors.append("strong positive rows must not carry mapping warnings")
        for expected_fact in ["repository", "commit_hash", "language", "target_kind", "target_path"]:
            if row.get(expected_fact) in {None, ""}:
                row_errors.append(f"missing expected fact: {expected_fact}")
        if not (row.get("code_diff") or (row.get("code_before") and row.get("code_after"))):
            row_errors.append("missing code_diff or code_before/code_after")
        if not (row.get("doc_diff") or (row.get("doc_before") and row.get("doc_after"))):
            row_errors.append("missing doc_diff or doc_before/doc_after")
        record_id = row.get("record_id")
        if record_id in seen:
            row_errors.append(f"duplicate record_id: {record_id}")
        seen.add(record_id)
        counts[row.get("label_source")] += 1
        if row_errors:
            errors.append({"line": line_no, "record_id": record_id, "errors": row_errors})
    result = {"status": "ok" if not errors else "error", "records_checked": records, "label_source_counts": dict(counts), "errors": errors[:100]}
    write_validation_report(result, input_path)
    return result


def write_validation_report(result: dict[str, Any], input_path: Path) -> None:
    path = REPORTS_DIR / "external_codocbench_sample_validation_2026_08.md"
    lines = [
        "# External CoDocBench Sample Validation 2026-08",
        "",
        f"- Input: `{input_path}`",
        f"- Status: `{result['status']}`",
        f"- Records checked: `{result.get('records_checked', 0)}`",
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
    path.write_text("\n".join(lines), encoding="utf-8")
