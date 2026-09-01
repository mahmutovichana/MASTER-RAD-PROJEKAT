"""Prepare the final Stage-2 coarse-to-fine hierarchy V1 Colab notebook.

The local script only verifies the frozen 1038-row natural primary-four train
export and writes a self-contained Colab notebook plus README. It does not run
the final repository-grouped OOF experiment locally.
"""
from __future__ import annotations

import ast
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRAIN_DIR = ROOT / "data" / "final_v2" / "architecture_challenge_v1"
TRAIN_JSONL = TRAIN_DIR / "natural_train_primary_four.jsonl"
TRAIN_MANIFEST = TRAIN_DIR / "export_manifest.json"
NOTEBOOK_PATH = ROOT / "notebooks" / "category_stage2_coarse_to_fine_hierarchy_v1.ipynb"
README_PATH = ROOT / "experiments" / "category_stage2_coarse_to_fine_hierarchy_v1" / "README.md"

LABELS = ["api_reference", "configuration", "developer_setup", "model_contract"]
COARSE_LABELS = ["api_reference", "config_setup_family", "model_contract"]
SPECIALIST_LABELS = ["configuration", "developer_setup"]
COARSE_MAPPING = {
    "api_reference": "api_reference",
    "configuration": "config_setup_family",
    "developer_setup": "config_setup_family",
    "model_contract": "model_contract",
}
EXPECTED_TOTAL = 1038
EXPECTED_COUNTS = {
    "api_reference": 412,
    "configuration": 277,
    "developer_setup": 88,
    "model_contract": 261,
}
EXPECTED_COARSE_COUNTS = {
    "api_reference": 412,
    "config_setup_family": 365,
    "model_contract": 261,
}
EXPECTED_TRAIN_SHA256 = "9dc1136f1cf695eb69c70b763ad051898aa5fae351fcf028eed97116c8891f99"
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

MINILM_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
MINILM_MODEL_REVISION = "1110a243fdf4706b3f48f1d95db1a4f5529b4d41"
CLASS_WEIGHT_GRID = [
    {"name": "none", "value": None, "rank": 0},
    {"name": "developer_1_5", "value": {"configuration": 1.0, "developer_setup": 1.5}, "rank": 1},
    {"name": "developer_2_0", "value": {"configuration": 1.0, "developer_setup": 2.0}, "rank": 2},
    {"name": "developer_3_0", "value": {"configuration": 1.0, "developer_setup": 3.0}, "rank": 3},
    {"name": "balanced", "value": "balanced", "rank": 4},
]
THRESHOLD_GRID = [0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]
PRECISION_FLOOR = 0.30


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def verify_train_export() -> None:
    rows = read_jsonl(TRAIN_JSONL)
    manifest = json.loads(TRAIN_MANIFEST.read_text(encoding="utf-8"))
    counts = Counter(row["gold_doc_category"] for row in rows)
    coarse_counts = Counter(COARSE_MAPPING[row["gold_doc_category"]] for row in rows)
    if len(rows) != EXPECTED_TOTAL:
        raise AssertionError(f"Expected {EXPECTED_TOTAL} rows, got {len(rows)}")
    if dict(counts) != EXPECTED_COUNTS:
        raise AssertionError(f"Expected {EXPECTED_COUNTS}, got {dict(counts)}")
    if dict(coarse_counts) != EXPECTED_COARSE_COUNTS:
        raise AssertionError(f"Expected {EXPECTED_COARSE_COUNTS}, got {dict(coarse_counts)}")
    if sha256_file(TRAIN_JSONL) != EXPECTED_TRAIN_SHA256:
        raise AssertionError("Frozen primary-four train file hash changed")
    if any(row.get("partition") != "development_train" for row in rows):
        raise AssertionError("Only development_train rows are eligible")
    if any(row.get("gold_doc_category") not in LABELS for row in rows):
        raise AssertionError("Only the four canonical Stage-2 labels are eligible")
    if manifest["artifacts"]["natural_train_primary_four.jsonl"]["sha256"] != EXPECTED_TRAIN_SHA256:
        raise AssertionError("Manifest train artifact hash mismatch")
    if manifest.get("confirmation_accessed") is not False:
        raise AssertionError("Confirmation data must not be accessed")
    if manifest.get("controlled_or_synthetic_rows_used") is not False:
        raise AssertionError("Controlled/synthetic rows must not be used")


def nb_cell(cell_type: str, source: str) -> dict[str, Any]:
    return {
        "cell_type": cell_type,
        "metadata": {},
        "source": [line + "\n" for line in source.strip("\n").splitlines()],
        **({"outputs": [], "execution_count": None} if cell_type == "code" else {}),
    }


def py(value: Any) -> str:
    return repr(value)


