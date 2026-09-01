"""Prepare the configuration-vs-developer_setup specialist Colab pilot.

Local work is intentionally limited to a small train-only export, a
self-contained Colab notebook, and lightweight tests/manifests. The specialist
OOF experiment must be executed on Colab GPU, not locally.
"""
from __future__ import annotations

import ast
import hashlib
import json
import re
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE_TRAIN_PATH = ROOT / "data" / "final_v2" / "architecture_challenge_v1" / "natural_train_primary_four.jsonl"
EXPORT_DIR = ROOT / "data" / "final_v2" / "configuration_setup_specialist_v1"
EXPORT_JSONL = EXPORT_DIR / "natural_train_configuration_setup.jsonl"
EXPORT_MANIFEST = EXPORT_DIR / "export_manifest.json"
NOTEBOOK_PATH = ROOT / "notebooks" / "category_configuration_vs_developer_setup_specialist_v1.ipynb"
OUTPUT_DIR = ROOT / "experiments" / "category_hierarchy_pilot_v1" / "configuration_vs_developer_setup"

LABELS = ["configuration", "developer_setup"]
SAFE_FIELDS = [
    "case_id",
    "repository",
    "language",
    "code_changed_files",
    "code_diff_excerpt",
    "docs_before_excerpt",
    "gold_doc_category",
    "partition",
]
FORBIDDEN_EXPORT_FIELDS = {
    "controlled_design_label",
    "controlled_design_supervision",
    "docs_after",
    "docs_after_excerpt",
    "docs_diff",
    "docs_diff_excerpt",
    "human_doc_category",
    "human_docs_update_required",
    "human_label_notes",
    "independent_human_reviewed",
    "label_source",
    "owner_accepted_for_training",
    "pr_number",
    "provenance_tier",
    "repository_full_name_for_model",
    "review_status",
    "suggested_doc_category",
    "suggested_docs_update_required",
    "suggested_notes",
    "supervision_source",
}

EXPECTED_COUNTS = {"configuration": 277, "developer_setup": 88}
EXPECTED_TOTAL = 365
SOURCE_TRAIN_SHA256 = "9dc1136f1cf695eb69c70b763ad051898aa5fae351fcf028eed97116c8891f99"

MINILM_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
MINILM_MODEL_REVISION = "1110a243fdf4706b3f48f1d95db1a4f5529b4d41"
SENTENCE_TRANSFORMERS_VERSION = "5.1.2"
TRANSFORMERS_VERSION = "4.56.2"
TOKENIZERS_VERSION = "0.22.0"
HUGGINGFACE_HUB_VERSION = "0.34.4"
ACCELERATE_VERSION = "1.10.1"
SCIKIT_LEARN_VERSION = "1.7.2"
MATPLOTLIB_VERSION = "3.10.6"

CURRENT_HYBRID_CONFIG = {
    "semantic_encoder": {
        "model_name": MINILM_MODEL_NAME,
        "revision": MINILM_MODEL_REVISION,
        "chunk_chars": 1000,
        "max_chunks_per_side": 2,
        "normalize_embeddings": True,
        "chunk_pooling": "mean of normalized chunk embeddings, then renormalize",
    },
    "lexical_code_channel": {
        "vectorizer": "TfidfVectorizer",
        "analyzer": "char_wb",
        "ngram_range": [3, 5],
        "min_df": 2,
        "max_features": 20000,
        "sublinear_tf": True,
        "dtype": "np.float32",
        "fit_policy": "fit on each OOF fold-train only; transform fold-eval only",
    },
    "semantic_relational_features": [
        "E_code",
        "E_docs",
        "abs(E_code - E_docs)",
        "E_code * E_docs",
        "cosine(E_code, E_docs)",
    ],
    "lexical_scalar_features": [
        "log1p(shared code/docs token count)",
        "shared / union token ratio",
        "shared / min(code token count, docs token count)",
        "identifier overlap ratio",
        "changed-path token overlap ratio",
        "log1p(code text length)",
        "log1p(docs text length)",
    ],
    "classifier": {
        "class": "LogisticRegression",
        "C": 1.0,
        "solver": "lbfgs",
        "max_iter": 2000,
        "random_state": 42,
        "class_weight": None,
        "threshold": 0.5,
        "resampling": None,
    },
}


def reject_forbidden_path(path: Path) -> None:
    normalized = str(path).replace("\\", "/").lower()
    forbidden = ["validation", "confirmation", "refresh"]
    if any(word in normalized for word in forbidden):
        raise ValueError(f"Forbidden validation/confirmation/refresh path: {path}")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def stable_json_hash(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    reject_forbidden_path(path)
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_number}: row is not an object")
            if str(row.get("partition") or "").lower() != "development_train":
                raise ValueError(f"{path}:{line_number}: only development_train is allowed")
            rows.append(row)
    return rows


def export_row(row: dict[str, Any]) -> dict[str, Any]:
    if row.get("gold_doc_category") not in LABELS:
        raise ValueError(f"{row.get('case_id')}: specialist export allows only {LABELS}")
    if str(row.get("partition") or "") != "development_train":
        raise ValueError(f"{row.get('case_id')}: validation/refresh/confirmation rows are forbidden")
    if row.get("controlled_design_supervision") is True:
        raise ValueError(f"{row.get('case_id')}: controlled row is forbidden")
    for field in ("label_source", "supervision_source", "provenance_tier"):
        value = str(row.get(field) or "").lower()
        if "controlled" in value or "synthetic" in value:
            raise ValueError(f"{row.get('case_id')}: controlled/synthetic provenance is forbidden")
    exported = {field: row.get(field) for field in SAFE_FIELDS}
    if set(exported) != set(SAFE_FIELDS):
        raise AssertionError("specialist export schema mismatch")
    if set(exported) & FORBIDDEN_EXPORT_FIELDS:
        raise AssertionError("forbidden field entered specialist export")
    return exported


