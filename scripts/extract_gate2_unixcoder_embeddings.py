from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np

from docguard_ml_v2.gate2_study import load_config, load_development_rows, safe_code_view, safe_docs_view, sha256_file


def head_tail(ids: list[int], capacity: int) -> tuple[list[int], bool]:
    if len(ids) <= capacity:
        return ids, False
    head = (capacity + 1) // 2
    tail = capacity - head
    return ids[:head] + (ids[-tail:] if tail else []), True


def encode_text(tokenizer: Any, text: str, max_length: int) -> tuple[list[int], int, bool]:
    original = tokenizer.encode(text, add_special_tokens=False)
    capacity = max_length - int(tokenizer.num_special_tokens_to_add(pair=False))
    if capacity < 1:
        raise RuntimeError("Tokenizer special tokens consume the complete input budget")
    kept, truncated = head_tail(original, capacity)
    built = tokenizer.build_inputs_with_special_tokens(kept)
    if len(built) > max_length:
        raise RuntimeError("Constructed UniXcoder input exceeds max_length")
    return built, len(original), truncated


def git_sha() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=PROJECT_ROOT, text=True).strip()


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def checkpoint_identity(*, config: dict[str, Any], view_manifest: dict[str, Any], row_order_sha256: str) -> dict[str, Any]:
    semantic = config["families"]["M2"]
    return {
        "gold_sha256": view_manifest["gold_sha256"],
        "development_view_sha256": view_manifest["development_view_sha256"],
        "row_order_sha256": row_order_sha256,
        "encoder_revision": semantic["encoder_revision"],
        "tokenizer_revision": semantic["tokenizer_revision"],
        "pooling": semantic["pooling"],
        "max_length": int(semantic["max_length"]),
        "dtype": "float32",
    }


def _checkpoint_specs(total_rows: int, hidden_size: int) -> dict[str, tuple[str, tuple[int, ...]]]:
    return {
        "code": ("float32", (total_rows, hidden_size)),
        "docs": ("float32", (total_rows, hidden_size)),
        "code_lengths": ("int32", (total_rows,)),
        "docs_lengths": ("int32", (total_rows,)),
        "code_truncated": ("uint8", (total_rows,)),
        "docs_truncated": ("uint8", (total_rows,)),
    }


def open_embedding_checkpoint(
    checkpoint_dir: Path,
    *,
    identity: dict[str, Any],
    total_rows: int,
    hidden_size: int,
    resume: bool,
) -> tuple[dict[str, Any], dict[str, np.memmap], Path]:
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    metadata_path = checkpoint_dir / "embedding_checkpoint.json"
    specs = _checkpoint_specs(total_rows, hidden_size)
    if metadata_path.exists():
        if not resume:
            raise RuntimeError("Embedding checkpoint exists; pass --resume to verify and continue it")
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        for key, expected in identity.items():
            if metadata.get("identity", {}).get(key) != expected:
                raise RuntimeError(f"Embedding checkpoint identity mismatch: {key}")
        if metadata.get("total_rows") != total_rows or metadata.get("hidden_size") != hidden_size:
            raise RuntimeError("Embedding checkpoint shape identity mismatch")
        if not isinstance(metadata.get("completed_count"), int) or not 0 <= metadata["completed_count"] <= total_rows:
            raise RuntimeError("Embedding checkpoint completed_count is invalid")
        mode = "r+"
    else:
        unexpected = [checkpoint_dir / f"{name}.mmap" for name in specs if (checkpoint_dir / f"{name}.mmap").exists()]
        if unexpected:
            raise RuntimeError("Embedding checkpoint metadata is missing but memmap files exist")
        metadata = {
            "schema_version": "gate2_unixcoder_embedding_checkpoint_v1",
            "status": "IN_PROGRESS",
            "identity": identity,
            "total_rows": total_rows,
            "hidden_size": hidden_size,
            "completed_count": 0,
        }
        mode = "w+"
    arrays: dict[str, np.memmap] = {}
    try:
        for name, (dtype, shape) in specs.items():
            array_path = checkpoint_dir / f"{name}.mmap"
            expected_bytes = int(np.prod(shape)) * np.dtype(dtype).itemsize
            if mode == "r+" and (not array_path.exists() or array_path.stat().st_size != expected_bytes):
                raise ValueError(f"{name}.mmap byte size mismatch")
            arrays[name] = np.memmap(array_path, dtype=dtype, mode=mode, shape=shape)
    except (OSError, ValueError) as exc:
        raise RuntimeError(f"Embedding checkpoint is corrupt or incomplete: {exc}") from exc
    if mode == "w+":
        for array in arrays.values():
            array.flush()
        atomic_write_json(metadata_path, metadata)
    return metadata, arrays, metadata_path


