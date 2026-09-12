from __future__ import annotations

import argparse
import hashlib
import json
import os
import zipfile
from pathlib import Path


ARCHIVE = Path("/kaggle/working/s1_development_return_artifacts.zip")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Package the S1 development-only Kaggle return")
    parser.add_argument("--output", type=Path, default=Path("/kaggle/working/s1-development"))
    args = parser.parse_args()
    output = args.output.resolve()
    required = [
        "canary_receipt.json", "runtime_manifest.json", "development_metrics.json", "retrieval_metrics.json",
        "retrieval_results.jsonl", "generation_results.jsonl", "prompt_hashes.json", "model_revision_receipt.json",
        "development_selection_status.json", "execution.log", "checkpoints/development_metrics_complete.json",
    ]
    missing = [relative for relative in required if not (output / relative).is_file()]
    if missing:
        raise RuntimeError(f"Cannot package incomplete S1 development return; missing: {missing}")
    files = [path for path in sorted(output.rglob("*")) if path.is_file() and path.name != "artifact_manifest.json"]
    manifest = {
        "scientific_status": "POST_HOC_STAGE3_CHALLENGER_DEVELOPMENT_ONLY",
        "confirmation_accessed": False,
        "gate6_row_level_human_data_accessed": False,
        "file_count_excluding_manifest": len(files),
        "files": [{"path": path.relative_to(output).as_posix(), "bytes": path.stat().st_size, "sha256": sha256(path)} for path in files],
    }
    manifest_path = output / "artifact_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    files.append(manifest_path)
    if ARCHIVE.exists():
        ARCHIVE.unlink()
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in sorted(files):
            archive.write(path, arcname=path.relative_to(output).as_posix())
    digest = sha256(ARCHIVE)
    print(f"archive_path={ARCHIVE}")
    print(f"archive_size={ARCHIVE.stat().st_size}")
    print(f"archive_sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