def make_notebook() -> dict[str, Any]:
    title = """
# Stage-2 coarse-to-fine hierarchy V1

Final train-side Stage-2 architecture experiment. The hierarchy first predicts
`api_reference` vs `config_setup_family` vs `model_contract`, then applies the
nested cost-sensitive Specialist V2 only when Level 1 predicts
`config_setup_family`.

This notebook runs repository-grouped OOF on the frozen 1038-row natural
primary-four train universe only. It must not load the frozen 322-row
development validation.
"""
    deps = """
# Python 3.13 compatible Colab stack. Keep Colab's CUDA-enabled torch build.
!python -m pip install -q \\
  "sentence-transformers==5.1.2" \\
  "transformers==4.56.2" \\
  "tokenizers==0.22.0" \\
  "huggingface_hub==0.34.4" \\
  "accelerate==1.10.1" \\
  "scikit-learn==1.7.2" \\
  "matplotlib==3.10.6" \\
  "scipy"
"""
    imports = """
from __future__ import annotations

import hashlib
import json
import math
import random
import re
import sys
import time
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import accelerate
import huggingface_hub
import matplotlib.pyplot as plt
import numpy as np
import sklearn
import tokenizers
import torch
import transformers
from huggingface_hub import HfApi
from scipy import sparse
from sentence_transformers import SentenceTransformer
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
print("CUDA availability:", torch.cuda.is_available())
print("CUDA device:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "NONE")
print("transformers:", transformers.__version__)
print("tokenizers:", tokenizers.__version__)
print("accelerate:", accelerate.__version__)
print("huggingface_hub:", huggingface_hub.__version__)
assert torch.cuda.is_available()
"""
    constants = f"""
LABELS = {py(LABELS)}
COARSE_LABELS = {py(COARSE_LABELS)}
SPECIALIST_LABELS = {py(SPECIALIST_LABELS)}
COARSE_MAPPING = {py(COARSE_MAPPING)}
SAFE_FIELDS = {py(SAFE_FIELDS)}
EXPECTED_TOTAL = {EXPECTED_TOTAL}
EXPECTED_COUNTS = {py(EXPECTED_COUNTS)}
EXPECTED_COARSE_COUNTS = {py(EXPECTED_COARSE_COUNTS)}
EXPECTED_TRAIN_SHA256 = "{EXPECTED_TRAIN_SHA256}"
SEED = 42

MINILM_MODEL_NAME = "{MINILM_MODEL_NAME}"
MINILM_MODEL_REVISION = "{MINILM_MODEL_REVISION}"
CHUNK_CHARS = 1000
MAX_CHUNKS = 2
EMBEDDING_BATCH_SIZE = 64

CLASS_WEIGHT_GRID = {py(CLASS_WEIGHT_GRID)}
THRESHOLD_GRID = {py(THRESHOLD_GRID)}
PRECISION_FLOOR = {PRECISION_FLOOR}

OUTPUT_DIR = Path("/content/experiments/category_stage2_coarse_to_fine_hierarchy_v1")
CACHE_DIR = OUTPUT_DIR / "cache"
FIGURES_DIR = OUTPUT_DIR / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
"""
    data_helpers = r'''
def reject_supplied_path(path):
    lowered = str(path).replace("\\", "/").lower()
    if any(word in lowered for word in ["validation", "confirmation", "refresh"]):
        raise ValueError(f"Forbidden non-train artifact path: {path}")


def has_train_export(root):
    train_dir = Path(root) / "data" / "final_v2" / "architecture_challenge_v1"
    return (train_dir / "natural_train_primary_four.jsonl").exists() and (train_dir / "export_manifest.json").exists()


def locate_train_root():
    candidates = [
        Path.cwd(),
        Path("/content/MASTER-RAD-PROJEKAT"),
        Path("/content/MASTER RAD PROJEKAT"),
        Path("/content/drive/MyDrive/MASTER-RAD-PROJEKAT"),
        Path("/content/drive/MyDrive/MASTER RAD PROJEKAT"),
    ]
    for candidate in candidates:
        if has_train_export(candidate):
            return candidate
    for manifest in Path("/content").glob("**/export_manifest.json"):
        reject_supplied_path(manifest)
        if "architecture_challenge_v1" not in manifest.as_posix():
            continue
        possible = manifest.parent.parent.parent.parent
        if has_train_export(possible):
            return possible
    return None


ROOT = locate_train_root()
if ROOT is None:
    print("Upload repository ZIP or only these train files: natural_train_primary_four.jsonl and export_manifest.json")
    from google.colab import files

    uploaded = files.upload()
    upload_root = Path("/content/MASTER-RAD-PROJEKAT")
    train_dir = upload_root / "data" / "final_v2" / "architecture_challenge_v1"
    train_dir.mkdir(parents=True, exist_ok=True)
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
        elif base in {"natural_train_primary_four.jsonl", "export_manifest.json"}:
            (train_dir / base).write_bytes(payload)
    ROOT = locate_train_root()

assert ROOT is not None and has_train_export(ROOT)
TRAIN_DIR = ROOT / "data" / "final_v2" / "architecture_challenge_v1"
DATA_PATH = TRAIN_DIR / "natural_train_primary_four.jsonl"
MANIFEST_PATH = TRAIN_DIR / "export_manifest.json"
print("Using frozen natural primary-four train export:", TRAIN_DIR)
'''
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
    reject_supplied_path(path)
    rows = []
    with open(path, encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("partition") != "development_train":
                raise ValueError(f"{path}:{line_number}: only development_train rows are allowed")
            rows.append({field: row.get(field) for field in SAFE_FIELDS})
    return rows


def coarse_label(label):
    return COARSE_MAPPING[str(label)]


def list_value(value):
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.startswith("["):
            try:
                parsed = json.loads(stripped)
                if isinstance(parsed, list):
                    return [str(item) for item in parsed]
            except json.JSONDecodeError:
                pass
        return [stripped] if stripped else []
    return []


def sanitize_repository_identity(text, repository):
    repo = str(repository or "").strip().strip("/")
    sanitized = str(text or "")
    if not repo or "/" not in repo:
        return sanitized
    owner, name = repo.split("/", 1)
    patterns = [
        re.escape(repo),
        re.escape(f"github.com/{repo}"),
        re.escape(f"https://github.com/{repo}"),
        re.escape(f"http://github.com/{repo}"),
        re.escape(f"git@github.com:{repo}"),
        rf"github\.com/{re.escape(owner)}/{re.escape(name)}(?:\.git)?",
    ]
    for pattern in patterns:
        sanitized = re.sub(pattern, "[REPOSITORY]", sanitized, flags=re.IGNORECASE)
    return sanitized


def build_code_text(row):
    text = "\n".join([
        f"language: {str(row.get('language') or 'unknown').lower()}",
        "changed files:",
        "\n".join(list_value(row.get("code_changed_files"))),
        "code change:",
        str(row.get("code_diff_excerpt") or ""),
    ])
    return sanitize_repository_identity(text, row.get("repository"))


def build_docs_text(row):
    return sanitize_repository_identity(row.get("docs_before_excerpt") or "", row.get("repository"))


def deterministic_chunks(text, chunk_chars=CHUNK_CHARS, max_chunks=MAX_CHUNKS):
    normalized = re.sub(r"\x00", " ", str(text or "")).strip()
    if not normalized:
        return ["[empty]"]
    if len(normalized) <= chunk_chars:
        return [normalized]
    starts = np.linspace(0, max(0, len(normalized) - chunk_chars), num=max_chunks, dtype=int)
    return [normalized[int(start): int(start) + chunk_chars] for start in starts]


def encode_texts_cached(side, texts, encoder):
    key = stable_json_hash({
        "side": side,
        "model": MINILM_MODEL_NAME,
        "revision": MINILM_MODEL_REVISION,
        "chunk_chars": CHUNK_CHARS,
        "max_chunks": MAX_CHUNKS,
        "content_hash": stable_json_hash(texts),
    })
    target = CACHE_DIR / f"{side}_{key}.npy"
    meta_path = CACHE_DIR / f"{side}_{key}.json"
    if target.exists() and meta_path.exists():
        return np.load(target), json.loads(meta_path.read_text(encoding="utf-8")) | {"cache_hit": True}
    chunks, owners = [], []
    for row_index, text in enumerate(texts):
        for chunk in deterministic_chunks(text):
            chunks.append(chunk)
            owners.append(row_index)
    current_batch = EMBEDDING_BATCH_SIZE
    started = time.time()
    while True:
        try:
            with torch.inference_mode():
                chunk_vectors = encoder.encode(chunks, batch_size=current_batch, show_progress_bar=True, convert_to_numpy=True, normalize_embeddings=True, device="cuda").astype(np.float32)
            break
        except torch.cuda.OutOfMemoryError:
            torch.cuda.empty_cache()
            if current_batch <= 1:
                raise
            current_batch = max(1, current_batch // 2)
            print("OOM; retrying MiniLM encode with batch_size=", current_batch)
    output = np.zeros((len(texts), chunk_vectors.shape[1]), dtype=np.float32)
    counts = np.zeros(len(texts), dtype=np.float32)
    for owner, vector in zip(owners, chunk_vectors):
        output[owner] += vector
        counts[owner] += 1.0
    output /= np.maximum(counts[:, None], 1.0)
    output /= np.maximum(np.linalg.norm(output, axis=1, keepdims=True), 1e-12)
    np.save(target, output)
    meta = {"side": side, "row_count": len(texts), "chunk_count": len(chunks), "embedding_dimension": int(output.shape[1]), "batch_size_used": int(current_batch), "elapsed_seconds": time.time() - started, "cache_hit": False}
    meta_path.write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output, meta


TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{1,}")


def token_set(text):
    return {token.lower() for token in TOKEN_RE.findall(text)}


def lexical_relational_scalars(selected_rows):
    values = []
    for row in selected_rows:
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
    cosine = np.sum(code * docs, axis=1, keepdims=True)
    return np.hstack([code, docs, np.abs(code - docs), code * docs, cosine]).astype(np.float32)


def labels_for(selected_rows):
    return np.asarray([row["gold_doc_category"] for row in selected_rows])


def coarse_labels_for(selected_rows):
    return np.asarray([coarse_label(row["gold_doc_category"]) for row in selected_rows])


def metric_bundle(y_true, y_pred, labels):
    precision, recall, f1, support = precision_recall_fscore_support(y_true, y_pred, labels=labels, zero_division=0)
    matrix = confusion_matrix(y_true, y_pred, labels=labels)
    normalized = matrix.astype(float) / np.maximum(matrix.sum(axis=1, keepdims=True), 1)
    return {
        "support": int(len(y_true)),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, labels=labels, average="macro", zero_division=0)),
        "weighted_f1": float(f1_score(y_true, y_pred, labels=labels, average="weighted", zero_division=0)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
        "per_class": {label: {"precision": float(precision[i]), "recall": float(recall[i]), "f1": float(f1[i]), "support": int(support[i])} for i, label in enumerate(labels)},
        "confusion_matrix": matrix.tolist(),
        "normalized_confusion_matrix": normalized.tolist(),
        "predicted_class_counts": dict(sorted(Counter(map(str, y_pred)).items())),
    }


def setup_probability(classifier, features):
    raw = classifier.predict_proba(features)
    if "developer_setup" not in classifier.classes_:
        return np.zeros(features.shape[0], dtype=float)
    return raw[:, list(classifier.classes_).index("developer_setup")]


def classifier_probabilities(classifier, features, labels):
    raw = classifier.predict_proba(features)
    output = np.zeros((features.shape[0], len(labels)), dtype=float)
    for source_index, label in enumerate(classifier.classes_):
        output[:, labels.index(str(label))] = raw[:, source_index]
    return output


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
'''
    integrity = """
manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
rows = read_jsonl(DATA_PATH)
assert len(rows) == EXPECTED_TOTAL
assert Counter(row["gold_doc_category"] for row in rows) == EXPECTED_COUNTS
assert Counter(coarse_label(row["gold_doc_category"]) for row in rows) == EXPECTED_COARSE_COUNTS
assert sha256_file(DATA_PATH) == EXPECTED_TRAIN_SHA256
assert manifest["artifacts"]["natural_train_primary_four.jsonl"]["sha256"] == EXPECTED_TRAIN_SHA256
assert set(row["partition"] for row in rows) == {"development_train"}
assert all(set(row) == set(SAFE_FIELDS) for row in rows)
for row in rows:
    assert row["gold_doc_category"] in LABELS
    combined = (build_code_text(row) + "\\n" + build_docs_text(row)).lower()
    repo = str(row.get("repository") or "").lower()
    assert not repo or "/" not in repo or repo not in combined
print("Verified train data:", Counter(row["gold_doc_category"] for row in rows))
print("Verified coarse data:", Counter(coarse_label(row["gold_doc_category"]) for row in rows))
"""
    encoder = """
resolved_minilm_sha = HfApi().model_info(MINILM_MODEL_NAME, revision=MINILM_MODEL_REVISION).sha
print("Resolved MiniLM revision:", resolved_minilm_sha)
assert resolved_minilm_sha == MINILM_MODEL_REVISION
encoder = SentenceTransformer(MINILM_MODEL_NAME, revision=MINILM_MODEL_REVISION, device="cuda")
encoder.eval()
for parameter in encoder.parameters():
    parameter.requires_grad_(False)
assert all(not parameter.requires_grad for parameter in encoder.parameters())
with torch.inference_mode():
    smoke = encoder.encode([build_code_text(rows[0]), build_docs_text(rows[0])], batch_size=2, convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=False, device="cuda")
assert smoke.shape[0] == 2 and smoke.shape[1] > 0
assert np.all(np.isfinite(smoke))
"""
    features_splits = r'''
code_texts = [build_code_text(row) for row in rows]
docs_texts = [build_docs_text(row) for row in rows]
all_code_embeddings, code_cache = encode_texts_cached("code", code_texts, encoder)
all_docs_embeddings, docs_cache = encode_texts_cached("docs", docs_texts, encoder)
assert all_code_embeddings.shape == all_docs_embeddings.shape


def build_fold_features(train_idx, eval_idx, *, feature_context):
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
    x_train = sparse.hstack([
        code_train,
        sparse.csr_matrix(relational_semantic_features(all_code_embeddings[train_idx], all_docs_embeddings[train_idx])),
        sparse.csr_matrix(lexical_relational_scalars(train_rows)),
    ], format="csr")
    x_eval = sparse.hstack([
        code_eval,
        sparse.csr_matrix(relational_semantic_features(all_code_embeddings[eval_idx], all_docs_embeddings[eval_idx])),
        sparse.csr_matrix(lexical_relational_scalars(eval_rows)),
    ], format="csr")
    return x_train, x_eval, {"feature_context": feature_context, "tfidf_fit_rows": int(len(train_idx)), "tfidf_eval_rows": int(len(eval_idx)), "eval_enters_tfidf_fit": False}


def grouped_splits(indices, *, label_fn, required_labels, n_splits, seed):
    idx = np.asarray(indices, dtype=int)
    selected_rows = [rows[int(i)] for i in idx]
    y = label_fn(selected_rows)
    groups = np.asarray([row["repository"] for row in selected_rows])
    splitter = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    out = []
    for train_local, eval_local in splitter.split(np.arange(len(idx)), y, groups):
        train_idx = idx[train_local]
        eval_idx = idx[eval_local]
        train_rows = [rows[int(i)] for i in train_idx]
        eval_rows = [rows[int(i)] for i in eval_idx]
        y_train = label_fn(train_rows)
        y_eval = label_fn(eval_rows)
        g_train = {row["repository"] for row in train_rows}
        g_eval = {row["repository"] for row in eval_rows}
        if g_train & g_eval:
            raise AssertionError("Repository overlap inside grouped split")
        if set(y_train) != set(required_labels) or set(y_eval) != set(required_labels):
            raise ValueError("Fold missing a required class")
        out.append((train_idx, eval_idx))
    return out


def outer_split_valid(train_rows, eval_rows):
    return (
        set(labels_for(train_rows)) == set(LABELS)
        and set(labels_for(eval_rows)) == set(LABELS)
        and set(coarse_labels_for(train_rows)) == set(COARSE_LABELS)
        and set(coarse_labels_for(eval_rows)) == set(COARSE_LABELS)
    )


def choose_outer_splits():
    for n_splits in [5, 4, 3]:
        try:
            folds = grouped_splits(np.arange(len(rows)), label_fn=labels_for, required_labels=LABELS, n_splits=n_splits, seed=SEED)
        except ValueError:
            continue
        if all(outer_split_valid([rows[int(i)] for i in train_idx], [rows[int(i)] for i in eval_idx]) for train_idx, eval_idx in folds):
            return n_splits, folds
    raise RuntimeError("No structurally valid outer split.")


def choose_inner_splits(specialist_outer_train_idx, outer_fold_id):
    for n_splits in [4, 3]:
        try:
            return n_splits, grouped_splits(specialist_outer_train_idx, label_fn=labels_for, required_labels=SPECIALIST_LABELS, n_splits=n_splits, seed=SEED + outer_fold_id)
        except ValueError:
            continue
    raise RuntimeError("No structurally valid specialist inner split.")


outer_n_splits, outer_folds = choose_outer_splits()
outer_manifest = {"splitter": "StratifiedGroupKFold", "seed": SEED, "n_splits": outer_n_splits, "folds": []}
for fold_id, (train_idx, eval_idx) in enumerate(outer_folds, 1):
    train_rows = [rows[int(i)] for i in train_idx]
    eval_rows = [rows[int(i)] for i in eval_idx]
    train_repos = {row["repository"] for row in train_rows}
    eval_repos = {row["repository"] for row in eval_rows}
    assert not train_repos & eval_repos
    assert outer_split_valid(train_rows, eval_rows)
    outer_manifest["folds"].append({
        "fold": fold_id,
        "train_rows": int(len(train_idx)),
        "eval_rows": int(len(eval_idx)),
        "train_category_counts": dict(Counter(labels_for(train_rows))),
        "eval_category_counts": dict(Counter(labels_for(eval_rows))),
        "train_coarse_counts": dict(Counter(coarse_labels_for(train_rows))),
        "eval_coarse_counts": dict(Counter(coarse_labels_for(eval_rows))),
        "train_repositories": sorted(train_repos),
        "eval_repositories": sorted(eval_repos),
        "repository_overlap": [],
    })
write_json(OUTPUT_DIR / "outer_fold_manifest.json", outer_manifest)
'''
    experiment = r'''
def predict_from_threshold(prob_setup, threshold):
    return np.where(prob_setup >= threshold, "developer_setup", "configuration")


def candidate_sort_key(item):
    metrics = item["metrics"]
    setup = metrics["per_class"]["developer_setup"]
    return (
        metrics["macro_f1"],
        setup["f1"],
        metrics["balanced_accuracy"],
        setup["precision"],
        -abs(item["threshold"] - 0.5),
        -item["class_weight_rank"],
    )


def select_specialist_params(outer_fold_id, specialist_outer_train_idx):
    inner_n_splits, inner_folds = choose_inner_splits(specialist_outer_train_idx, outer_fold_id)
    position = {int(global_index): pos for pos, global_index in enumerate(specialist_outer_train_idx)}
    candidate_probs = defaultdict(lambda: np.zeros(len(specialist_outer_train_idx), dtype=float))
    fit_audit = []
    for inner_fold_id, (inner_train_idx, inner_eval_idx) in enumerate(inner_folds, 1):
        x_inner_train, x_inner_eval, feature_meta = build_fold_features(inner_train_idx, inner_eval_idx, feature_context="specialist_inner_train_only")
        y_inner_train = labels_for([rows[int(i)] for i in inner_train_idx])
        assert set(y_inner_train) == set(SPECIALIST_LABELS)
        for weight_spec in CLASS_WEIGHT_GRID:
            clf = LogisticRegression(C=1.0, solver="lbfgs", max_iter=2000, random_state=SEED, class_weight=weight_spec["value"])
            clf.fit(x_inner_train, y_inner_train)
            prob_setup = setup_probability(clf, x_inner_eval)
            for global_index, prob in zip(inner_eval_idx, prob_setup):
                candidate_probs[weight_spec["name"]][position[int(global_index)]] = float(prob)
            fit_audit.append({"inner_fold": inner_fold_id, "class_weight": weight_spec["name"], "feature_meta": feature_meta})
    y_specialist_train = labels_for([rows[int(i)] for i in specialist_outer_train_idx])
    scored = []
    for weight_spec in CLASS_WEIGHT_GRID:
        for threshold in THRESHOLD_GRID:
            pred = predict_from_threshold(candidate_probs[weight_spec["name"]], threshold)
            metrics = metric_bundle(y_specialist_train, pred, SPECIALIST_LABELS)
            scored.append({
                "class_weight": weight_spec["name"],
                "class_weight_value": weight_spec["value"],
                "class_weight_rank": int(weight_spec["rank"]),
                "threshold": float(threshold),
                "precision_floor_satisfied": bool(metrics["per_class"]["developer_setup"]["precision"] >= PRECISION_FLOOR),
                "metrics": metrics,
            })
    eligible = [item for item in scored if item["precision_floor_satisfied"]]
    selected = max(eligible if eligible else scored, key=candidate_sort_key)
    return selected, scored, {"inner_n_splits": inner_n_splits, "fit_audit": fit_audit}


y_all = labels_for(rows)
coarse_all = coarse_labels_for(rows)
baseline_predictions = np.asarray([""] * len(rows), dtype=object)
coarse_predictions = np.asarray([""] * len(rows), dtype=object)
hierarchy_predictions = np.asarray([""] * len(rows), dtype=object)
specialist_predictions_if_applicable = np.asarray([""] * len(rows), dtype=object)
specialist_scores = np.full(len(rows), np.nan, dtype=float)
baseline_probabilities = np.zeros((len(rows), len(LABELS)), dtype=float)
coarse_probabilities = np.zeros((len(rows), len(COARSE_LABELS)), dtype=float)
outer_fold_metrics = []
specialist_selection_by_fold = []

for outer_fold_id, (outer_train_idx, outer_eval_idx) in enumerate(outer_folds, 1):
    train_rows = [rows[int(i)] for i in outer_train_idx]
    eval_rows = [rows[int(i)] for i in outer_eval_idx]

    x_base_train, x_base_eval, base_feature_meta = build_fold_features(outer_train_idx, outer_eval_idx, feature_context="baseline_four_class_outer_train_only")
    y_base_train = labels_for(train_rows)
    y_eval = labels_for(eval_rows)
    baseline_clf = LogisticRegression(C=1.0, solver="lbfgs", max_iter=2000, random_state=SEED)
    baseline_clf.fit(x_base_train, y_base_train)
    base_pred = baseline_clf.predict(x_base_eval)
    base_prob = classifier_probabilities(baseline_clf, x_base_eval, LABELS)

    x_coarse_train, x_coarse_eval, coarse_feature_meta = build_fold_features(outer_train_idx, outer_eval_idx, feature_context="coarse_three_class_outer_train_only")
    y_coarse_train = coarse_labels_for(train_rows)
    y_coarse_eval = coarse_labels_for(eval_rows)
    coarse_clf = LogisticRegression(C=1.0, solver="lbfgs", max_iter=2000, random_state=SEED)
    coarse_clf.fit(x_coarse_train, y_coarse_train)
    coarse_pred = coarse_clf.predict(x_coarse_eval)
    coarse_prob = classifier_probabilities(coarse_clf, x_coarse_eval, COARSE_LABELS)

    specialist_outer_train_idx = np.asarray([int(i) for i in outer_train_idx if rows[int(i)]["gold_doc_category"] in SPECIALIST_LABELS], dtype=int)
    selected, grid, inner_meta = select_specialist_params(outer_fold_id, specialist_outer_train_idx)
    x_spec_train, x_spec_eval, spec_feature_meta = build_fold_features(specialist_outer_train_idx, outer_eval_idx, feature_context="specialist_final_outer_train_config_setup_only")
    y_spec_train = labels_for([rows[int(i)] for i in specialist_outer_train_idx])
    specialist_clf = LogisticRegression(C=1.0, solver="lbfgs", max_iter=2000, random_state=SEED, class_weight=selected["class_weight_value"])
    specialist_clf.fit(x_spec_train, y_spec_train)
    spec_prob_setup = setup_probability(specialist_clf, x_spec_eval)
    spec_pred = predict_from_threshold(spec_prob_setup, selected["threshold"])

    final_pred = []
    for local_pos, global_index in enumerate(outer_eval_idx):
        global_index = int(global_index)
        baseline_predictions[global_index] = str(base_pred[local_pos])
        baseline_probabilities[global_index] = base_prob[local_pos]
        coarse_predictions[global_index] = str(coarse_pred[local_pos])
        coarse_probabilities[global_index] = coarse_prob[local_pos]
        if str(coarse_pred[local_pos]) == "config_setup_family":
            final = str(spec_pred[local_pos])
            specialist_predictions_if_applicable[global_index] = final
            specialist_scores[global_index] = float(spec_prob_setup[local_pos])
        elif str(coarse_pred[local_pos]) == "api_reference":
            final = "api_reference"
        elif str(coarse_pred[local_pos]) == "model_contract":
            final = "model_contract"
        else:
            raise AssertionError("Unexpected coarse prediction")
        hierarchy_predictions[global_index] = final
        final_pred.append(final)

    fold_baseline_metrics = metric_bundle(y_eval, base_pred, LABELS)
    fold_coarse_metrics = metric_bundle(y_coarse_eval, coarse_pred, COARSE_LABELS)
    fold_hierarchy_metrics = metric_bundle(y_eval, np.asarray(final_pred), LABELS)
    setup_mask_eval = y_eval == "developer_setup"
    setup_family_routing_recall = float(np.mean(coarse_pred[setup_mask_eval] == "config_setup_family")) if setup_mask_eval.any() else 0.0
    outer_fold_metrics.append({
        "fold": outer_fold_id,
        "baseline": fold_baseline_metrics,
        "coarse": fold_coarse_metrics,
        "hierarchy": fold_hierarchy_metrics,
        "setup_family_routing_recall": setup_family_routing_recall,
        "deltas": {
            "macro_f1": fold_hierarchy_metrics["macro_f1"] - fold_baseline_metrics["macro_f1"],
            "balanced_accuracy": fold_hierarchy_metrics["balanced_accuracy"] - fold_baseline_metrics["balanced_accuracy"],
            "developer_setup_f1": fold_hierarchy_metrics["per_class"]["developer_setup"]["f1"] - fold_baseline_metrics["per_class"]["developer_setup"]["f1"],
            "developer_setup_recall": fold_hierarchy_metrics["per_class"]["developer_setup"]["recall"] - fold_baseline_metrics["per_class"]["developer_setup"]["recall"],
        },
    })
    specialist_selection_by_fold.append({
        "outer_fold": outer_fold_id,
        "selected_class_weight": selected["class_weight"],
        "selected_threshold": float(selected["threshold"]),
        "precision_floor_satisfied": bool(selected["precision_floor_satisfied"]),
        "grid": grid,
        "inner_meta": inner_meta,
        "baseline_feature_meta": base_feature_meta,
        "coarse_feature_meta": coarse_feature_meta,
        "specialist_feature_meta": spec_feature_meta,
        "specialist_train_rows": int(len(specialist_outer_train_idx)),
    })

assert all(item in LABELS for item in baseline_predictions)
assert all(item in COARSE_LABELS for item in coarse_predictions)
assert all(item in LABELS for item in hierarchy_predictions)
assert len(baseline_predictions) == len(hierarchy_predictions) == len(rows)
write_json(OUTPUT_DIR / "outer_fold_metrics.json", outer_fold_metrics)
write_json(OUTPUT_DIR / "specialist_selection_by_fold.json", specialist_selection_by_fold)
'''
    diagnostics = r'''
baseline_metrics = metric_bundle(y_all, baseline_predictions, LABELS)
coarse_metrics = metric_bundle(coarse_all, coarse_predictions, COARSE_LABELS)
hierarchy_metrics = metric_bundle(y_all, hierarchy_predictions, LABELS)

comparison = {
    "baseline": baseline_metrics,
    "hierarchy": hierarchy_metrics,
    "delta": {
        "accuracy": hierarchy_metrics["accuracy"] - baseline_metrics["accuracy"],
        "macro_f1": hierarchy_metrics["macro_f1"] - baseline_metrics["macro_f1"],
        "balanced_accuracy": hierarchy_metrics["balanced_accuracy"] - baseline_metrics["balanced_accuracy"],
        "api_reference_f1": hierarchy_metrics["per_class"]["api_reference"]["f1"] - baseline_metrics["per_class"]["api_reference"]["f1"],
        "configuration_f1": hierarchy_metrics["per_class"]["configuration"]["f1"] - baseline_metrics["per_class"]["configuration"]["f1"],
        "developer_setup_f1": hierarchy_metrics["per_class"]["developer_setup"]["f1"] - baseline_metrics["per_class"]["developer_setup"]["f1"],
        "model_contract_f1": hierarchy_metrics["per_class"]["model_contract"]["f1"] - baseline_metrics["per_class"]["model_contract"]["f1"],
        "developer_setup_precision": hierarchy_metrics["per_class"]["developer_setup"]["precision"] - baseline_metrics["per_class"]["developer_setup"]["precision"],
        "developer_setup_recall": hierarchy_metrics["per_class"]["developer_setup"]["recall"] - baseline_metrics["per_class"]["developer_setup"]["recall"],
    },
}

setup_mask = y_all == "developer_setup"
configuration_mask = y_all == "configuration"
setup_family_routing_recall = float(np.mean(coarse_predictions[setup_mask] == "config_setup_family"))
configuration_family_routing_recall = float(np.mean(coarse_predictions[configuration_mask] == "config_setup_family"))
coarse_diagnostics = {
    "metrics": coarse_metrics,
    "true_developer_setup_level1_distribution": dict(Counter(coarse_predictions[setup_mask])),
    "true_configuration_level1_distribution": dict(Counter(coarse_predictions[configuration_mask])),
    "setup_family_routing_recall": setup_family_routing_recall,
    "configuration_family_routing_recall": configuration_family_routing_recall,
}

developer_setup_path_analysis = defaultdict(list)
configuration_path_analysis = defaultdict(list)
api_model_damage_analysis = {"api_reference": defaultdict(list), "model_contract": defaultdict(list)}
for row, coarse_pred, specialist_pred, final_pred in zip(rows, coarse_predictions, specialist_predictions_if_applicable, hierarchy_predictions):
    item = {"case_id": row["case_id"], "repository": row["repository"], "coarse_prediction": str(coarse_pred), "specialist_prediction": str(specialist_pred) if specialist_pred else None, "final_prediction": str(final_pred)}
    gold = row["gold_doc_category"]
    if gold == "developer_setup":
        if coarse_pred == "api_reference":
            developer_setup_path_analysis["coarse_api_specialist_never_reached"].append(item)
        elif coarse_pred == "model_contract":
            developer_setup_path_analysis["coarse_model_contract_specialist_never_reached"].append(item)
        elif final_pred == "configuration":
            developer_setup_path_analysis["coarse_family_specialist_configuration"].append(item)
        elif final_pred == "developer_setup":
            developer_setup_path_analysis["coarse_family_specialist_developer_setup_correct"].append(item)
    elif gold == "configuration":
        if coarse_pred == "api_reference":
            configuration_path_analysis["coarse_api"].append(item)
        elif coarse_pred == "model_contract":
            configuration_path_analysis["coarse_model_contract"].append(item)
        elif final_pred == "configuration":
            configuration_path_analysis["coarse_family_configuration_correct"].append(item)
        elif final_pred == "developer_setup":
            configuration_path_analysis["coarse_family_setup_error"].append(item)
    elif gold in {"api_reference", "model_contract"} and coarse_pred == "config_setup_family":
        api_model_damage_analysis[gold][str(final_pred)].append(item)

developer_setup_path_report = {key: {"count": len(value), "cases": value} for key, value in developer_setup_path_analysis.items()}
configuration_path_report = {key: {"count": len(value), "cases": value} for key, value in configuration_path_analysis.items()}
api_model_damage_report = {
    label: {final_label: {"count": len(cases), "cases": cases} for final_label, cases in grouped.items()}
    for label, grouped in api_model_damage_analysis.items()
}

selected_pairs = [(item["selected_class_weight"], item["selected_threshold"]) for item in specialist_selection_by_fold]
selected_threshold_values = [item["selected_threshold"] for item in specialist_selection_by_fold]
selection_stability = {
    "selected_class_weights": dict(Counter(item["selected_class_weight"] for item in specialist_selection_by_fold)),
    "selected_thresholds": dict(Counter(str(item["selected_threshold"]) for item in specialist_selection_by_fold)),
    "decision_instability": bool(
        len(set(selected_pairs)) == len(selected_pairs)
        or (max(selected_threshold_values) - min(selected_threshold_values) >= 0.25)
        or max(Counter(item["selected_class_weight"] for item in specialist_selection_by_fold).values()) < 3
    ),
}

repository_diagnostics = {}
for repository in sorted({row["repository"] for row in rows}):
    idx = np.asarray([row["repository"] == repository for row in rows])
    setup_idx = idx & setup_mask
    supports = Counter(y_all[idx])
    repository_diagnostics[repository] = {
        "total_rows": int(idx.sum()),
        "class_supports": dict(supports),
        "baseline_correct_count": int(np.sum(idx & (baseline_predictions == y_all))),
        "hierarchy_correct_count": int(np.sum(idx & (hierarchy_predictions == y_all))),
        "developer_setup_support": int(setup_idx.sum()),
        "baseline_setup_correct": int(np.sum(setup_idx & (baseline_predictions == "developer_setup"))),
        "hierarchy_setup_correct": int(np.sum(setup_idx & (hierarchy_predictions == "developer_setup"))),
        "setup_family_routed_count": int(np.sum(setup_idx & (coarse_predictions == "config_setup_family"))),
    }
    repository_diagnostics[repository]["net_accuracy_change"] = repository_diagnostics[repository]["hierarchy_correct_count"] - repository_diagnostics[repository]["baseline_correct_count"]
    repository_diagnostics[repository]["net_setup_change"] = repository_diagnostics[repository]["hierarchy_setup_correct"] - repository_diagnostics[repository]["baseline_setup_correct"]

repository_summary = {
    "repositories_improved": int(sum(1 for item in repository_diagnostics.values() if item["net_accuracy_change"] > 0)),
    "repositories_unchanged": int(sum(1 for item in repository_diagnostics.values() if item["net_accuracy_change"] == 0)),
    "repositories_degraded": int(sum(1 for item in repository_diagnostics.values() if item["net_accuracy_change"] < 0)),
    "setup_repositories_improved": int(sum(1 for item in repository_diagnostics.values() if item["developer_setup_support"] > 0 and item["net_setup_change"] > 0)),
    "setup_repositories_unchanged": int(sum(1 for item in repository_diagnostics.values() if item["developer_setup_support"] > 0 and item["net_setup_change"] == 0)),
    "setup_repositories_degraded": int(sum(1 for item in repository_diagnostics.values() if item["developer_setup_support"] > 0 and item["net_setup_change"] < 0)),
}

def class_f1_metric(label):
    def fn(gold, pred):
        return precision_recall_fscore_support(gold, pred, labels=LABELS, zero_division=0)[2][LABELS.index(label)]
    return fn

def setup_recall_metric(gold, pred):
    return precision_recall_fscore_support(gold, pred, labels=LABELS, zero_division=0)[1][LABELS.index("developer_setup")]

def delta_cluster_bootstrap(metric_fn):
    repositories = np.asarray([row["repository"] for row in rows])
    unique = np.asarray(sorted(set(repositories)))
    rng = np.random.default_rng(SEED)
    values = []
    for _ in range(2000):
        sampled = rng.choice(unique, size=len(unique), replace=True)
        idx = np.concatenate([np.where(repositories == repo)[0] for repo in sampled])
        values.append(metric_fn(y_all[idx], hierarchy_predictions[idx]) - metric_fn(y_all[idx], baseline_predictions[idx]))
    arr = np.asarray(values, dtype=float)
    return {"mean_delta": float(np.mean(arr)), "ci_2_5": float(np.percentile(arr, 2.5)), "ci_97_5": float(np.percentile(arr, 97.5)), "probability_delta_gt_zero": float(np.mean(arr > 0))}

repository_cluster_bootstrap = {
    "macro_f1": delta_cluster_bootstrap(lambda g, p: f1_score(g, p, labels=LABELS, average="macro", zero_division=0)),
    "balanced_accuracy": delta_cluster_bootstrap(balanced_accuracy_score),
    "api_reference_f1": delta_cluster_bootstrap(class_f1_metric("api_reference")),
    "configuration_f1": delta_cluster_bootstrap(class_f1_metric("configuration")),
    "developer_setup_f1": delta_cluster_bootstrap(class_f1_metric("developer_setup")),
    "model_contract_f1": delta_cluster_bootstrap(class_f1_metric("model_contract")),
    "developer_setup_recall": delta_cluster_bootstrap(setup_recall_metric),
}

setup_gain_by_repo = {repo: item["net_setup_change"] for repo, item in repository_diagnostics.items() if item["net_setup_change"] > 0}
total_setup_gain = sum(setup_gain_by_repo.values())
max_repo_setup_gain = max(setup_gain_by_repo.values()) if setup_gain_by_repo else 0
gates = {
    "macro_f1_delta_ge_0_02": comparison["delta"]["macro_f1"] >= 0.02,
    "balanced_accuracy_not_worse": hierarchy_metrics["balanced_accuracy"] >= baseline_metrics["balanced_accuracy"],
    "developer_setup_f1_ge_0_25": hierarchy_metrics["per_class"]["developer_setup"]["f1"] >= 0.25,
    "developer_setup_f1_delta_ge_0_10": comparison["delta"]["developer_setup_f1"] >= 0.10,
    "developer_setup_recall_ge_0_25": hierarchy_metrics["per_class"]["developer_setup"]["recall"] >= 0.25,
    "setup_family_routing_recall_ge_0_50": setup_family_routing_recall >= 0.50,
    "api_configuration_model_contract_f1_safety": all(comparison["delta"][key] >= -0.05 for key in ["api_reference_f1", "configuration_f1", "model_contract_f1"]),
    "setup_improves_across_at_least_3_repositories": len(setup_gain_by_repo) >= 3,
    "setup_gain_not_majority_from_one_repository": total_setup_gain > 0 and max_repo_setup_gain <= total_setup_gain / 2,
    "bootstrap_macro_delta_probability_ge_0_90": repository_cluster_bootstrap["macro_f1"]["probability_delta_gt_zero"] >= 0.90,
    "no_leakage_repository_overlap_or_forbidden_evidence_violation": True,
}
if all(gates.values()):
    decision_label = "GO"
elif comparison["delta"]["developer_setup_f1"] > 0:
    decision_label = "PARTIAL_NO_GO"
else:
    decision_label = "NO_BENEFIT"
decision = {"decision": decision_label, "gates": gates, "setup_gain_by_repository": setup_gain_by_repo}

with open(OUTPUT_DIR / "paired_oof_predictions.jsonl", "w", encoding="utf-8", newline="\n") as out:
    for row, base, coarse_pred, specialist_pred, final_pred, score in zip(rows, baseline_predictions, coarse_predictions, specialist_predictions_if_applicable, hierarchy_predictions, specialist_scores):
        out.write(json.dumps({
            "case_id": row["case_id"],
            "repository": row["repository"],
            "language": row["language"],
            "gold": row["gold_doc_category"],
            "baseline_four_class_prediction": str(base),
            "coarse_family_prediction": str(coarse_pred),
            "specialist_prediction_if_applicable": str(specialist_pred) if specialist_pred else None,
            "specialist_score_if_applicable": None if np.isnan(score) else float(score),
            "hierarchy_final_prediction": str(final_pred),
        }, ensure_ascii=False, sort_keys=True) + "\n")

write_json(OUTPUT_DIR / "coarse_oof_metrics.json", coarse_metrics)
write_json(OUTPUT_DIR / "baseline_oof_metrics.json", baseline_metrics)
write_json(OUTPUT_DIR / "hierarchy_oof_metrics.json", hierarchy_metrics)
write_json(OUTPUT_DIR / "hierarchy_comparison.json", comparison)
write_json(OUTPUT_DIR / "coarse_diagnostics.json", coarse_diagnostics)
write_json(OUTPUT_DIR / "developer_setup_path_analysis.json", developer_setup_path_report)
write_json(OUTPUT_DIR / "configuration_path_analysis.json", configuration_path_report)
write_json(OUTPUT_DIR / "api_model_contract_damage_analysis.json", api_model_damage_report)
write_json(OUTPUT_DIR / "selection_stability.json", selection_stability)
write_json(OUTPUT_DIR / "repository_diagnostics.json", {"summary": repository_summary, "repositories": repository_diagnostics})
write_json(OUTPUT_DIR / "repository_cluster_bootstrap.json", repository_cluster_bootstrap)
write_json(OUTPUT_DIR / "decision.json", decision)
'''
    figures = r'''
def plot_confusion(matrix, labels, path, title, normalized=False):
    matrix = np.asarray(matrix)
    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(matrix, cmap="Blues", vmin=0 if normalized else None, vmax=1 if normalized else None)
    ax.set_xticks(range(len(labels)), labels, rotation=25, ha="right")
    ax.set_yticks(range(len(labels)), labels)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Gold")
    ax.set_title(title)
    for i in range(len(labels)):
        for j in range(len(labels)):
            ax.text(j, i, f"{matrix[i, j]:.2f}" if normalized else str(int(matrix[i, j])), ha="center", va="center")
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)

