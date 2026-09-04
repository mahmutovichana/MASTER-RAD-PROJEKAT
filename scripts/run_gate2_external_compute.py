from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
import tarfile
import time
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from docguard_ml_v2.gate2_study import load_config, load_development_rows, sha256_file
from scripts.manage_gate2_checkpoint import scientific_identity, validate_embedding_checkpoint
from scripts.verify_gate2_return_artifacts import run as verify_return_artifacts


@dataclass(frozen=True)
class Stage:
    name: str
    action: Callable[[], Any]


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def append_event(path: Path, event: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")


def execute_fail_closed(stages: list[Stage], *, status_path: Path, event_path: Path) -> dict[str, Any]:
    completed: list[str] = []
    for stage in stages:
        append_event(event_path, {"stage": stage.name, "status": "STARTED", "time_unix": time.time()})
        try:
            stage.action()
        except BaseException as exc:
            failure = {
                "status": "FAILED",
                "failed_stage": stage.name,
                "completed_stages": completed,
                "error": str(exc),
                "traceback": traceback.format_exc(),
                "confirmation_accessed": False,
            }
            atomic_json(status_path, failure)
            append_event(event_path, {"stage": stage.name, "status": "FAILED", "time_unix": time.time(), "error": str(exc)})
            raise
        completed.append(stage.name)
        append_event(event_path, {"stage": stage.name, "status": "COMPLETED", "time_unix": time.time()})
    result = {"status": "COMPLETE", "completed_stages": completed, "confirmation_accessed": False}
    atomic_json(status_path, result)
    return result


def checked_python(*arguments: str) -> None:
    subprocess.run([sys.executable, *arguments], cwd=PROJECT_ROOT, check=True)


def complete_embedding_exists(embedding_dir: Path, expected: dict[str, Any]) -> bool:
    manifest_path = embedding_dir / "gate2_unixcoder_embeddings_manifest.json"
    artifact_path = embedding_dir / "gate2_unixcoder_embeddings.npz"
    if not manifest_path.exists() and not artifact_path.exists():
        return False
    if not manifest_path.exists() or not artifact_path.exists():
        raise RuntimeError("Persistent embedding output is incomplete")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("status") != "COMPLETE" or manifest.get("artifact_sha256") != sha256_file(artifact_path):
        raise RuntimeError("Persistent embedding output failed COMPLETE/hash verification")
    for key, value in expected.items():
        if manifest.get(key) != value:
            raise RuntimeError(f"Persistent embedding identity mismatch: {key}")
    return True


def require_embedding_compute(*, complete_artifact: bool, complete_checkpoint: bool, cuda_available: bool) -> bool:
    reusable = complete_artifact or complete_checkpoint
    if not reusable and not cuda_available:
        raise RuntimeError("CUDA GPU is required until the persistent embedding artifact is COMPLETE")
    return reusable


def verify_environment(config: dict[str, Any], embedding_dir: Path, checkpoint_dir: Path, view: dict[str, Any], config_path: Path) -> None:
    import torch
    import transformers
    import tokenizers
    import accelerate
    import huggingface_hub
    import safetensors

    required = config["dependencies"]
    actual = {
        "transformers": transformers.__version__,
        "tokenizers": tokenizers.__version__,
        "accelerate": accelerate.__version__,
        "huggingface_hub": huggingface_hub.__version__,
        "safetensors": safetensors.__version__,
    }
    mismatches = {name: {"required": required[name], "actual": value} for name, value in actual.items() if value != required[name]}
    if mismatches:
        raise RuntimeError(f"External dependency mismatch: {mismatches}")
    semantic = config["families"]["M2"]
    reusable = complete_embedding_exists(embedding_dir, {
        "gold_sha256": view["gold_sha256"],
        "development_view_sha256": view["development_view_sha256"],
        "encoder_revision": semantic["encoder_revision"],
        "tokenizer_revision": semantic["tokenizer_revision"],
        "pooling": semantic["pooling"],
        "max_length": semantic["max_length"],
        "dtype": "float32",
        "development_rows": view["development_rows"],
    })
    checkpoint = validate_embedding_checkpoint(checkpoint_dir, scientific_identity(config_path))
    complete_memmaps = checkpoint is not None and checkpoint.get("status") == "COMPLETE"
    require_embedding_compute(complete_artifact=reusable, complete_checkpoint=complete_memmaps, cuda_available=torch.cuda.is_available())
    print(json.dumps({
        "python": platform.python_version(),
        "torch": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
        "cuda_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        **actual,
        "complete_embeddings_reused": reusable,
        "complete_embedding_checkpoint_reused": complete_memmaps,
    }, indent=2), flush=True)


def package_return(*, archive: Path, embedding_dir: Path, result_dir: Path) -> Path:
    manifest = embedding_dir / "gate2_unixcoder_embeddings_manifest.json"
    verification = result_dir / "return_artifact_verification.json"
    if not manifest.exists() or not verification.exists():
        raise RuntimeError("Verified return metadata is missing")
    archive.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive, "w:gz") as handle:
        handle.add(manifest, arcname="gate2_embeddings/gate2_unixcoder_embeddings_manifest.json")
        for path in sorted(result_dir.rglob("*")):
            if path.is_file():
                handle.add(path, arcname=(Path("gate2_results") / path.relative_to(result_dir)).as_posix())
    return archive