def persist_embedding_chunk(
    *,
    metadata: dict[str, Any],
    metadata_path: Path,
    arrays: dict[str, np.memmap],
    start: int,
    code: np.ndarray,
    docs: np.ndarray,
    code_lengths: np.ndarray,
    docs_lengths: np.ndarray,
    code_truncated: np.ndarray,
    docs_truncated: np.ndarray,
) -> None:
    if start != metadata["completed_count"]:
        raise RuntimeError("Embedding checkpoint append is not contiguous")
    stop = start + len(code)
    if stop > metadata["total_rows"] or docs.shape != code.shape:
        raise RuntimeError("Embedding checkpoint chunk shape mismatch")
    arrays["code"][start:stop] = code
    arrays["docs"][start:stop] = docs
    arrays["code_lengths"][start:stop] = code_lengths
    arrays["docs_lengths"][start:stop] = docs_lengths
    arrays["code_truncated"][start:stop] = code_truncated
    arrays["docs_truncated"][start:stop] = docs_truncated
    for array in arrays.values():
        array.flush()
    metadata["completed_count"] = stop
    atomic_write_json(metadata_path, metadata)


def verify_complete_artifact(*, output_dir: Path, identity: dict[str, Any], expected_rows: int) -> dict[str, Any] | None:
    manifest_path = output_dir / "gate2_unixcoder_embeddings_manifest.json"
    artifact_path = output_dir / "gate2_unixcoder_embeddings.npz"
    if not manifest_path.exists() and not artifact_path.exists():
        return None
    if not manifest_path.exists() or not artifact_path.exists():
        raise RuntimeError("Incomplete final embedding artifact pair")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("status") != "COMPLETE" or manifest.get("development_rows") != expected_rows:
        raise RuntimeError("Final embedding manifest is not COMPLETE")
    for key, expected in identity.items():
        manifest_key = "row_order_sha256" if key == "row_order_sha256" else key
        if manifest.get(manifest_key) != expected:
            raise RuntimeError(f"Final embedding identity mismatch: {key}")
    if sha256_file(artifact_path) != manifest.get("artifact_sha256"):
        raise RuntimeError("Final embedding artifact SHA-256 mismatch")
    return {**manifest, "reused_complete_artifact": True}


