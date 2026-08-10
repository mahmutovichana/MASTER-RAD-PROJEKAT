from __future__ import annotations

from pathlib import Path
from typing import Any


EXPECTED_FILES = [
    "public_comment_update_data/comment_update",
    "public_comment_update_data/full_comment_generation",
    "train.jsonl",
    "valid.jsonl",
    "test.jsonl",
    "train.tsv",
    "valid.tsv",
    "test.tsv",
]


def inspect_panthaplackel(data_dir: Path | None = None, limit: int = 5) -> dict[str, Any]:
    if data_dir is None:
        return {
            "status": "needs_local_data",
            "dataset": "panthaplackel_comment_update",
            "message": "Automatic download is not implemented. Provide --data-dir pointing to downloaded LearningToUpdateNLComments data.",
            "expected_files": EXPECTED_FILES,
            "why_no_output": "The repository points to external Google Drive data; local schema must be confirmed before creating records.",
        }
    if not data_dir.exists():
        return {
            "status": "error",
            "dataset": "panthaplackel_comment_update",
            "message": f"data directory not found: {data_dir}",
            "expected_files": EXPECTED_FILES,
            "why_no_output": "No local files were available to inspect.",
        }
    files = [path for path in data_dir.rglob("*") if path.is_file()]
    sample_files = []
    for path in files[:limit]:
        sample_files.append(
            {
                "path": str(path),
                "size_bytes": path.stat().st_size,
                "suffix": path.suffix,
            }
        )
    return {
        "status": "local_files_inspected",
        "dataset": "panthaplackel_comment_update",
        "data_dir": str(data_dir),
        "file_count": len(files),
        "sample_files": sample_files,
        "expected_files": EXPECTED_FILES,
        "next_step": "Confirm whether data contains only update pairs or explicit non-update labels before implementing prepare.",
    }


def prepare_panthaplackel(*_args: Any, **_kwargs: Any) -> dict[str, Any]:
    return {
        "status": "not_implemented",
        "dataset": "panthaplackel_comment_update",
        "message": "Panthaplackel preparation is not implemented until local data format and label availability are confirmed.",
    }