def run(
    config_path: Path,
    persistent_dir: Path,
    *,
    return_archive: Path | None = None,
    candidate_workers: int = 2,
    thread_limit: int = 1,
    heartbeat_seconds: float = 60.0,
) -> dict[str, Any]:
    if candidate_workers < 1 or thread_limit < 1 or heartbeat_seconds < 0:
        raise ValueError("candidate-workers/thread-limit must be >= 1 and heartbeat-seconds must be >= 0")
    config = load_config(config_path)
    _, view = load_development_rows(config_path=config_path)
    embedding_dir = persistent_dir / "embeddings"
    checkpoint_dir = persistent_dir / "embedding_checkpoint"
    result_dir = persistent_dir / "results"
    status_path = persistent_dir / "external_workflow_status.json"
    event_path = persistent_dir / "external_workflow_events.jsonl"
    result_dir.mkdir(parents=True, exist_ok=True)

    def verify_return() -> None:
        result = verify_return_artifacts(config_path, embedding_dir, result_dir)
        atomic_json(result_dir / "return_artifact_verification.json", result)

    stages = [
        Stage("gate1_freeze_verifier", lambda: checked_python("scripts/verify_final_v2_gold_freeze.py")),
        Stage("external_environment_verifier", lambda: verify_environment(config, embedding_dir, checkpoint_dir, view, config_path)),
        Stage("development_only_loader", lambda: load_development_rows(config_path=config_path)),
        Stage("unixcoder_embedding_resume", lambda: checked_python("scripts/extract_gate2_unixcoder_embeddings.py", "--config", str(config_path), "--output-dir", str(embedding_dir), "--checkpoint-dir", str(checkpoint_dir), "--resume")),
        Stage("preregistered_M1_M2_M3_resume", lambda: checked_python("scripts/run_gate2_model_study.py", "--config", str(config_path), "--embedding-dir", str(embedding_dir), "--output-dir", str(result_dir), "--families", "M1", "M2", "M3", "--resume", "--candidate-workers", str(candidate_workers), "--thread-limit", str(thread_limit), "--heartbeat-seconds", str(heartbeat_seconds))),
        Stage("return_artifact_verifier", verify_return),
        Stage("final_packaging", lambda: package_return(archive=return_archive or (persistent_dir / "gate2_colab_return.tar.gz"), embedding_dir=embedding_dir, result_dir=result_dir)),
    ]
    return execute_fail_closed(stages, status_path=status_path, event_path=event_path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Fail-closed and resumable Final V2 Gate 2 external compute workflow.")
    parser.add_argument("--config", default="configs/final_v2/gate2_model_study.json")
    parser.add_argument("--persistent-dir", required=True)
    parser.add_argument("--return-archive", help="Final verified return archive path (packaged only after all verifiers pass).")
    parser.add_argument("--candidate-workers", type=int, default=2)
    parser.add_argument("--thread-limit", type=int, default=1)
    parser.add_argument("--heartbeat-seconds", type=float, default=60.0)
    args = parser.parse_args()
    try:
        result = run(
            Path(args.config),
            Path(args.persistent_dir),
            return_archive=Path(args.return_archive) if args.return_archive else None,
            candidate_workers=args.candidate_workers,
            thread_limit=args.thread_limit,
            heartbeat_seconds=args.heartbeat_seconds,
        )
    except BaseException as exc:
        print(json.dumps({"status": "FAILED", "error": str(exc)}, indent=2), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