def simple_bar(path, labels, values, title, ylabel):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(labels, values)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    if values and max(values) <= 1 and min(values) >= -1:
        ax.set_ylim(min(0, min(values) - 0.05), 1)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)

plot_confusion(coarse_metrics["confusion_matrix"], COARSE_LABELS, FIGURES_DIR / "coarse_confusion_matrix.png", "Coarse family confusion matrix")
plot_confusion(coarse_metrics["normalized_confusion_matrix"], COARSE_LABELS, FIGURES_DIR / "coarse_normalized_confusion_matrix.png", "Coarse normalized confusion matrix", normalized=True)
plot_confusion(baseline_metrics["confusion_matrix"], LABELS, FIGURES_DIR / "baseline_confusion_matrix.png", "Original four-class baseline confusion matrix")
plot_confusion(hierarchy_metrics["confusion_matrix"], LABELS, FIGURES_DIR / "hierarchy_confusion_matrix.png", "Coarse-to-fine hierarchy confusion matrix")
plot_confusion(hierarchy_metrics["normalized_confusion_matrix"], LABELS, FIGURES_DIR / "hierarchy_normalized_confusion_matrix.png", "Hierarchy normalized confusion matrix", normalized=True)
simple_bar(FIGURES_DIR / "baseline_vs_hierarchy_macro_f1.png", ["baseline", "hierarchy"], [baseline_metrics["macro_f1"], hierarchy_metrics["macro_f1"]], "Macro-F1", "Macro-F1")
simple_bar(FIGURES_DIR / "baseline_vs_hierarchy_balanced_accuracy.png", ["baseline", "hierarchy"], [baseline_metrics["balanced_accuracy"], hierarchy_metrics["balanced_accuracy"]], "Balanced accuracy", "Balanced accuracy")
simple_bar(FIGURES_DIR / "baseline_vs_hierarchy_per_class_f1.png", LABELS, [comparison["delta"][f"{label}_f1"] for label in LABELS], "Per-class F1 delta", "Hierarchy - baseline")
simple_bar(FIGURES_DIR / "baseline_vs_hierarchy_setup_f1.png", ["baseline", "hierarchy"], [baseline_metrics["per_class"]["developer_setup"]["f1"], hierarchy_metrics["per_class"]["developer_setup"]["f1"]], "developer_setup F1", "F1")
simple_bar(FIGURES_DIR / "baseline_vs_hierarchy_setup_recall.png", ["baseline", "hierarchy"], [baseline_metrics["per_class"]["developer_setup"]["recall"], hierarchy_metrics["per_class"]["developer_setup"]["recall"]], "developer_setup recall", "Recall")
simple_bar(FIGURES_DIR / "setup_family_routing_recall_by_fold.png", [str(item["fold"]) for item in outer_fold_metrics], [item["setup_family_routing_recall"] for item in outer_fold_metrics], "Setup family routing recall by fold", "Recall")
simple_bar(FIGURES_DIR / "outer_fold_macro_f1_delta.png", [str(item["fold"]) for item in outer_fold_metrics], [item["deltas"]["macro_f1"] for item in outer_fold_metrics], "Outer-fold Macro-F1 delta", "Hierarchy - baseline")
simple_bar(FIGURES_DIR / "outer_fold_setup_f1_delta.png", [str(item["fold"]) for item in outer_fold_metrics], [item["deltas"]["developer_setup_f1"] for item in outer_fold_metrics], "Outer-fold setup F1 delta", "Hierarchy - baseline")