def run(config_path: Path, output_dir: Path, batch_size: int, *, checkpoint_dir: Path | None = None, resume: bool = False) -> dict[str, Any]:
    config = load_config(config_path)
    semantic = config["families"]["M2"]
    rows, view_manifest = load_development_rows(config_path=config_path)
    case_ids = np.asarray([str(row["case_id"]) for row in rows])
    repositories = np.asarray([str(row["repository"]).strip().lower() for row in rows])
    row_order_sha = hashlib.sha256(("\n".join(case_ids.tolist()) + "\n").encode("utf-8")).hexdigest()
    identity = checkpoint_identity(config=config, view_manifest=view_manifest, row_order_sha256=row_order_sha)
    output_dir.mkdir(parents=True, exist_ok=True)
    complete = verify_complete_artifact(output_dir=output_dir, identity=identity, expected_rows=len(rows))
    if complete is not None:
        return complete
    try:
        import torch
        import transformers
        from transformers import AutoModel, AutoTokenizer
    except ImportError as exc:
        raise RuntimeError("Install the exact preregistered Transformers/PyTorch stack") from exc
    if not torch.cuda.is_available():
        raise RuntimeError("Gate 2 UniXcoder extraction requires CUDA; use the canonical Colab runbook")
    repository = semantic["encoder_repository"]
    revision = semantic["encoder_revision"]
    max_length = int(semantic["max_length"])
    hf_token = os.environ.get("HF_TOKEN") or None
    tokenizer = AutoTokenizer.from_pretrained(repository, revision=revision, token=hf_token, trust_remote_code=False)
    model = AutoModel.from_pretrained(repository, revision=revision, token=hf_token, trust_remote_code=False)
    model.eval().cuda()
    hidden_size = int(model.config.hidden_size)
    persistent_dir = checkpoint_dir or (output_dir / "checkpoint")
    metadata, arrays, metadata_path = open_embedding_checkpoint(
        persistent_dir,
        identity=identity,
        total_rows=len(rows),
        hidden_size=hidden_size,
        resume=resume,
    )

    def pool(batch_ids: list[list[int]]) -> np.ndarray:
        padded = np.full((len(batch_ids), max_length), int(tokenizer.pad_token_id), dtype=np.int64)
        mask = np.zeros((len(batch_ids), max_length), dtype=np.int64)
        for index, ids in enumerate(batch_ids):
            padded[index, : len(ids)] = ids
            mask[index, : len(ids)] = 1
        input_ids = torch.from_numpy(padded).cuda(non_blocking=True)
        attention_mask = torch.from_numpy(mask).cuda(non_blocking=True)
        with torch.inference_mode():
            hidden = model(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state.float()
            weights = attention_mask.unsqueeze(-1).to(hidden.dtype)
            pooled = (hidden * weights).sum(dim=1) / weights.sum(dim=1).clamp(min=1.0)
        return pooled.cpu().numpy().astype(np.float32, copy=False)

    for start in range(int(metadata["completed_count"]), len(rows), batch_size):
        batch = rows[start : start + batch_size]
        code_ids: list[list[int]] = []
        docs_ids: list[list[int]] = []
        code_lengths: list[int] = []
        docs_lengths: list[int] = []
        code_truncated_flags: list[int] = []
        docs_truncated_flags: list[int] = []
        for row in batch:
            code, code_len, code_truncated = encode_text(tokenizer, safe_code_view(row), max_length)
            docs, docs_len, docs_truncated = encode_text(tokenizer, safe_docs_view(row), max_length)
            code_ids.append(code)
            docs_ids.append(docs)
            code_lengths.append(code_len)
            docs_lengths.append(docs_len)
            code_truncated_flags.append(int(code_truncated))
            docs_truncated_flags.append(int(docs_truncated))
        stop = start + len(batch)
        persist_embedding_chunk(
            metadata=metadata,
            metadata_path=metadata_path,
            arrays=arrays,
            start=start,
            code=pool(code_ids),
            docs=pool(docs_ids),
            code_lengths=np.asarray(code_lengths, dtype=np.int32),
            docs_lengths=np.asarray(docs_lengths, dtype=np.int32),
            code_truncated=np.asarray(code_truncated_flags, dtype=np.uint8),
            docs_truncated=np.asarray(docs_truncated_flags, dtype=np.uint8),
        )
        print(json.dumps({"embedded": stop, "total": len(rows)}), flush=True)

    if metadata["completed_count"] != len(rows):
        raise RuntimeError("Embedding checkpoint did not reach all development rows")
    artifact = output_dir / "gate2_unixcoder_embeddings.npz"
    np.savez_compressed(artifact, case_ids=case_ids, repositories=repositories, code=np.asarray(arrays["code"]), docs=np.asarray(arrays["docs"]))

    def quantiles(values: list[int]) -> dict[str, float]:
        return {name: float(value) for name, value in zip(["p0", "p25", "p50", "p75", "p90", "p95", "p99", "p100"], np.quantile(values, [0, .25, .5, .75, .9, .95, .99, 1]))}

    code_truncated_total = int(np.sum(arrays["code_truncated"]))
    docs_truncated_total = int(np.sum(arrays["docs_truncated"]))
    by_language: dict[str, Counter] = defaultdict(lambda: Counter(rows=0, code_truncated=0, docs_truncated=0))
    for index, row in enumerate(rows):
        language = str(row.get("language") or "unknown").lower()
        by_language[language]["rows"] += 1
        by_language[language]["code_truncated"] += int(arrays["code_truncated"][index])
        by_language[language]["docs_truncated"] += int(arrays["docs_truncated"][index])
    truncation = {
        "rows": len(rows),
        "max_length": max_length,
        "code_truncated_rows": code_truncated_total,
        "docs_truncated_rows": docs_truncated_total,
        "code_truncated_percent": 100.0 * code_truncated_total / len(rows),
        "docs_truncated_percent": 100.0 * docs_truncated_total / len(rows),
        "code_token_length_quantiles": quantiles(np.asarray(arrays["code_lengths"]).tolist()),
        "docs_token_length_quantiles": quantiles(np.asarray(arrays["docs_lengths"]).tolist()),
        "by_language": {key: dict(value) for key, value in sorted(by_language.items())},
    }
    manifest = {
        "status": "COMPLETE",
        **view_manifest,
        "source_commit": git_sha(),
        "encoder_repository": repository,
        "encoder_revision": revision,
        "tokenizer_revision": semantic["tokenizer_revision"],
        "row_order_sha256": row_order_sha,
        "resolved_model_commit_hash": getattr(model.config, "_commit_hash", None),
        "resolved_tokenizer_commit_hash": tokenizer.init_kwargs.get("_commit_hash"),
        "pooling": semantic["pooling"],
        "max_length": max_length,
        "dtype": "float32",
        "device": torch.cuda.get_device_name(0),
        "python": platform.python_version(),
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "hidden_size": hidden_size,
        "relation_dimension": hidden_size * 4 + 1,
        "artifact_path": str(artifact),
        "artifact_sha256": sha256_file(artifact),
        "truncation": truncation,
        "confirmation_accessed": False,
    }
    atomic_write_json(output_dir / "gate2_unixcoder_embeddings_manifest.json", manifest)
    metadata["status"] = "COMPLETE"
    metadata["final_artifact_sha256"] = manifest["artifact_sha256"]
    atomic_write_json(metadata_path, metadata)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/final_v2/gate2_model_study.json")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--checkpoint-dir")
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run(Path(args.config), Path(args.output_dir), args.batch_size, checkpoint_dir=Path(args.checkpoint_dir) if args.checkpoint_dir else None, resume=args.resume), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
