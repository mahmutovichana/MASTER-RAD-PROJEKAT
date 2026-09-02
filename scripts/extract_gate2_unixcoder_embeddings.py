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


def run(config_path: Path, output_dir: Path, batch_size: int) -> dict[str, Any]:
    try:
        import torch
        import transformers
        from transformers import AutoModel, AutoTokenizer
    except ImportError as exc:
        raise RuntimeError("Install the exact preregistered Transformers/PyTorch stack") from exc
    if not torch.cuda.is_available():
        raise RuntimeError("Gate 2 UniXcoder extraction requires CUDA; use the canonical Colab runbook")
    config = load_config(config_path)
    semantic = config["families"]["M2"]
    rows, view_manifest = load_development_rows(config_path=config_path)
    repository = semantic["encoder_repository"]
    revision = semantic["encoder_revision"]
    max_length = int(semantic["max_length"])
    hf_token = os.environ.get("HF_TOKEN") or None
    tokenizer = AutoTokenizer.from_pretrained(repository, revision=revision, token=hf_token, trust_remote_code=False)
    model = AutoModel.from_pretrained(repository, revision=revision, token=hf_token, trust_remote_code=False)
    model.eval().cuda()
    hidden_size = int(model.config.hidden_size)
    code_embeddings = np.empty((len(rows), hidden_size), dtype=np.float32)
    docs_embeddings = np.empty((len(rows), hidden_size), dtype=np.float32)
    stats: dict[str, Any] = {
        "max_length": max_length,
        "code_original_lengths": [],
        "docs_original_lengths": [],
        "code_truncated": 0,
        "docs_truncated": 0,
        "by_language": defaultdict(lambda: Counter(rows=0, code_truncated=0, docs_truncated=0)),
    }

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

    for start in range(0, len(rows), batch_size):
        batch = rows[start : start + batch_size]
        code_ids: list[list[int]] = []
        docs_ids: list[list[int]] = []
        for row in batch:
            code, code_len, code_truncated = encode_text(tokenizer, safe_code_view(row), max_length)
            docs, docs_len, docs_truncated = encode_text(tokenizer, safe_docs_view(row), max_length)
            code_ids.append(code)
            docs_ids.append(docs)
            stats["code_original_lengths"].append(code_len)
            stats["docs_original_lengths"].append(docs_len)
            stats["code_truncated"] += int(code_truncated)
            stats["docs_truncated"] += int(docs_truncated)
            language = str(row.get("language") or "unknown").lower()
            stats["by_language"][language]["rows"] += 1
            stats["by_language"][language]["code_truncated"] += int(code_truncated)
            stats["by_language"][language]["docs_truncated"] += int(docs_truncated)
        stop = start + len(batch)
        code_embeddings[start:stop] = pool(code_ids)
        docs_embeddings[start:stop] = pool(docs_ids)
        print(json.dumps({"embedded": stop, "total": len(rows)}), flush=True)

    output_dir.mkdir(parents=True, exist_ok=True)
    artifact = output_dir / "gate2_unixcoder_embeddings.npz"
    case_ids = np.asarray([str(row["case_id"]) for row in rows])
    repositories = np.asarray([str(row["repository"]).strip().lower() for row in rows])
    np.savez_compressed(artifact, case_ids=case_ids, repositories=repositories, code=code_embeddings, docs=docs_embeddings)
    row_order_sha = hashlib.sha256(("\n".join(case_ids.tolist()) + "\n").encode("utf-8")).hexdigest()

    def quantiles(values: list[int]) -> dict[str, float]:
        return {name: float(value) for name, value in zip(["p0", "p25", "p50", "p75", "p90", "p95", "p99", "p100"], np.quantile(values, [0, .25, .5, .75, .9, .95, .99, 1]))}

    truncation = {
        "rows": len(rows),
        "max_length": max_length,
        "code_truncated_rows": stats["code_truncated"],
        "docs_truncated_rows": stats["docs_truncated"],
        "code_truncated_percent": 100.0 * stats["code_truncated"] / len(rows),
        "docs_truncated_percent": 100.0 * stats["docs_truncated"] / len(rows),
        "code_token_length_quantiles": quantiles(stats["code_original_lengths"]),
        "docs_token_length_quantiles": quantiles(stats["docs_original_lengths"]),
        "by_language": {key: dict(value) for key, value in sorted(stats["by_language"].items())},
    }
    manifest = {
        "status": "COMPLETE",
        **view_manifest,
        "source_commit": git_sha(),
        "encoder_repository": repository,
        "encoder_revision": revision,
        "tokenizer_revision": semantic["tokenizer_revision"],
        "resolved_model_commit_hash": getattr(model.config, "_commit_hash", None),
        "resolved_tokenizer_commit_hash": tokenizer.init_kwargs.get("_commit_hash"),
        "pooling": semantic["pooling"],
        "dtype": "float32",
        "device": torch.cuda.get_device_name(0),
        "python": platform.python_version(),
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "hidden_size": hidden_size,
        "relation_dimension": hidden_size * 4 + 1,
        "row_order_sha256": row_order_sha,
        "artifact_path": str(artifact),
        "artifact_sha256": sha256_file(artifact),
        "truncation": truncation,
        "confirmation_accessed": False,
    }
    (output_dir / "gate2_unixcoder_embeddings_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/final_v2/gate2_model_study.json")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--batch-size", type=int, default=16)
    args = parser.parse_args()
    print(json.dumps(run(Path(args.config), Path(args.output_dir), args.batch_size), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