def load_and_build_export() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if sha256_file(SOURCE_TRAIN_PATH) != SOURCE_TRAIN_SHA256:
        raise AssertionError("Frozen Architecture Challenge V1 train file hash changed")
    source_rows = read_jsonl(SOURCE_TRAIN_PATH)
    selected = [export_row(row) for row in source_rows if row.get("gold_doc_category") in LABELS]
    counts = dict(Counter(row["gold_doc_category"] for row in selected))
    if len(selected) != EXPECTED_TOTAL:
        raise AssertionError(f"Expected {EXPECTED_TOTAL} rows, got {len(selected)}")
    if counts != EXPECTED_COUNTS:
        raise AssertionError(f"Expected {EXPECTED_COUNTS}, got {counts}")
    repositories = {str(row["repository"]) for row in selected}
    manifest = {
        "schema": "configuration_setup_specialist_v1_export",
        "created_at": datetime.now(UTC).isoformat(),
        "purpose": "train-only repository-grouped OOF pilot for configuration vs developer_setup",
        "source": {
            "path": str(SOURCE_TRAIN_PATH.relative_to(ROOT)),
            "sha256": SOURCE_TRAIN_SHA256,
            "source_rows": len(source_rows),
        },
        "artifacts": {
            "natural_train_configuration_setup.jsonl": {
                "path": str(EXPORT_JSONL.relative_to(ROOT)),
            }
        },
        "row_count": len(selected),
        "category_counts": counts,
        "repository_count": len(repositories),
        "language_counts": dict(sorted(Counter(str(row.get("language") or "unknown").lower() for row in selected).items())),
        "safe_fields": SAFE_FIELDS,
        "forbidden_fields_excluded": sorted(FORBIDDEN_EXPORT_FIELDS),
        "confirmation_accessed": False,
        "frozen_322_validation_accessed": False,
        "development_validation_rows_used": False,
        "refresh_validation_rows_used": False,
        "controlled_or_synthetic_rows_used": False,
        "repository_identity_for_grouping_only": True,
        "current_hybrid_config": CURRENT_HYBRID_CONFIG,
    }
    return selected, manifest


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def py_source(value: Any) -> str:
    return repr(value)


def nb_cell(cell_type: str, source: str) -> dict[str, Any]:
    return {
        "cell_type": cell_type,
        "metadata": {},
        "source": [line + "\n" for line in source.strip("\n").splitlines()],
        **({"outputs": [], "execution_count": None} if cell_type == "code" else {}),
    }