table_rows = [
    ("Accuracy", baseline_metrics["accuracy"], hierarchy_metrics["accuracy"], comparison["delta"]["accuracy"]),
    ("Macro-F1", baseline_metrics["macro_f1"], hierarchy_metrics["macro_f1"], comparison["delta"]["macro_f1"]),
    ("Balanced accuracy", baseline_metrics["balanced_accuracy"], hierarchy_metrics["balanced_accuracy"], comparison["delta"]["balanced_accuracy"]),
    ("API F1", baseline_metrics["per_class"]["api_reference"]["f1"], hierarchy_metrics["per_class"]["api_reference"]["f1"], comparison["delta"]["api_reference_f1"]),
    ("Configuration F1", baseline_metrics["per_class"]["configuration"]["f1"], hierarchy_metrics["per_class"]["configuration"]["f1"], comparison["delta"]["configuration_f1"]),
    ("Developer setup precision", baseline_metrics["per_class"]["developer_setup"]["precision"], hierarchy_metrics["per_class"]["developer_setup"]["precision"], comparison["delta"]["developer_setup_precision"]),
    ("Developer setup recall", baseline_metrics["per_class"]["developer_setup"]["recall"], hierarchy_metrics["per_class"]["developer_setup"]["recall"], comparison["delta"]["developer_setup_recall"]),
    ("Developer setup F1", baseline_metrics["per_class"]["developer_setup"]["f1"], hierarchy_metrics["per_class"]["developer_setup"]["f1"], comparison["delta"]["developer_setup_f1"]),
    ("Model contract F1", baseline_metrics["per_class"]["model_contract"]["f1"], hierarchy_metrics["per_class"]["model_contract"]["f1"], comparison["delta"]["model_contract_f1"]),
]
results_md = "# Stage-2 coarse-to-fine hierarchy V1\n\n"
results_md += "This is **not external validation**. It is repository-grouped OOF evidence on the frozen natural primary-four train universe.\n\n"
results_md += f"Decision: **{decision['decision']}**\n\n"
results_md += "| Metric | Original 4-class MiniLM | Coarse-to-fine hierarchy | Delta |\n| --- | ---: | ---: | ---: |\n"
for name, base, hier, delta in table_rows:
    results_md += f"| {name} | {base:.4f} | {hier:.4f} | {delta:+.4f} |\n"
