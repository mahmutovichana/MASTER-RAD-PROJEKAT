from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import shutil
import sys
import tarfile
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np

from docguard_ml_v2.gate2_study import load_config, load_development_rows, load_fold_checkpoint, sha256_file


EMBEDDING_FILES = {
    "embedding_checkpoint.json",
    "code.mmap",
    "docs.mmap",
    "code_lengths.mmap",
    "docs_lengths.mmap",
    "code_truncated.mmap",
    "docs_truncated.mmap",
}
SAFE_ROOT_FILES = {"external_workflow_status.json", "external_workflow_events.jsonl"}
FOLD_RE = re.compile(r"^(binary|category)_(M[123])_fold([0-4])_checkpoint\.json$")
SECRET_RE = re.compile(r"(^|[._-])(token|secret|credential|password)([._-]|$)", re.IGNORECASE)
SECRET_VALUE_RE = re.compile(rb"(?:hf_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|ghp_[A-Za-z0-9]{20,})")


def _canonical_sha(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def scientific_identity(config_path: Path) -> dict[str, Any]:
    config = load_config(config_path)
    rows, view = load_development_rows(config_path=config_path)
    semantic = config["families"]["M2"]
    return {
        "scientific_config_sha256": sha256_file(config_path),
        "gold_sha256": view["gold_sha256"],
        "development_view_sha256": view["development_view_sha256"],
        "development_rows": view["development_rows"],
        "row_order_sha256": hashlib.sha256(("\n".join(str(row["case_id"]) for row in rows) + "\n").encode("utf-8")).hexdigest(),
        "encoder_revision": semantic["encoder_revision"],
        "tokenizer_revision": semantic["tokenizer_revision"],
        "pooling": semantic["pooling"],
        "max_length": int(semantic["max_length"]),
        "dtype": "float32",
        "confirmation_accessed": False,
    }


def _checkpoint_specs(total_rows: int, hidden_size: int) -> dict[str, tuple[str, tuple[int, ...]]]:
    return {
        "code.mmap": ("float32", (total_rows, hidden_size)),
        "docs.mmap": ("float32", (total_rows, hidden_size)),
        "code_lengths.mmap": ("int32", (total_rows,)),
        "docs_lengths.mmap": ("int32", (total_rows,)),
        "code_truncated.mmap": ("uint8", (total_rows,)),
        "docs_truncated.mmap": ("uint8", (total_rows,)),
    }


def validate_embedding_checkpoint(checkpoint_dir: Path, identity: dict[str, Any]) -> dict[str, Any] | None:
    metadata_path = checkpoint_dir / "embedding_checkpoint.json"
    present = [path for path in checkpoint_dir.glob("*") if path.is_file()] if checkpoint_dir.exists() else []
    if not metadata_path.exists():
        if present:
            raise RuntimeError("Embedding checkpoint metadata is missing")
        return None
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    expected_identity = {key: identity[key] for key in (
        "gold_sha256", "development_view_sha256", "row_order_sha256", "encoder_revision", "tokenizer_revision", "pooling", "max_length", "dtype"
    )}
    for key, expected in expected_identity.items():
        if metadata.get("identity", {}).get(key) != expected:
            raise RuntimeError(f"Embedding checkpoint scientific identity mismatch: {key}")
    total_rows = metadata.get("total_rows")
    hidden_size = metadata.get("hidden_size")
    completed = metadata.get("completed_count")
    if total_rows != identity["development_rows"] or not isinstance(hidden_size, int) or hidden_size < 1:
        raise RuntimeError("Embedding checkpoint shape identity mismatch")
    if not isinstance(completed, int) or not 0 <= completed <= total_rows:
        raise RuntimeError("Embedding checkpoint completed_count is invalid")
    if metadata.get("status") == "COMPLETE" and completed != total_rows:
        raise RuntimeError("COMPLETE embedding checkpoint has incomplete rows")
    for name, (dtype, shape) in _checkpoint_specs(total_rows, hidden_size).items():
        path = checkpoint_dir / name
        expected_bytes = int(np.prod(shape)) * np.dtype(dtype).itemsize
        if not path.exists() or path.stat().st_size != expected_bytes:
            raise RuntimeError(f"Embedding checkpoint file is missing or has wrong size: {name}")
    unexpected = sorted(path.name for path in present if path.name not in EMBEDDING_FILES)
    if unexpected:
        raise RuntimeError(f"Unexpected embedding checkpoint files: {unexpected}")
    return metadata


def _validate_fold(path: Path, config_path: Path, identity: dict[str, Any], embedding_artifact_sha256: str | None = None) -> None:
    match = FOLD_RE.fullmatch(path.name)
    if not match:
        raise RuntimeError(f"Unexpected results checkpoint file: {path.name}")
    task, family, fold_text = match.groups()
    fold_path = PROJECT_ROOT / f"reports/final_v2/gate2/outer_fold_assignments_{task}.csv"
    expected = {
        "task": task,
        "family": family,
        "outer_fold": int(fold_text),
        "gold_sha256": identity["gold_sha256"],
        "development_view_sha256": identity["development_view_sha256"],
        "scientific_config_sha256": sha256_file(config_path),
        "fold_assignment_sha256": sha256_file(fold_path),
    }
    if family in {"M2", "M3"}:
        if not embedding_artifact_sha256:
            raise RuntimeError("Semantic fold checkpoint exists without a COMPLETE embedding identity")
        expected["embedding_artifact_sha256"] = embedding_artifact_sha256
    load_fold_checkpoint(path, expected_identity=expected)


def collect_portable_files(persistent_dir: Path, config_path: Path, identity: dict[str, Any]) -> list[tuple[Path, str]]:
    files: list[tuple[Path, str]] = []
    metadata = validate_embedding_checkpoint(persistent_dir / "embedding_checkpoint", identity)
    embedding_artifact_sha256 = metadata.get("final_artifact_sha256") if metadata else None
    if metadata is not None:
        for name in sorted(EMBEDDING_FILES):
            files.append((persistent_dir / "embedding_checkpoint" / name, f"embedding_checkpoint/{name}"))
    result_dir = persistent_dir / "results"
    if result_dir.exists():
        for path in sorted(result_dir.glob("*_checkpoint.json")):
            _validate_fold(path, config_path, identity, embedding_artifact_sha256)
            files.append((path, f"results/{path.name}"))
        registry = result_dir / "GATE2_RUN_REGISTRY.jsonl"
        if registry.exists():
            files.append((registry, "results/GATE2_RUN_REGISTRY.jsonl"))
    for name in sorted(SAFE_ROOT_FILES):
        path = persistent_dir / name
        if path.exists():
            files.append((path, name))
    for path, arcname in files:
        lowered = arcname.lower()
        if "confirmation" in lowered or SECRET_RE.search(Path(lowered).name) or "huggingface" in lowered or "model" in lowered and "checkpoint" not in lowered:
            raise RuntimeError(f"Prohibited portable checkpoint member: {arcname}")
        if not path.is_file():
            raise RuntimeError(f"Portable checkpoint member is not a regular file: {path}")
        if path.suffix in {".json", ".jsonl"} and SECRET_VALUE_RE.search(path.read_bytes()):
            raise RuntimeError(f"Possible secret value in portable checkpoint member: {arcname}")
    return files


def export_checkpoint(config_path: Path, persistent_dir: Path, archive: Path) -> dict[str, Any]:
    identity = scientific_identity(config_path)
    files = collect_portable_files(persistent_dir, config_path, identity)
    members = [{"path": arcname, "bytes": path.stat().st_size, "sha256": sha256_file(path)} for path, arcname in files]
    manifest = {
        "schema_version": "gate2_portable_checkpoint_v1",
        "scientific_identity": identity,
        "members": members,
        "confirmation_accessed": False,
    }
    manifest["manifest_sha256"] = _canonical_sha(manifest)
    archive.parent.mkdir(parents=True, exist_ok=True)
    temporary = archive.with_suffix(archive.suffix + ".tmp")
    with temporary.open("wb") as raw, gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as compressed, tarfile.open(fileobj=compressed, mode="w") as handle:
        encoded = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")
        info = tarfile.TarInfo("gate2_checkpoint_archive_manifest.json")
        info.size, info.mtime, info.mode = len(encoded), 0, 0o644
        import io
        handle.addfile(info, io.BytesIO(encoded))
        for path, arcname in files:
            info = handle.gettarinfo(str(path), arcname=arcname)
            info.uid = info.gid = info.mtime = 0
            info.uname = info.gname = ""
            info.mode = 0o644
            with path.open("rb") as source:
                handle.addfile(info, source)
    temporary.replace(archive)
    return {"status": "EXPORTED", "archive": str(archive), "archive_sha256": sha256_file(archive), "members": len(members), "confirmation_accessed": False}


def _safe_member(name: str) -> bool:
    path = PurePosixPath(name)
    return bool(name) and not path.is_absolute() and ".." not in path.parts and "\\" not in name


def restore_checkpoint(config_path: Path, persistent_dir: Path, archive: Path) -> dict[str, Any]:
    identity = scientific_identity(config_path)
    if not archive.is_file():
        raise RuntimeError(f"Checkpoint archive does not exist: {archive}")
    with tempfile.TemporaryDirectory(prefix="gate2_restore_") as temp_name:
        temp = Path(temp_name)
        with tarfile.open(archive, "r:gz") as handle:
            members = handle.getmembers()
            if any(not member.isfile() or not _safe_member(member.name) for member in members):
                raise RuntimeError("Checkpoint archive contains an unsafe member")
            for member in members:
                source = handle.extractfile(member)
                if source is None:
                    raise RuntimeError(f"Checkpoint archive member cannot be read: {member.name}")
                destination = temp / Path(member.name)
                destination.parent.mkdir(parents=True, exist_ok=True)
                with destination.open("wb") as output:
                    shutil.copyfileobj(source, output)
        manifest_path = temp / "gate2_checkpoint_archive_manifest.json"
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise RuntimeError("Checkpoint archive manifest is missing or corrupt") from exc
        recorded = manifest.pop("manifest_sha256", None)
        if not recorded or _canonical_sha(manifest) != recorded:
            raise RuntimeError("Checkpoint archive manifest hash mismatch")
        if manifest.get("scientific_identity") != identity:
            raise RuntimeError("Checkpoint archive scientific identity mismatch")
        declared = {entry["path"]: entry for entry in manifest.get("members", [])}
        actual = {member.name for member in members} - {"gate2_checkpoint_archive_manifest.json"}
        if set(declared) != actual:
            raise RuntimeError("Checkpoint archive member set mismatch")
        for name, entry in declared.items():
            path = temp / Path(name)
            if path.stat().st_size != entry["bytes"] or sha256_file(path) != entry["sha256"]:
                raise RuntimeError(f"Checkpoint archive member hash mismatch: {name}")
        restored_metadata = validate_embedding_checkpoint(temp / "embedding_checkpoint", identity)
        for path in sorted((temp / "results").glob("*_checkpoint.json")) if (temp / "results").exists() else []:
            _validate_fold(path, config_path, identity, restored_metadata.get("final_artifact_sha256") if restored_metadata else None)
        managed_roots = [persistent_dir / "embedding_checkpoint", persistent_dir / "results"] + [persistent_dir / name for name in SAFE_ROOT_FILES]
        if any(path.exists() for path in managed_roots):
            raise RuntimeError("Restore target already contains managed Gate 2 state; use an empty persistent directory")
        persistent_dir.mkdir(parents=True, exist_ok=True)
        for name in sorted(actual):
            source = temp / Path(name)
            destination = persistent_dir / Path(name)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
    return {"status": "RESTORED", "archive": str(archive), "members": len(declared), "confirmation_accessed": False}


def verify_checkpoint(config_path: Path, archive: Path) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="gate2_verify_") as temporary:
        result = restore_checkpoint(config_path, Path(temporary) / "verified_state", archive)
    return {**result, "status": "VERIFIED"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Export or restore a verified, protocol-bound Gate 2 checkpoint archive.")
    parser.add_argument("action", choices=["export", "restore", "verify"])
    parser.add_argument("--config", default="configs/final_v2/gate2_model_study.json")
    parser.add_argument("--persistent-dir")
    parser.add_argument("--archive", required=True)
    args = parser.parse_args()
    if args.action == "verify":
        result = verify_checkpoint(Path(args.config), Path(args.archive))
    else:
        if not args.persistent_dir:
            parser.error("--persistent-dir is required for export and restore")
        operation = export_checkpoint if args.action == "export" else restore_checkpoint
        result = operation(Path(args.config), Path(args.persistent_dir), Path(args.archive))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