def make_notebook() -> dict[str, Any]:
    title = """
# Configuration vs developer_setup specialist pilot V1

This Colab notebook runs a train-only repository-grouped out-of-fold specialist pilot. It uses only the small specialist export with `configuration` and `developer_setup` development-training rows. It must not load the frozen 322-row development validation.
"""
    deps = f"""
# Python 3.13 compatible Colab stack. Keep Colab's CUDA-enabled torch.
# sentence-transformers==6.0.1 conflicts with transformers==4.56.2, so this notebook uses 5.1.2.
!python -m pip install -q \\
  "sentence-transformers=={SENTENCE_TRANSFORMERS_VERSION}" \\
  "transformers=={TRANSFORMERS_VERSION}" \\
  "tokenizers=={TOKENIZERS_VERSION}" \\
  "huggingface_hub=={HUGGINGFACE_HUB_VERSION}" \\
  "accelerate=={ACCELERATE_VERSION}" \\
  "scikit-learn=={SCIKIT_LEARN_VERSION}" \\
  "matplotlib=={MATPLOTLIB_VERSION}" \\
  "scipy"
"""
    imports = """
from __future__ import annotations

import hashlib
import json
import math
import os
import random
import re
import shutil
import sys
import time
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import scipy
import sklearn
import torch
import tokenizers
import transformers
from huggingface_hub import HfApi, __version__ as hf_hub_version
from scipy import sparse
from sentence_transformers import SentenceTransformer, __version__ as sentence_transformers_version
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
)
from sklearn.model_selection import StratifiedGroupKFold

print("Python:", sys.version)
print("torch:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
print("GPU name:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "NONE")
print("transformers:", transformers.__version__)
print("tokenizers:", tokenizers.__version__)
print("sentence-transformers:", sentence_transformers_version)
print("scikit-learn:", sklearn.__version__)
assert torch.cuda.is_available() == True
"""
    constants = f"""
REQUIRED_FILES = ["natural_train_configuration_setup.jsonl", "export_manifest.json"]
LABELS = {py_source(LABELS)}
SAFE_FIELDS = {py_source(SAFE_FIELDS)}
EXPECTED_COUNTS = {py_source(EXPECTED_COUNTS)}
EXPECTED_TOTAL = {EXPECTED_TOTAL}
SEED = 42

MINILM_MODEL_NAME = "{MINILM_MODEL_NAME}"
MINILM_MODEL_REVISION = "{MINILM_MODEL_REVISION}"
CHUNK_CHARS = 1000
MAX_CHUNKS = 2
EMBEDDING_BATCH_SIZE = 64

OUTPUT_DIR = Path("/content/experiments/category_hierarchy_pilot_v1/configuration_vs_developer_setup")
CACHE_DIR = OUTPUT_DIR / "cache"
FIGURES_DIR = OUTPUT_DIR / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
"""
    load_data = """
def reject_supplied_path(path):
    lowered = str(path).replace("\\\\", "/").lower()
    if any(word in lowered for word in ["validation", "confirmation", "refresh"]):
        raise ValueError(f"Forbidden supplied path/file name for train-only specialist pilot: {path}")


def has_export(root):
    export_dir = Path(root) / "data" / "final_v2" / "configuration_setup_specialist_v1"
    return all((export_dir / name).exists() for name in REQUIRED_FILES)


def locate_export_root():
    candidates = [
        Path.cwd(),
        Path("/content/MASTER-RAD-PROJEKAT"),
        Path("/content/MASTER RAD PROJEKAT"),
        Path("/content/drive/MyDrive/MASTER-RAD-PROJEKAT"),
        Path("/content/drive/MyDrive/MASTER RAD PROJEKAT"),
    ]
    for candidate in candidates:
        if has_export(candidate):
            return candidate
    for manifest in Path("/content").glob("**/export_manifest.json"):
        if "configuration_setup_specialist_v1" not in manifest.as_posix():
            continue
        possible_root = manifest.parent.parent.parent.parent
        if has_export(possible_root):
            return possible_root
    return None


ROOT = locate_export_root()
if ROOT is None:
    print("Specialist export nije pronađen. Uploaduj ZIP repozitorija ili samo ova dva fajla:")
    for name in REQUIRED_FILES:
        print("-", name)
    from google.colab import files

    uploaded = files.upload()
    upload_root = Path("/content/MASTER-RAD-PROJEKAT")
    export_dir = upload_root / "data" / "final_v2" / "configuration_setup_specialist_v1"
    export_dir.mkdir(parents=True, exist_ok=True)
    for name, payload in uploaded.items():
        reject_supplied_path(name)
        base = Path(name).name
        if base.lower().endswith(".zip"):
            zip_path = upload_root / base
            zip_path.write_bytes(payload)
            with zipfile.ZipFile(zip_path) as archive:
                for member in archive.namelist():
                    reject_supplied_path(member)
                archive.extractall(upload_root)
        elif base in REQUIRED_FILES:
            (export_dir / base).write_bytes(payload)
        else:
            print(f"Skipping unrelated uploaded file: {name}")
    ROOT = locate_export_root()

assert ROOT is not None and has_export(ROOT), "Missing train-only specialist export."
EXPORT_DIR = ROOT / "data" / "final_v2" / "configuration_setup_specialist_v1"
DATA_PATH = EXPORT_DIR / "natural_train_configuration_setup.jsonl"
MANIFEST_PATH = EXPORT_DIR / "export_manifest.json"
for path in [DATA_PATH, MANIFEST_PATH]:
    reject_supplied_path(path.name)
print("Using specialist export:", EXPORT_DIR)
"""
    helpers = r'''
def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def stable_json_hash(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def read_jsonl(path):
    reject_supplied_path(path.name)
    rows = []
    with open(path, encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("partition") != "development_train":
                raise ValueError(f"{path}:{line_number}: only development_train allowed")
            rows.append(row)
    return rows


def list_value(value):
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, str):
        text = value.strip()
        if text.startswith("["):
            try:
                parsed = json.loads(text)
                if isinstance(parsed, list):
                    return [str(item) for item in parsed]
            except json.JSONDecodeError:
                pass
        return [text] if text else []
    return []


def sanitize_repository_identity(text, repository):
    repo = str(repository or "").strip().strip("/")
    sanitized = str(text)
    if not repo or "/" not in repo:
        return sanitized
    owner, name = repo.split("/", 1)
    patterns = [
        re.escape(repo),
        re.escape(f"github.com/{repo}"),
        re.escape(f"https://github.com/{repo}"),
        re.escape(f"http://github.com/{repo}"),
        re.escape(f"git@github.com:{repo}"),
    ]
    for pattern in patterns:
        sanitized = re.sub(pattern, "[REPOSITORY]", sanitized, flags=re.IGNORECASE)
    return re.sub(rf"github\.com/{re.escape(owner)}/{re.escape(name)}(?:\.git)?", "[REPOSITORY]", sanitized, flags=re.IGNORECASE)


def build_code_text(row):
    text = "\n".join([
        f"language: {str(row.get('language') or 'unknown').lower()}",
        "changed files:",
        "\n".join(list_value(row.get("code_changed_files"))),
        "code change:",
        str(row.get("code_diff_excerpt") or ""),
    ])
    return sanitize_repository_identity(text, row.get("repository") or "")


def build_docs_text(row):
    return sanitize_repository_identity(row.get("docs_before_excerpt") or "", row.get("repository") or "")


def deterministic_chunks(text, chunk_chars=CHUNK_CHARS, max_chunks=MAX_CHUNKS):
    normalized = re.sub(r"\x00", " ", str(text or "")).strip()
    if not normalized:
        return ["[empty]"]
    if len(normalized) <= chunk_chars:
        return [normalized]
    starts = np.linspace(0, max(0, len(normalized) - chunk_chars), num=max_chunks, dtype=int)
    return [normalized[int(start): int(start) + chunk_chars] for start in starts]


def embedding_cache_key(side, texts):
    return stable_json_hash({
        "model": MINILM_MODEL_NAME,
        "revision": MINILM_MODEL_REVISION,
        "side": side,
        "chunk_chars": CHUNK_CHARS,
        "max_chunks": MAX_CHUNKS,
        "normalize_embeddings": True,
        "content_hash": stable_json_hash(texts),
    })


def encode_texts_cached(side, texts, encoder, batch_size=EMBEDDING_BATCH_SIZE):
    key = embedding_cache_key(side, texts)
    target = CACHE_DIR / f"{side}_embeddings.npy"
    metadata = CACHE_DIR / f"{side}_embeddings.json"
    if target.exists() and metadata.exists():
        return np.load(target), json.loads(metadata.read_text(encoding="utf-8")) | {"cache_hit": True}
    chunks, owners = [], []
    for row_index, text in enumerate(texts):
        for chunk in deterministic_chunks(text):
            chunks.append(chunk)
            owners.append(row_index)
    started = time.time()
    current_batch = batch_size
    while True:
        try:
            with torch.inference_mode():
                chunk_vectors = encoder.encode(chunks, batch_size=current_batch, show_progress_bar=True, convert_to_numpy=True, normalize_embeddings=True, device="cuda").astype(np.float32)
            break
        except torch.cuda.OutOfMemoryError:
            torch.cuda.empty_cache()
            if current_batch <= 1:
                raise RuntimeError("MiniLM embedding extraction OOM at batch_size=1; stop and report.")
            current_batch = max(1, current_batch // 2)
            print("OOM during embedding extraction; retrying with batch_size=", current_batch)
    output = np.zeros((len(texts), chunk_vectors.shape[1]), dtype=np.float32)
    counts = np.zeros(len(texts), dtype=np.float32)
    for owner, vector in zip(owners, chunk_vectors):
        output[owner] += vector
        counts[owner] += 1.0
    output /= np.maximum(counts[:, None], 1.0)
    norms = np.linalg.norm(output, axis=1, keepdims=True)
    output /= np.maximum(norms, 1e-12)
    np.save(target, output)
    meta = {
        "side": side,
        "row_count": len(texts),
        "chunk_count": len(chunks),
        "embedding_dimension": int(output.shape[1]),
        "batch_size_used": int(current_batch),
        "elapsed_seconds": time.time() - started,
        "cache_file": str(target),
        "cache_bytes": int(target.stat().st_size),
        "cache_hit": False,
    }
    metadata.write_text(json.dumps(meta, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output, meta


TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{1,}")


def token_set(text):
    return {token.lower() for token in TOKEN_RE.findall(text)}


def lexical_relational_scalars(rows):
    values = []
    for row in rows:
        code_text = build_code_text(row)
        docs_text = build_docs_text(row)
        code_tokens = token_set(code_text)
        docs_tokens = token_set(docs_text)
        shared = code_tokens & docs_tokens
        union = code_tokens | docs_tokens
        identifiers = {token for token in code_tokens if "_" in token or any(char.isupper() for char in token)}
        path_tokens = token_set(" ".join(list_value(row.get("code_changed_files"))))
        values.append([
            math.log1p(len(shared)),
            len(shared) / max(1, len(union)),
            len(shared) / max(1, min(len(code_tokens), len(docs_tokens))),
            len(identifiers & docs_tokens) / max(1, len(identifiers)),
            len(path_tokens & docs_tokens) / max(1, len(path_tokens)),
            math.log1p(len(code_text)),
            math.log1p(len(docs_text)),
        ])
    return np.asarray(values, dtype=np.float32)


def relational_semantic_features(code, docs):
    if code.shape != docs.shape:
        raise ValueError(f"Embedding shape mismatch: {code.shape} vs {docs.shape}")
    cosine = np.sum(code * docs, axis=1, keepdims=True)
    return np.hstack([code, docs, np.abs(code - docs), code * docs, cosine]).astype(np.float32)


def labels_for(rows):
    return np.asarray([row["gold_doc_category"] for row in rows])


def make_classifier():
    return LogisticRegression(C=1.0, solver="lbfgs", max_iter=2000, random_state=SEED)


def probabilities(model, features):
    raw = np.asarray(model.predict_proba(features), dtype=float)
    output = np.zeros((raw.shape[0], len(LABELS)), dtype=float)
    for source_index, label in enumerate(map(str, model.classes_)):
        output[:, LABELS.index(label)] = raw[:, source_index]
    return output


def metric_bundle(y_true, y_pred):
    precision, recall, f1, support = precision_recall_fscore_support(y_true, y_pred, labels=LABELS, zero_division=0)
    matrix = confusion_matrix(y_true, y_pred, labels=LABELS)
    normalized = matrix.astype(float) / np.maximum(matrix.sum(axis=1, keepdims=True), 1)
    return {
        "support": int(len(y_true)),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, labels=LABELS, average="macro", zero_division=0)),
        "weighted_f1": float(f1_score(y_true, y_pred, labels=LABELS, average="weighted", zero_division=0)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "per_class": {
            label: {
                "precision": float(precision[index]),
                "recall": float(recall[index]),
                "f1": float(f1[index]),
                "support": int(support[index]),
            }
            for index, label in enumerate(LABELS)
        },
        "confusion_matrix": matrix.tolist(),
        "normalized_confusion_matrix": normalized.tolist(),
        "predicted_class_counts": dict(sorted(Counter(map(str, y_pred)).items())),
    }


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
'''
    integrity = """
manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
rows = read_jsonl(DATA_PATH)
assert len(rows) == EXPECTED_TOTAL
assert Counter(row["gold_doc_category"] for row in rows) == EXPECTED_COUNTS
assert set(row["partition"] for row in rows) == {"development_train"}
assert all(set(row) == set(SAFE_FIELDS) for row in rows)
assert sha256_file(DATA_PATH) == manifest["artifacts"]["natural_train_configuration_setup.jsonl"]["sha256"]
assert manifest["row_count"] == EXPECTED_TOTAL
assert manifest["category_counts"] == EXPECTED_COUNTS
assert manifest["confirmation_accessed"] is False
assert manifest["frozen_322_validation_accessed"] is False
assert manifest["development_validation_rows_used"] is False
assert manifest["refresh_validation_rows_used"] is False
assert manifest["controlled_or_synthetic_rows_used"] is False
for row in rows[:20]:
    combined = (build_code_text(row) + "\\n" + build_docs_text(row)).lower()
    repo = str(row.get("repository") or "").lower()
    if repo and "/" in repo:
        assert repo not in combined
print("Train-only specialist export verified:", manifest["category_counts"])
"""
    load_encoder = """
model_info = HfApi().model_info(MINILM_MODEL_NAME, revision=MINILM_MODEL_REVISION)
resolved_minilm_sha = model_info.sha
print("Resolved MiniLM revision:", resolved_minilm_sha)
assert resolved_minilm_sha == MINILM_MODEL_REVISION

load_started = time.time()
encoder = SentenceTransformer(
    MINILM_MODEL_NAME,
    revision=MINILM_MODEL_REVISION,
    device="cuda",
)
encoder.eval()
if hasattr(encoder, "parameters"):
    for parameter in encoder.parameters():
        parameter.requires_grad_(False)
assert all(not parameter.requires_grad for parameter in encoder.parameters())

code_sample = build_code_text(rows[0])
docs_sample = build_docs_text(rows[0])
with torch.inference_mode():
    sample_embeddings = encoder.encode([code_sample, docs_sample], batch_size=2, convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=False, device="cuda")
    duplicate_a = encoder.encode(["duplicate deterministic smoke"], batch_size=1, convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=False, device="cuda")
    duplicate_b = encoder.encode(["duplicate deterministic smoke"], batch_size=1, convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=False, device="cuda")
assert np.all(np.isfinite(sample_embeddings))
assert sample_embeddings.shape[0] == 2 and sample_embeddings.shape[1] > 0
assert np.allclose(np.linalg.norm(sample_embeddings, axis=1), 1.0, atol=1e-3)
assert np.allclose(duplicate_a, duplicate_b, atol=1e-5)
print({"embedding_dim": int(sample_embeddings.shape[1]), "smoke_seconds": time.time() - load_started})
"""
    embeddings = """
code_texts = [build_code_text(row) for row in rows]
docs_texts = [build_docs_text(row) for row in rows]
all_code_embeddings, code_cache = encode_texts_cached("all_code", code_texts, encoder)
all_docs_embeddings, docs_cache = encode_texts_cached("all_docs", docs_texts, encoder)
assert all_code_embeddings.shape[0] == len(rows)
assert all_docs_embeddings.shape[0] == len(rows)
assert all_code_embeddings.shape == all_docs_embeddings.shape
"""
    oof = """
def choose_grouped_folds(rows):
    y = labels_for(rows)
    groups = np.asarray([row["repository"] for row in rows])
    for n_splits in [5, 4, 3]:
        splitter = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=SEED)
        candidate = []
        valid = True
        for train_idx, eval_idx in splitter.split(np.arange(len(rows)), y, groups):
            if set(groups[train_idx]) & set(groups[eval_idx]):
                valid = False
            if set(y[train_idx]) != set(LABELS) or set(y[eval_idx]) != set(LABELS):
                valid = False
            candidate.append((train_idx, eval_idx))
        if valid:
            return n_splits, candidate
    raise RuntimeError("No valid StratifiedGroupKFold split with 5/4/3 folds.")


def build_fold_features(train_idx, eval_idx):
    train_rows = [rows[int(i)] for i in train_idx]
    eval_rows = [rows[int(i)] for i in eval_idx]
    code_vectorizer = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(3, 5),
        min_df=2,
        max_features=20000,
        sublinear_tf=True,
        dtype=np.float32,
    )
    code_train = code_vectorizer.fit_transform([build_code_text(row) for row in train_rows])
    code_eval = code_vectorizer.transform([build_code_text(row) for row in eval_rows])
    train_semantic = relational_semantic_features(all_code_embeddings[train_idx], all_docs_embeddings[train_idx])
    eval_semantic = relational_semantic_features(all_code_embeddings[eval_idx], all_docs_embeddings[eval_idx])
    x_train = sparse.hstack([code_train, sparse.csr_matrix(train_semantic), sparse.csr_matrix(lexical_relational_scalars(train_rows))], format="csr")
    x_eval = sparse.hstack([code_eval, sparse.csr_matrix(eval_semantic), sparse.csr_matrix(lexical_relational_scalars(eval_rows))], format="csr")
    return x_train, x_eval, {"code_vocabulary_size": len(code_vectorizer.vocabulary_), "vectorizer_fit_rows": len(train_rows), "fold_eval_never_enters_vectorizer_fit": True}


n_splits, folds = choose_grouped_folds(rows)
y_all = labels_for(rows)
oof_predictions = [None] * len(rows)
oof_probabilities = np.zeros((len(rows), len(LABELS)), dtype=float)
fold_metrics = []
fold_manifest = {"n_splits": n_splits, "folds": [], "splitter": "StratifiedGroupKFold", "seed": SEED}

for fold_id, (train_idx, eval_idx) in enumerate(folds, 1):
    x_train, x_eval, feature_meta = build_fold_features(train_idx, eval_idx)
    train_rows_fold = [rows[int(i)] for i in train_idx]
    eval_rows_fold = [rows[int(i)] for i in eval_idx]
    y_train = labels_for(train_rows_fold)
    y_eval = labels_for(eval_rows_fold)
    classifier = make_classifier()
    classifier.fit(x_train, y_train)
    eval_pred = classifier.predict(x_eval)
    eval_prob = probabilities(classifier, x_eval)
    for local_pos, global_index in enumerate(eval_idx):
        oof_predictions[int(global_index)] = str(eval_pred[local_pos])
        oof_probabilities[int(global_index)] = eval_prob[local_pos]
    metrics = metric_bundle(y_eval, eval_pred)
    fold_metrics.append({"fold": fold_id, "metrics": metrics})
    fold_manifest["folds"].append({
        "fold": fold_id,
        "train_rows": int(len(train_idx)),
        "eval_rows": int(len(eval_idx)),
        "train_category_counts": dict(Counter(map(str, y_train))),
        "eval_category_counts": dict(Counter(map(str, y_eval))),
        "train_repository_count": len({row["repository"] for row in train_rows_fold}),
        "eval_repository_count": len({row["repository"] for row in eval_rows_fold}),
        "repository_overlap": sorted({row["repository"] for row in train_rows_fold} & {row["repository"] for row in eval_rows_fold}),
        "feature_meta": feature_meta,
    })

assert all(pred is not None for pred in oof_predictions)
assert all(not item["repository_overlap"] for item in fold_manifest["folds"])
write_json(OUTPUT_DIR / "fold_metrics.json", fold_metrics)
write_json(OUTPUT_DIR / "fold_manifest.json", fold_manifest)
"""
    metrics_diag = """
majority_label = Counter(y_all).most_common(1)[0][0]
majority_predictions = np.asarray([majority_label] * len(rows))
oof_predictions_array = np.asarray(oof_predictions)
oof_metrics = metric_bundle(y_all, oof_predictions_array)
majority_metrics = metric_bundle(y_all, majority_predictions)
write_json(OUTPUT_DIR / "oof_metrics.json", {"specialist": oof_metrics, "majority_baseline": majority_metrics})

with open(OUTPUT_DIR / "oof_predictions.jsonl", "w", encoding="utf-8", newline="\\n") as handle:
    for row, pred, prob in zip(rows, oof_predictions_array, oof_probabilities):
        handle.write(json.dumps({
            "case_id": row["case_id"],
            "repository": row["repository"],
            "language": row["language"],
            "gold": row["gold_doc_category"],
            "prediction": str(pred),
            "correct": row["gold_doc_category"] == str(pred),
            "probabilities": {label: float(prob[LABELS.index(label)]) for label in LABELS},
        }, ensure_ascii=False, sort_keys=True) + "\\n")

pairs = list(zip(y_all, oof_predictions_array))
probability_diagnostics = {
    "developer_setup_probability_by_gold": {
        label: {
            "count": int(sum(y_all == label)),
            "mean": float(np.mean(oof_probabilities[y_all == label, LABELS.index("developer_setup")])),
            "median": float(np.median(oof_probabilities[y_all == label, LABELS.index("developer_setup")])),
            "p10": float(np.percentile(oof_probabilities[y_all == label, LABELS.index("developer_setup")], 10)),
            "p90": float(np.percentile(oof_probabilities[y_all == label, LABELS.index("developer_setup")], 90)),
        }
        for label in LABELS
    }
}
write_json(OUTPUT_DIR / "probability_diagnostics.json", probability_diagnostics)

language_diagnostics = {}
for language in sorted({str(row.get("language") or "unknown").lower() for row in rows}):
    idx = np.asarray([str(row.get("language") or "unknown").lower() == language for row in rows])
    if idx.any():
        language_diagnostics[language] = metric_bundle(y_all[idx], oof_predictions_array[idx])
write_json(OUTPUT_DIR / "language_diagnostics.json", language_diagnostics)

repo_setup = {}
for repository in sorted({row["repository"] for row in rows}):
    idx = np.asarray([row["repository"] == repository for row in rows])
    if np.any((y_all == "developer_setup") & idx):
        repo_setup[repository] = {
            "rows": int(idx.sum()),
            "setup_rows": int(np.sum((y_all == "developer_setup") & idx)),
            "setup_correct": int(np.sum((y_all == "developer_setup") & idx & (oof_predictions_array == "developer_setup"))),
            "predicted_setup": int(np.sum(idx & (oof_predictions_array == "developer_setup"))),
        }
write_json(OUTPUT_DIR / "repository_setup_diagnostics.json", repo_setup)

repository_ids = np.asarray([row["repository"] for row in rows])
unique_repos = np.asarray(sorted(set(repository_ids)))
rng = np.random.default_rng(SEED)
bootstrap_macro_delta = []
bootstrap_balanced_delta = []
for _ in range(2000):
    sampled_repos = rng.choice(unique_repos, size=len(unique_repos), replace=True)
    sampled_indices = np.concatenate([np.where(repository_ids == repo)[0] for repo in sampled_repos])
    gold = y_all[sampled_indices]
    specialist = oof_predictions_array[sampled_indices]
    majority = majority_predictions[sampled_indices]
    bootstrap_macro_delta.append(f1_score(gold, specialist, labels=LABELS, average="macro", zero_division=0) - f1_score(gold, majority, labels=LABELS, average="macro", zero_division=0))
    bootstrap_balanced_delta.append(balanced_accuracy_score(gold, specialist) - balanced_accuracy_score(gold, majority))

def boot_summary(values):
    arr = np.asarray(values)
    return {"mean_delta": float(np.mean(arr)), "ci_2_5": float(np.percentile(arr, 2.5)), "ci_97_5": float(np.percentile(arr, 97.5)), "probability_delta_gt_zero": float(np.mean(arr > 0))}

repository_cluster_bootstrap = {
    "baseline": "majority_class",
    "iterations": 2000,
    "seed": SEED,
    "clusters": int(len(unique_repos)),
    "macro_f1_delta": boot_summary(bootstrap_macro_delta),
    "balanced_accuracy_delta": boot_summary(bootstrap_balanced_delta),
}
write_json(OUTPUT_DIR / "repository_cluster_bootstrap.json", repository_cluster_bootstrap)

setup_correct_repos = sorted({row["repository"] for row, pred in zip(rows, oof_predictions_array) if row["gold_doc_category"] == "developer_setup" and pred == "developer_setup"})
decision_gates = {
    "developer_setup_f1_ge_0_30": oof_metrics["per_class"]["developer_setup"]["f1"] >= 0.30,
    "balanced_accuracy_ge_0_60": oof_metrics["balanced_accuracy"] >= 0.60,
    "binary_macro_f1_ge_0_60": oof_metrics["macro_f1"] >= 0.60,
    "developer_setup_recall_ge_0_25": oof_metrics["per_class"]["developer_setup"]["recall"] >= 0.25,
    "setup_detections_across_multiple_repositories": len(setup_correct_repos) >= 2,
    "no_leakage_integrity_issue": True,
}
decision = {"decision": "GO" if all(decision_gates.values()) else "NO_GO", "gates": decision_gates, "setup_correct_repositories": setup_correct_repos}
write_json(OUTPUT_DIR / "decision.json", decision)
"""
    figures_reports = """
def plot_confusion(matrix, path, title, normalized=False):
    matrix = np.asarray(matrix)
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(matrix, cmap="Blues", vmin=0 if normalized else None, vmax=1 if normalized else None)
    ax.set_xticks(range(len(LABELS)), LABELS)
    ax.set_yticks(range(len(LABELS)), LABELS)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Gold")
    ax.set_title(title)
    for i in range(len(LABELS)):
        for j in range(len(LABELS)):
            ax.text(j, i, f"{matrix[i, j]:.2f}" if normalized else str(int(matrix[i, j])), ha="center", va="center")
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


plot_confusion(oof_metrics["confusion_matrix"], FIGURES_DIR / "oof_confusion_matrix.png", "OOF confusion matrix")
plot_confusion(oof_metrics["normalized_confusion_matrix"], FIGURES_DIR / "oof_normalized_confusion_matrix.png", "OOF normalized confusion matrix", normalized=True)

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot([item["fold"] for item in fold_metrics], [item["metrics"]["per_class"]["developer_setup"]["f1"] for item in fold_metrics], marker="o")
ax.set_ylim(0, 1)
ax.set_xlabel("Fold")
ax.set_ylabel("developer_setup F1")
fig.tight_layout()
fig.savefig(FIGURES_DIR / "fold_developer_setup_f1.png", dpi=180)
plt.close(fig)

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot([item["fold"] for item in fold_metrics], [item["metrics"]["macro_f1"] for item in fold_metrics], marker="o")
ax.set_ylim(0, 1)
ax.set_xlabel("Fold")
ax.set_ylabel("Macro-F1")
fig.tight_layout()
fig.savefig(FIGURES_DIR / "fold_macro_f1.png", dpi=180)
plt.close(fig)

fig, ax = plt.subplots(figsize=(7, 4))
for label in LABELS:
    ax.hist(oof_probabilities[y_all == label, LABELS.index("developer_setup")], alpha=0.6, bins=20, label=label)
ax.set_xlabel("OOF developer_setup probability")
ax.set_ylabel("Rows")
ax.legend()
fig.tight_layout()
fig.savefig(FIGURES_DIR / "setup_probability_distribution.png", dpi=180)
plt.close(fig)

fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(["majority", "specialist"], [majority_metrics["macro_f1"], oof_metrics["macro_f1"]])
ax.set_ylim(0, 1)
ax.set_ylabel("OOF Macro-F1")
fig.tight_layout()
fig.savefig(FIGURES_DIR / "majority_vs_specialist.png", dpi=180)
plt.close(fig)

errors = [
    {"case_id": row["case_id"], "repository": row["repository"], "language": row["language"], "gold": row["gold_doc_category"], "prediction": str(pred), "developer_setup_probability": float(prob[LABELS.index("developer_setup")])}
    for row, pred, prob in zip(rows, oof_predictions_array, oof_probabilities)
    if row["gold_doc_category"] != str(pred)
]
error_lines = ["# Bounded OOF error analysis", "", f"Total OOF errors: {len(errors)}", "", "## First 50 errors", ""]
for item in errors[:50]:
    error_lines.append(f"- `{item['case_id']}`: {item['gold']} -> {item['prediction']}; setup probability {item['developer_setup_probability']:.4f}")
(OUTPUT_DIR / "error_analysis.md").write_text("\\n".join(error_lines) + "\\n", encoding="utf-8")

binary_dataset_manifest = {
    "row_count": len(rows),
    "category_counts": dict(Counter(y_all)),
    "repository_count": len(unique_repos),
    "data_sha256": sha256_file(DATA_PATH),
    "source_manifest": manifest,
}
write_json(OUTPUT_DIR / "binary_dataset_manifest.json", binary_dataset_manifest)

experiment_manifest = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "model": "configuration_vs_developer_setup_specialist_v1",
    "encoder": {
        "model_name": MINILM_MODEL_NAME,
        "revision": MINILM_MODEL_REVISION,
        "resolved_revision": resolved_minilm_sha,
        "frozen": True,
        "eval_mode": True,
        "embedding_dimension": int(all_code_embeddings.shape[1]),
        "chunk_chars": CHUNK_CHARS,
        "max_chunks": MAX_CHUNKS,
        "normalize_embeddings": True,
        "gpu_used_for_embedding_extraction": True,
    },
    "dependencies": {
        "python": sys.version,
        "torch": torch.__version__,
        "cuda_device": torch.cuda.get_device_name(0),
        "sentence_transformers": sentence_transformers_version,
        "transformers": transformers.__version__,
        "tokenizers": tokenizers.__version__,
        "huggingface_hub": hf_hub_version,
        "scikit_learn": sklearn.__version__,
    },
    "classifier": {
        "class": "LogisticRegression",
        "C": 1.0,
        "solver": "lbfgs",
        "max_iter": 2000,
        "random_state": 42,
        "class_weight": None,
        "threshold": 0.5,
        "resampling": None,
    },
    "folds": fold_manifest,
    "confirmation_accessed": False,
    "frozen_322_validation_accessed": False,
    "validation_file_required": False,
}
write_json(OUTPUT_DIR / "experiment_manifest.json", experiment_manifest)

results_md = f'''# Configuration vs developer_setup specialist pilot V1

Decision: **{decision["decision"]}**

This is a train-only repository-grouped OOF pilot. It does not use the frozen 322-row development validation.

## OOF metrics

- Rows: **{len(rows)}**
- Folds: **{n_splits}**
- Macro-F1: **{oof_metrics["macro_f1"]:.4f}**
- Balanced accuracy: **{oof_metrics["balanced_accuracy"]:.4f}**
- configuration F1: **{oof_metrics["per_class"]["configuration"]["f1"]:.4f}**
- developer_setup F1: **{oof_metrics["per_class"]["developer_setup"]["f1"]:.4f}**
- developer_setup recall: **{oof_metrics["per_class"]["developer_setup"]["recall"]:.4f}**

## Majority baseline

- Majority label: `{majority_label}`
- Majority Macro-F1: **{majority_metrics["macro_f1"]:.4f}**
- Majority balanced accuracy: **{majority_metrics["balanced_accuracy"]:.4f}**

## GO / NO-GO gates

```json
{json.dumps(decision_gates, indent=2, sort_keys=True)}
```
'''
(OUTPUT_DIR / "RESULTS.md").write_text(results_md, encoding="utf-8")

zip_path = Path("/content/configuration_setup_specialist_v1_results.zip")
if zip_path.exists():
    zip_path.unlink()
lightweight_files = [
    "RESULTS.md",
    "experiment_manifest.json",
    "binary_dataset_manifest.json",
    "oof_metrics.json",
    "oof_predictions.jsonl",
    "fold_metrics.json",
    "fold_manifest.json",
    "repository_cluster_bootstrap.json",
    "language_diagnostics.json",
    "repository_setup_diagnostics.json",
    "probability_diagnostics.json",
    "error_analysis.md",
    "decision.json",
]
with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for name in lightweight_files:
        archive.write(OUTPUT_DIR / name, arcname=name)
    for figure in FIGURES_DIR.glob("*.png"):
        archive.write(figure, arcname=f"figures/{figure.name}")
print("Created lightweight result package:", zip_path)
"""
    download = """
from google.colab import files
files.download("/content/configuration_setup_specialist_v1_results.zip")
"""
    return {
        "cells": [
            nb_cell("markdown", title),
            nb_cell("code", deps),
            nb_cell("code", imports),
            nb_cell("code", constants),
            nb_cell("code", load_data),
            nb_cell("code", helpers),
            nb_cell("code", integrity),
            nb_cell("code", load_encoder),
            nb_cell("code", embeddings),
            nb_cell("code", oof),
            nb_cell("code", metrics_diag),
            nb_cell("code", figures_reports),
            nb_cell("code", download),
        ],
        "metadata": {
            "accelerator": "GPU",
            "colab": {"provenance": []},
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def write_notebook() -> None:
    NOTEBOOK_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTEBOOK_PATH.write_text(json.dumps(make_notebook(), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def compile_notebook_code_cells(path: Path) -> list[str]:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    for index, cell in enumerate(notebook.get("cells", []), 1):
        if cell.get("cell_type") != "code":
            continue
        source = "".join(cell.get("source", []))
        executable_lines = [
            line.strip()
            for line in source.splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        if executable_lines and executable_lines[0].startswith("!"):
            continue
        try:
            ast.parse(source)
        except SyntaxError as exc:
            errors.append(f"cell {index}: {exc}")
    return errors


def main() -> None:
    rows, manifest = load_and_build_export()
    write_jsonl(EXPORT_JSONL, rows)
    manifest["artifacts"]["natural_train_configuration_setup.jsonl"]["bytes"] = EXPORT_JSONL.stat().st_size
    manifest["artifacts"]["natural_train_configuration_setup.jsonl"]["sha256"] = sha256_file(EXPORT_JSONL)
    manifest["case_ids_sha256"] = stable_json_hash([row["case_id"] for row in rows])
    write_json(EXPORT_MANIFEST, manifest)
    write_notebook()
    compile_errors = compile_notebook_code_cells(NOTEBOOK_PATH)
    if compile_errors:
        raise SyntaxError("; ".join(compile_errors))
    print(
        json.dumps(
            {
                "status": "prepared",
                "export": str(EXPORT_JSONL.relative_to(ROOT)),
                "manifest": str(EXPORT_MANIFEST.relative_to(ROOT)),
                "notebook": str(NOTEBOOK_PATH.relative_to(ROOT)),
                "row_count": len(rows),
                "category_counts": manifest["category_counts"],
                "export_sha256": manifest["artifacts"]["natural_train_configuration_setup.jsonl"]["sha256"],
                "created_at": datetime.now(UTC).isoformat(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