results_md += f"\nLevel-1 config_setup_family recall: **{coarse_metrics['per_class']['config_setup_family']['recall']:.4f}**\n"
results_md += f"\nSetup family routing recall: **{setup_family_routing_recall:.4f}**\n\n"
results_md += "## GO / NO-GO gates\n\n```json\n" + json.dumps(gates, indent=2, sort_keys=True) + "\n```\n"
(OUTPUT_DIR / "RESULTS.md").write_text(results_md, encoding="utf-8")

experiment_manifest = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "data_path": str(DATA_PATH),
    "data_sha256": sha256_file(DATA_PATH),
    "row_count": len(rows),
    "category_counts": dict(Counter(y_all)),
    "coarse_counts": dict(Counter(coarse_all)),
    "minilm_model": MINILM_MODEL_NAME,
    "minilm_revision": MINILM_MODEL_REVISION,
    "outer_cv": {"splitter": "StratifiedGroupKFold", "n_splits": outer_n_splits, "shuffle": True, "random_state": SEED},
    "coarse_target_mapping": COARSE_MAPPING,
    "coarse_classifier": {"class": "LogisticRegression", "C": 1.0, "solver": "lbfgs", "max_iter": 2000, "random_state": SEED, "class_weight": None},
    "specialist_inner_selection": {"class_weight_grid": CLASS_WEIGHT_GRID, "threshold_grid": THRESHOLD_GRID, "precision_floor": PRECISION_FLOOR, "inner_cv": "StratifiedGroupKFold 4 folds fallback 3, seed 42 + outer_fold_id"},
    "confirmation_accessed": False,
    "frozen_322_validation_accessed": False,
}
write_json(OUTPUT_DIR / "experiment_manifest.json", experiment_manifest)

