from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np

from docguard_ml_v2.gate2_study import load_config, load_development_rows, sha256_file


def run(config_path: Path, embedding_dir: Path, result_dir: Path) -> dict:
    config = load_config(config_path)
    rows, view = load_development_rows(config_path=config_path)
    manifest_path = embedding_dir / "gate2_unixcoder_embeddings_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    artifact = embedding_dir / "gate2_unixcoder_embeddings.npz"
    if sha256_file(artifact) != manifest["artifact_sha256"]:
        raise RuntimeError("Embedding artifact hash mismatch")
    if manifest["gold_sha256"] != view["gold_sha256"] or manifest["development_view_sha256"] != view["development_view_sha256"]:
        raise RuntimeError("Embedding artifact does not match frozen development view")
    if manifest["encoder_revision"] != config["families"]["M2"]["encoder_revision"]:
        raise RuntimeError("Encoder revision mismatch")
    with np.load(artifact, allow_pickle=False) as payload:
        ids = payload["case_ids"].tolist()
        if ids != [str(row["case_id"]) for row in rows]:
            raise RuntimeError("Embedding row order mismatch")
        if payload["code"].shape[0] != len(rows) or payload["docs"].shape != payload["code"].shape:
            raise RuntimeError("Embedding shape mismatch")
    expected = {f"{task}_{family}_summary.json" for task in ("binary", "category") for family in ("M1", "M2", "M3")}
    completed = {path.name: path for path in result_dir.glob("*_M[123]_summary.json")}
    missing = sorted(expected - set(completed))
    if missing:
        raise RuntimeError(f"Missing task-family summaries: {missing}")
    for name in sorted(expected):
        summary = json.loads(completed[name].read_text(encoding="utf-8"))
        if summary.get("confirmation_accessed") is not False or summary.get("development_view_sha256") != view["development_view_sha256"]:
            raise RuntimeError(f"Invalid development-only summary identity: {name}")
    return {"status": "PASS", "embedding_sha256": manifest["artifact_sha256"], "result_files": [str(completed[name]) for name in sorted(expected)], "confirmation_accessed": False}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--embedding-dir", required=True)
    parser.add_argument("--result-dir", required=True)
    args = parser.parse_args()
    print(json.dumps(run(Path(args.config), Path(args.embedding_dir), Path(args.result_dir)), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