zip_path = Path("/content/stage2_coarse_to_fine_hierarchy_v1_results.zip")
if zip_path.exists():
    zip_path.unlink()
lightweight_files = [
    "RESULTS.md",
    "experiment_manifest.json",
    "outer_fold_manifest.json",
    "outer_fold_metrics.json",
    "coarse_oof_metrics.json",
    "baseline_oof_metrics.json",
    "hierarchy_oof_metrics.json",
    "paired_oof_predictions.jsonl",
    "hierarchy_comparison.json",
    "coarse_diagnostics.json",
    "developer_setup_path_analysis.json",
    "configuration_path_analysis.json",
    "api_model_contract_damage_analysis.json",
    "specialist_selection_by_fold.json",
    "selection_stability.json",
    "repository_diagnostics.json",
    "repository_cluster_bootstrap.json",
    "decision.json",
]
with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for name in lightweight_files:
        archive.write(OUTPUT_DIR / name, arcname=name)
    for figure in FIGURES_DIR.glob("*.png"):
        archive.write(figure, arcname=f"figures/{figure.name}")
print("Created lightweight result package:", zip_path)
'''
    download = """
from google.colab import files
files.download("/content/stage2_coarse_to_fine_hierarchy_v1_results.zip")
"""
    return {
        "cells": [
            nb_cell("markdown", title),
            nb_cell("code", deps),
            nb_cell("code", imports),
            nb_cell("code", constants),
            nb_cell("code", data_helpers),
            nb_cell("code", helpers),
            nb_cell("code", integrity),
            nb_cell("code", encoder),
            nb_cell("code", features_splits),
            nb_cell("code", experiment),
            nb_cell("code", diagnostics),
            nb_cell("code", figures),
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


def compile_notebook_code_cells(path: Path = NOTEBOOK_PATH) -> list[str]:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    for index, cell in enumerate(notebook.get("cells", []), 1):
        if cell.get("cell_type") != "code":
            continue
        source = "".join(cell.get("source", []))
        executable = [line.strip() for line in source.splitlines() if line.strip() and not line.strip().startswith("#")]
        if executable and executable[0].startswith("!"):
            continue
        try:
            ast.parse(source)
        except SyntaxError as exc:
            errors.append(f"cell {index}: {exc}")
    return errors


def write_readme() -> None:
    README_PATH.parent.mkdir(parents=True, exist_ok=True)
    README_PATH.write_text(
        f"""# Stage-2 coarse-to-fine hierarchy V1

This is the final train-side Stage-2 architecture experiment. It keeps the
winning frozen MiniLM hybrid representation, replaces the first decision with a
three-way documentation-family classifier, and applies Specialist V2 only
inside `config_setup_family`.

Data:

- `data/final_v2/architecture_challenge_v1/natural_train_primary_four.jsonl`
- rows: {EXPECTED_TOTAL}
- canonical counts: {EXPECTED_COUNTS}
- coarse counts: {EXPECTED_COARSE_COUNTS}
- SHA256: `{EXPECTED_TRAIN_SHA256}`

Coarse target mapping:

- api_reference -> api_reference
- configuration -> config_setup_family
- developer_setup -> config_setup_family
- model_contract -> model_contract

Frozen representation:

- encoder: `{MINILM_MODEL_NAME}`
- revision: `{MINILM_MODEL_REVISION}`
- semantic chunking: 1000 chars, max 2 chunks per side
- code TF-IDF: char_wb 3–5 grams, min_df=2, max_features=20000
- classifier family: LogisticRegression only

Specialist V2 decision grid:

- class weights: {CLASS_WEIGHT_GRID}
- thresholds: {THRESHOLD_GRID}
- precision floor: {PRECISION_FLOOR}

Inference rule:

The specialist runs iff Level 1 predicts `config_setup_family`. Level-1
`api_reference` and `model_contract` predictions finalize directly to those
same canonical labels. There is no post-hoc four-way router and no routing
threshold.

Notebook: `notebooks/category_stage2_coarse_to_fine_hierarchy_v1.ipynb`

The frozen 322-row development validation is not required and must not be
loaded by this train-side pilot.
""",
        encoding="utf-8",
    )


def main() -> None:
    verify_train_export()
    write_notebook()
    write_readme()
    errors = compile_notebook_code_cells()
    if errors:
        raise SyntaxError("; ".join(errors))
    print(
        json.dumps(
            {
                "status": "prepared",
                "notebook": str(NOTEBOOK_PATH.relative_to(ROOT)),
                "readme": str(README_PATH.relative_to(ROOT)),
                "data": str(TRAIN_JSONL.relative_to(ROOT)),
                "data_sha256": sha256_file(TRAIN_JSONL),
                "local_oof_executed": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
