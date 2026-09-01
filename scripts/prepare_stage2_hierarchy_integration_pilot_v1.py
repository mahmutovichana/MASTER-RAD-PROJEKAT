"""Prepare the Stage-2 hierarchy integration pilot V1 Colab notebook.

This local script creates a self-contained Colab notebook and lightweight
methodology README. It verifies only the frozen 1038-row natural train export.
It must not run the final hierarchy OOF experiment locally.
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
NOTEBOOK_PATH = ROOT / "notebooks" / "category_stage2_hierarchical_integration_pilot_v1.ipynb"
README_PATH = ROOT / "experiments" / "category_hierarchy_integration_pilot_v1" / "README.md"

LABELS = ["api_reference", "configuration", "developer_setup", "model_contract"]
SPECIALIST_LABELS = ["configuration", "developer_setup"]
EXPECTED_TOTAL = 1038
EXPECTED_COUNTS = {
    "api_reference": 412,
    "configuration": 277,
    "developer_setup": 88,
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
    if len(rows) != EXPECTED_TOTAL:
        raise AssertionError(f"Expected {EXPECTED_TOTAL} rows, got {len(rows)}")
    if dict(counts) != EXPECTED_COUNTS:
        raise AssertionError(f"Expected {EXPECTED_COUNTS}, got {dict(counts)}")
    if sha256_file(TRAIN_JSONL) != EXPECTED_TRAIN_SHA256:
        raise AssertionError("Frozen primary-four train file hash changed")
    if any(row.get("partition") != "development_train" for row in rows):
        raise AssertionError("Hierarchy pilot may use only development_train rows")
    if any(row.get("gold_doc_category") not in LABELS for row in rows):
        raise AssertionError("Hierarchy pilot may use only the four primary categories")
    if manifest["artifacts"]["natural_train_primary_four.jsonl"]["sha256"] != EXPECTED_TRAIN_SHA256:
        raise AssertionError("Manifest train artifact hash does not match the frozen train export")
    if manifest.get("confirmation_accessed") is not False:
        raise AssertionError("Confirmation data must not be part of this export")
    if manifest.get("controlled_or_synthetic_rows_used") is not False:
        raise AssertionError("Controlled/synthetic data must not be part of this export")


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
# Stage-2 hierarchical integration pilot V1

This Colab notebook evaluates one predeclared hierarchy: the frozen four-class
MiniLM hybrid model routes only `configuration`/`developer_setup` general
predictions into the nested cost-sensitive Specialist V2 decision procedure.

This is train-side repository-grouped OOF evidence only. It must not load the
frozen 322-row development validation.
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
SPECIALIST_LABELS = {py(SPECIALIST_LABELS)}
SAFE_FIELDS = {py(SAFE_FIELDS)}
EXPECTED_TOTAL = {EXPECTED_TOTAL}
EXPECTED_COUNTS = {py(EXPECTED_COUNTS)}
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

OUTPUT_DIR = Path("/content/experiments/category_hierarchy_integration_pilot_v1")
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
    print("Upload the repository ZIP or these two train-only files: natural_train_primary_four.jsonl and export_manifest.json")
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
print("Using frozen primary-four train export:", TRAIN_DIR)
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


def metric_bundle(y_true, y_pred, labels=LABELS):
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
assert sha256_file(DATA_PATH) == EXPECTED_TRAIN_SHA256
assert set(row["partition"] for row in rows) == {"development_train"}
assert all(set(row) == set(SAFE_FIELDS) for row in rows)
for row in rows:
    assert row["gold_doc_category"] in LABELS
    combined = (build_code_text(row) + "\\n" + build_docs_text(row)).lower()
    repo = str(row.get("repository") or "").lower()
    assert not repo or "/" not in repo or repo not in combined
print("Verified frozen primary-four train data:", Counter(row["gold_doc_category"] for row in rows))
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
    feature_split = r'''
code_texts = [build_code_text(row) for row in rows]
docs_texts = [build_docs_text(row) for row in rows]
all_code_embeddings, code_cache = encode_texts_cached("code", code_texts, encoder)
all_docs_embeddings, docs_cache = encode_texts_cached("docs", docs_texts, encoder)
assert all_code_embeddings.shape == all_docs_embeddings.shape


def build_fold_features(train_idx, eval_idx, *, labels):
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
    return x_train, x_eval, {"labels": labels, "tfidf_fit_rows": int(len(train_idx)), "tfidf_eval_rows": int(len(eval_idx)), "eval_enters_tfidf_fit": False}


def grouped_splits(indices, *, labels, n_splits, seed):
    idx = np.asarray(indices, dtype=int)
    selected_rows = [rows[int(i)] for i in idx]
    y = labels_for(selected_rows)
    groups = np.asarray([row["repository"] for row in selected_rows])
    splitter = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    out = []
    for train_local, eval_local in splitter.split(np.arange(len(idx)), y, groups):
        train_idx = idx[train_local]
        eval_idx = idx[eval_local]
        y_train = labels_for([rows[int(i)] for i in train_idx])
        y_eval = labels_for([rows[int(i)] for i in eval_idx])
        g_train = {rows[int(i)]["repository"] for i in train_idx}
        g_eval = {rows[int(i)]["repository"] for i in eval_idx}
        if g_train & g_eval:
            raise AssertionError("Repository overlap inside grouped split")
        if set(y_train) != set(labels) or set(y_eval) != set(labels):
            raise ValueError("Fold missing a required class")
        out.append((train_idx, eval_idx))
    return out


def choose_outer_splits():
    for n_splits in [5, 4, 3]:
        try:
            return n_splits, grouped_splits(np.arange(len(rows)), labels=LABELS, n_splits=n_splits, seed=SEED)
        except ValueError:
            continue
    raise RuntimeError("No structurally valid outer split.")


def choose_inner_splits(specialist_outer_train_idx, outer_fold_id):
    for n_splits in [4, 3]:
        try:
            return n_splits, grouped_splits(specialist_outer_train_idx, labels=SPECIALIST_LABELS, n_splits=n_splits, seed=SEED + outer_fold_id)
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
    assert set(labels_for(train_rows)) == set(LABELS)
    assert set(labels_for(eval_rows)) == set(LABELS)
    outer_manifest["folds"].append({
        "fold": fold_id,
        "train_rows": int(len(train_idx)),
        "eval_rows": int(len(eval_idx)),
        "train_category_counts": dict(Counter(labels_for(train_rows))),
        "eval_category_counts": dict(Counter(labels_for(eval_rows))),
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
    threshold_closeness = -abs(item["threshold"] - 0.5)
    lower_weight_rank = -item["class_weight_rank"]
    return (
        metrics["macro_f1"],
        setup["f1"],
        metrics["balanced_accuracy"],
        setup["precision"],
        threshold_closeness,
        lower_weight_rank,
    )


def select_specialist_params(outer_fold_id, specialist_outer_train_idx):
    inner_n_splits, inner_folds = choose_inner_splits(specialist_outer_train_idx, outer_fold_id)
    position = {int(global_index): pos for pos, global_index in enumerate(specialist_outer_train_idx)}
    candidate_probs = defaultdict(lambda: np.zeros(len(specialist_outer_train_idx), dtype=float))
    fit_audit = []
    for inner_fold_id, (inner_train_idx, inner_eval_idx) in enumerate(inner_folds, 1):
        x_inner_train, x_inner_eval, feature_meta = build_fold_features(inner_train_idx, inner_eval_idx, labels=SPECIALIST_LABELS)
        y_inner_train = labels_for([rows[int(i)] for i in inner_train_idx])
        assert set(y_inner_train) == set(SPECIALIST_LABELS)
        for weight_spec in CLASS_WEIGHT_GRID:
            clf = LogisticRegression(C=1.0, solver="lbfgs", max_iter=2000, random_state=SEED, class_weight=weight_spec["value"])
            clf.fit(x_inner_train, y_inner_train)
            prob_setup = setup_probability(clf, x_inner_eval)
            for global_index, prob in zip(inner_eval_idx, prob_setup):
                candidate_probs[weight_spec["name"]][position[int(global_index)]] = float(prob)
            fit_audit.append({"inner_fold": inner_fold_id, "class_weight": weight_spec["name"], "train_rows": int(len(inner_train_idx)), "eval_rows": int(len(inner_eval_idx)), "feature_meta": feature_meta})
    y_specialist_train = labels_for([rows[int(i)] for i in specialist_outer_train_idx])
    scored = []
    for weight_spec in CLASS_WEIGHT_GRID:
        for threshold in THRESHOLD_GRID:
            pred = predict_from_threshold(candidate_probs[weight_spec["name"]], threshold)
            metrics = metric_bundle(y_specialist_train, pred, labels=SPECIALIST_LABELS)
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


def apply_routing_rule(general_prediction, specialist_prediction):
    if general_prediction in {"configuration", "developer_setup"}:
        return specialist_prediction
    return general_prediction


y_all = labels_for(rows)
baseline_predictions = np.asarray([""] * len(rows), dtype=object)
hierarchy_predictions = np.asarray([""] * len(rows), dtype=object)
general_probabilities = np.zeros((len(rows), len(LABELS)), dtype=float)
specialist_scores = np.full(len(rows), np.nan, dtype=float)
routed = np.zeros(len(rows), dtype=bool)
specialist_selection_by_fold = []
outer_fold_metrics = []

for outer_fold_id, (outer_train_idx, outer_eval_idx) in enumerate(outer_folds, 1):
    x_general_train, x_general_eval, general_feature_meta = build_fold_features(outer_train_idx, outer_eval_idx, labels=LABELS)
    y_general_train = labels_for([rows[int(i)] for i in outer_train_idx])
    y_general_eval = labels_for([rows[int(i)] for i in outer_eval_idx])
    general_clf = LogisticRegression(C=1.0, solver="lbfgs", max_iter=2000, random_state=SEED)
    general_clf.fit(x_general_train, y_general_train)
    general_pred = general_clf.predict(x_general_eval)
    general_prob = classifier_probabilities(general_clf, x_general_eval, LABELS)

    specialist_outer_train_idx = np.asarray([int(i) for i in outer_train_idx if rows[int(i)]["gold_doc_category"] in SPECIALIST_LABELS], dtype=int)
    selected, grid, inner_meta = select_specialist_params(outer_fold_id, specialist_outer_train_idx)
    x_spec_train, x_spec_eval, specialist_feature_meta = build_fold_features(specialist_outer_train_idx, outer_eval_idx, labels=SPECIALIST_LABELS)
    y_spec_train = labels_for([rows[int(i)] for i in specialist_outer_train_idx])
    specialist_clf = LogisticRegression(C=1.0, solver="lbfgs", max_iter=2000, random_state=SEED, class_weight=selected["class_weight_value"])
    specialist_clf.fit(x_spec_train, y_spec_train)
    spec_prob_setup = setup_probability(specialist_clf, x_spec_eval)
    spec_pred = predict_from_threshold(spec_prob_setup, selected["threshold"])

    final_pred = []
    for local_pos, global_index in enumerate(outer_eval_idx):
        baseline_predictions[int(global_index)] = str(general_pred[local_pos])
        general_probabilities[int(global_index)] = general_prob[local_pos]
        should_route = str(general_pred[local_pos]) in {"configuration", "developer_setup"}
        routed[int(global_index)] = should_route
        if should_route:
            specialist_scores[int(global_index)] = float(spec_prob_setup[local_pos])
            final = str(spec_pred[local_pos])
        else:
            final = str(general_pred[local_pos])
        hierarchy_predictions[int(global_index)] = final
        final_pred.append(final)

    fold_baseline_metrics = metric_bundle(y_general_eval, general_pred, labels=LABELS)
    fold_hierarchy_metrics = metric_bundle(y_general_eval, np.asarray(final_pred), labels=LABELS)
    outer_fold_metrics.append({
        "fold": outer_fold_id,
        "baseline": fold_baseline_metrics,
        "hierarchy": fold_hierarchy_metrics,
        "deltas": {
            "macro_f1": fold_hierarchy_metrics["macro_f1"] - fold_baseline_metrics["macro_f1"],
            "balanced_accuracy": fold_hierarchy_metrics["balanced_accuracy"] - fold_baseline_metrics["balanced_accuracy"],
            "developer_setup_f1": fold_hierarchy_metrics["per_class"]["developer_setup"]["f1"] - fold_baseline_metrics["per_class"]["developer_setup"]["f1"],
        },
    })
    specialist_selection_by_fold.append({
        "outer_fold": outer_fold_id,
        "selected_class_weight": selected["class_weight"],
        "selected_threshold": float(selected["threshold"]),
        "precision_floor_satisfied": bool(selected["precision_floor_satisfied"]),
        "grid": grid,
        "inner_meta": inner_meta,
        "general_feature_meta": general_feature_meta,
        "specialist_feature_meta": specialist_feature_meta,
        "specialist_train_rows": int(len(specialist_outer_train_idx)),
    })

assert all(item in LABELS for item in baseline_predictions)
assert all(item in LABELS for item in hierarchy_predictions)
assert len(baseline_predictions) == len(hierarchy_predictions) == len(rows)
assert np.all([apply_routing_rule(base, hier) == hier if base in {"configuration", "developer_setup"} else base == hier for base, hier in zip(baseline_predictions, hierarchy_predictions)])
write_json(OUTPUT_DIR / "outer_fold_metrics.json", outer_fold_metrics)
write_json(OUTPUT_DIR / "specialist_selection_by_fold.json", specialist_selection_by_fold)
'''
    diagnostics = r'''
baseline_metrics = metric_bundle(y_all, baseline_predictions, labels=LABELS)
hierarchy_metrics = metric_bundle(y_all, hierarchy_predictions, labels=LABELS)
comparison = {
    "baseline": baseline_metrics,
    "hierarchy": hierarchy_metrics,
    "delta": {
        "macro_f1": hierarchy_metrics["macro_f1"] - baseline_metrics["macro_f1"],
        "balanced_accuracy": hierarchy_metrics["balanced_accuracy"] - baseline_metrics["balanced_accuracy"],
        "api_reference_f1": hierarchy_metrics["per_class"]["api_reference"]["f1"] - baseline_metrics["per_class"]["api_reference"]["f1"],
        "configuration_f1": hierarchy_metrics["per_class"]["configuration"]["f1"] - baseline_metrics["per_class"]["configuration"]["f1"],
        "developer_setup_f1": hierarchy_metrics["per_class"]["developer_setup"]["f1"] - baseline_metrics["per_class"]["developer_setup"]["f1"],
        "model_contract_f1": hierarchy_metrics["per_class"]["model_contract"]["f1"] - baseline_metrics["per_class"]["model_contract"]["f1"],
        "developer_setup_precision": hierarchy_metrics["per_class"]["developer_setup"]["precision"] - baseline_metrics["per_class"]["developer_setup"]["precision"],
        "developer_setup_recall": hierarchy_metrics["per_class"]["developer_setup"]["recall"] - baseline_metrics["per_class"]["developer_setup"]["recall"],
    },
    "changed_predictions": {
        "count": int(np.sum(baseline_predictions != hierarchy_predictions)),
        "correct_before": int(np.sum((baseline_predictions != hierarchy_predictions) & (baseline_predictions == y_all))),
        "correct_after": int(np.sum((baseline_predictions != hierarchy_predictions) & (hierarchy_predictions == y_all))),
    },
}
comparison["changed_predictions"]["net_corrected_cases"] = comparison["changed_predictions"]["correct_after"] - comparison["changed_predictions"]["correct_before"]

routing_diagnostics = {
    "total_rows_routed": int(routed.sum()),
    "percent_rows_routed": float(routed.mean()),
    "by_true_class": {},
    "routed_gold_distribution": dict(Counter(y_all[routed])),
    "routed_general_prediction_distribution": dict(Counter(baseline_predictions[routed])),
    "routed_specialist_final_distribution": dict(Counter(hierarchy_predictions[routed])),
}
for label in LABELS:
    idx = y_all == label
    routing_diagnostics["by_true_class"][label] = {
        "support": int(idx.sum()),
        "routed_count": int(np.sum(idx & routed)),
        "not_routed_count": int(np.sum(idx & ~routed)),
        "routing_recall_for_this_true_class": float(np.sum(idx & routed) / max(1, idx.sum())),
    }

setup_idx = y_all == "developer_setup"
setup_categories = {
    "baseline_correct_and_hierarchy_remains_correct": [],
    "configuration_to_setup_rescues": [],
    "baseline_setup_changed_wrong_to_configuration": [],
    "baseline_api_reference_not_routed": [],
    "baseline_model_contract_not_routed": [],
}
for row, base, hier in zip(rows, baseline_predictions, hierarchy_predictions):
    if row["gold_doc_category"] != "developer_setup":
        continue
    item = {"case_id": row["case_id"], "repository": row["repository"], "baseline": str(base), "hierarchy": str(hier)}
    if base == "developer_setup" and hier == "developer_setup":
        setup_categories["baseline_correct_and_hierarchy_remains_correct"].append(item)
    elif base == "configuration" and hier == "developer_setup":
        setup_categories["configuration_to_setup_rescues"].append(item)
    elif base == "developer_setup" and hier == "configuration":
        setup_categories["baseline_setup_changed_wrong_to_configuration"].append(item)
    elif base == "api_reference":
        setup_categories["baseline_api_reference_not_routed"].append(item)
    elif base == "model_contract":
        setup_categories["baseline_model_contract_not_routed"].append(item)

developer_setup_rescue_analysis = {
    "setup_correct_baseline": int(np.sum(setup_idx & (baseline_predictions == "developer_setup"))),
    "setup_correct_hierarchy": int(np.sum(setup_idx & (hierarchy_predictions == "developer_setup"))),
    "net_setup_gain": int(np.sum(setup_idx & (hierarchy_predictions == "developer_setup")) - np.sum(setup_idx & (baseline_predictions == "developer_setup"))),
    "configuration_to_setup_rescues": len(setup_categories["configuration_to_setup_rescues"]),
    "case_groups": setup_categories,
}

new_errors = []
rescued_errors = []
for row, base, hier in zip(rows, baseline_predictions, hierarchy_predictions):
    base_correct = base == row["gold_doc_category"]
    hier_correct = hier == row["gold_doc_category"]
    item = {"case_id": row["case_id"], "repository": row["repository"], "gold": row["gold_doc_category"], "baseline": str(base), "hierarchy": str(hier)}
    if base_correct and not hier_correct:
        new_errors.append(item)
    if not base_correct and hier_correct:
        rescued_errors.append(item)
damage_analysis = {
    "hierarchy_new_error_count": len(new_errors),
    "hierarchy_rescued_error_count": len(rescued_errors),
    "true_configuration_baseline_correct_changed_to_setup": [
        item for item in new_errors
        if item["gold"] == "configuration" and item["baseline"] == "configuration" and item["hierarchy"] == "developer_setup"
    ],
}
with open(OUTPUT_DIR / "hierarchy_new_errors.jsonl", "w", encoding="utf-8", newline="\n") as out:
    for item in new_errors:
        out.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")
with open(OUTPUT_DIR / "hierarchy_rescued_errors.jsonl", "w", encoding="utf-8", newline="\n") as out:
    for item in rescued_errors:
        out.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")

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
    setup_mask = idx & (y_all == "developer_setup")
    repository_diagnostics[repository] = {
        "row_count": int(idx.sum()),
        "developer_setup_support": int(setup_mask.sum()),
        "baseline_correct": int(np.sum(idx & (baseline_predictions == y_all))),
        "hierarchy_correct": int(np.sum(idx & (hierarchy_predictions == y_all))),
        "baseline_setup_correct": int(np.sum(setup_mask & (baseline_predictions == "developer_setup"))),
        "hierarchy_setup_correct": int(np.sum(setup_mask & (hierarchy_predictions == "developer_setup"))),
    }
    repository_diagnostics[repository]["net_accuracy_change"] = repository_diagnostics[repository]["hierarchy_correct"] - repository_diagnostics[repository]["baseline_correct"]
    repository_diagnostics[repository]["net_setup_change"] = repository_diagnostics[repository]["hierarchy_setup_correct"] - repository_diagnostics[repository]["baseline_setup_correct"]

repo_summary = {
    "repositories_improved": int(sum(1 for item in repository_diagnostics.values() if item["net_accuracy_change"] > 0)),
    "repositories_unchanged": int(sum(1 for item in repository_diagnostics.values() if item["net_accuracy_change"] == 0)),
    "repositories_degraded": int(sum(1 for item in repository_diagnostics.values() if item["net_accuracy_change"] < 0)),
    "setup_repositories_improved": int(sum(1 for item in repository_diagnostics.values() if item["developer_setup_support"] > 0 and item["net_setup_change"] > 0)),
    "setup_repositories_unchanged": int(sum(1 for item in repository_diagnostics.values() if item["developer_setup_support"] > 0 and item["net_setup_change"] == 0)),
    "setup_repositories_worsened": int(sum(1 for item in repository_diagnostics.values() if item["developer_setup_support"] > 0 and item["net_setup_change"] < 0)),
}

def class_f1_metric(label):
    def fn(gold, pred):
        return precision_recall_fscore_support(gold, pred, labels=LABELS, zero_division=0)[2][LABELS.index(label)]
    return fn

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
}

setup_improved_repos = [repo for repo, item in repository_diagnostics.items() if item["net_setup_change"] > 0]
largest_setup_gain = max([item["net_setup_change"] for item in repository_diagnostics.values()] or [0])
setup_gain_total = sum(max(0, item["net_setup_change"]) for item in repository_diagnostics.values())
gates = {
    "macro_f1_delta_ge_0_02": comparison["delta"]["macro_f1"] >= 0.02,
    "balanced_accuracy_not_worse": hierarchy_metrics["balanced_accuracy"] >= baseline_metrics["balanced_accuracy"],
    "developer_setup_f1_ge_0_25": hierarchy_metrics["per_class"]["developer_setup"]["f1"] >= 0.25,
    "developer_setup_f1_delta_ge_0_15": comparison["delta"]["developer_setup_f1"] >= 0.15,
    "developer_setup_recall_ge_0_25": hierarchy_metrics["per_class"]["developer_setup"]["recall"] >= 0.25,
    "api_configuration_model_contract_f1_safety": all(comparison["delta"][key] >= -0.05 for key in ["api_reference_f1", "configuration_f1", "model_contract_f1"]),
    "setup_improves_across_at_least_3_repositories": len(setup_improved_repos) >= 3,
    "setup_gain_not_only_one_repository": setup_gain_total > 0 and largest_setup_gain < setup_gain_total,
    "bootstrap_macro_delta_probability_ge_0_90": repository_cluster_bootstrap["macro_f1"]["probability_delta_gt_zero"] >= 0.90,
    "no_leakage_or_partition_integrity_issue": True,
}
if all(gates.values()):
    decision_label = "GO"
elif comparison["delta"]["developer_setup_f1"] > 0:
    decision_label = "PARTIAL_NO_GO"
else:
    decision_label = "NO_BENEFIT"
decision = {"decision": decision_label, "gates": gates, "setup_improved_repositories": setup_improved_repos}

with open(OUTPUT_DIR / "paired_oof_predictions.jsonl", "w", encoding="utf-8", newline="\n") as out:
    for row, base, hier, route, score, probs in zip(rows, baseline_predictions, hierarchy_predictions, routed, specialist_scores, general_probabilities):
        out.write(json.dumps({
            "case_id": row["case_id"],
            "repository": row["repository"],
            "language": row["language"],
            "gold": row["gold_doc_category"],
            "general_baseline_prediction": str(base),
            "general_probabilities": {label: float(probs[LABELS.index(label)]) for label in LABELS},
            "routed": bool(route),
            "specialist_score": None if np.isnan(score) else float(score),
            "hierarchy_prediction": str(hier),
        }, ensure_ascii=False, sort_keys=True) + "\n")

write_json(OUTPUT_DIR / "baseline_oof_metrics.json", baseline_metrics)
write_json(OUTPUT_DIR / "hierarchy_oof_metrics.json", hierarchy_metrics)
write_json(OUTPUT_DIR / "hierarchy_comparison.json", comparison)
write_json(OUTPUT_DIR / "routing_diagnostics.json", routing_diagnostics)
write_json(OUTPUT_DIR / "developer_setup_rescue_analysis.json", developer_setup_rescue_analysis)
write_json(OUTPUT_DIR / "damage_analysis.json", damage_analysis)
write_json(OUTPUT_DIR / "selection_stability.json", selection_stability)
write_json(OUTPUT_DIR / "repository_diagnostics.json", {"summary": repo_summary, "repositories": repository_diagnostics})
write_json(OUTPUT_DIR / "repository_cluster_bootstrap.json", repository_cluster_bootstrap)
write_json(OUTPUT_DIR / "decision.json", decision)
'''
    figures_report = r'''
def plot_confusion(matrix, path, title, normalized=False):
    matrix = np.asarray(matrix)
    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(matrix, cmap="Blues", vmin=0 if normalized else None, vmax=1 if normalized else None)
    ax.set_xticks(range(len(LABELS)), LABELS, rotation=25, ha="right")
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

plot_confusion(baseline_metrics["confusion_matrix"], FIGURES_DIR / "baseline_confusion_matrix.png", "General baseline confusion matrix")
plot_confusion(hierarchy_metrics["confusion_matrix"], FIGURES_DIR / "hierarchy_confusion_matrix.png", "Hierarchy confusion matrix")
plot_confusion(hierarchy_metrics["normalized_confusion_matrix"], FIGURES_DIR / "hierarchy_normalized_confusion_matrix.png", "Hierarchy normalized confusion matrix", normalized=True)
simple_bar(FIGURES_DIR / "baseline_vs_hierarchy_macro_f1.png", ["baseline", "hierarchy"], [baseline_metrics["macro_f1"], hierarchy_metrics["macro_f1"]], "Macro-F1", "Macro-F1")
simple_bar(FIGURES_DIR / "baseline_vs_hierarchy_balanced_accuracy.png", ["baseline", "hierarchy"], [baseline_metrics["balanced_accuracy"], hierarchy_metrics["balanced_accuracy"]], "Balanced accuracy", "Balanced accuracy")
simple_bar(FIGURES_DIR / "baseline_vs_hierarchy_per_class_f1.png", LABELS, [comparison["delta"][f"{label}_f1"] for label in LABELS], "Per-class F1 delta", "Hierarchy - baseline")
simple_bar(FIGURES_DIR / "baseline_vs_hierarchy_setup_f1.png", ["baseline", "hierarchy"], [baseline_metrics["per_class"]["developer_setup"]["f1"], hierarchy_metrics["per_class"]["developer_setup"]["f1"]], "developer_setup F1", "F1")
simple_bar(FIGURES_DIR / "baseline_vs_hierarchy_setup_recall.png", ["baseline", "hierarchy"], [baseline_metrics["per_class"]["developer_setup"]["recall"], hierarchy_metrics["per_class"]["developer_setup"]["recall"]], "developer_setup recall", "Recall")
simple_bar(FIGURES_DIR / "outer_fold_macro_f1_delta.png", [str(item["fold"]) for item in outer_fold_metrics], [item["deltas"]["macro_f1"] for item in outer_fold_metrics], "Outer fold Macro-F1 delta", "Hierarchy - baseline")
simple_bar(FIGURES_DIR / "outer_fold_setup_f1_delta.png", [str(item["fold"]) for item in outer_fold_metrics], [item["deltas"]["developer_setup_f1"] for item in outer_fold_metrics], "Outer fold setup F1 delta", "Hierarchy - baseline")
simple_bar(FIGURES_DIR / "routing_breakdown.png", list(routing_diagnostics["routed_gold_distribution"].keys()), list(routing_diagnostics["routed_gold_distribution"].values()), "Routed rows by gold class", "Rows")

table_rows = [
    ("Macro-F1", baseline_metrics["macro_f1"], hierarchy_metrics["macro_f1"], comparison["delta"]["macro_f1"]),
    ("Balanced accuracy", baseline_metrics["balanced_accuracy"], hierarchy_metrics["balanced_accuracy"], comparison["delta"]["balanced_accuracy"]),
    ("API F1", baseline_metrics["per_class"]["api_reference"]["f1"], hierarchy_metrics["per_class"]["api_reference"]["f1"], comparison["delta"]["api_reference_f1"]),
    ("Configuration F1", baseline_metrics["per_class"]["configuration"]["f1"], hierarchy_metrics["per_class"]["configuration"]["f1"], comparison["delta"]["configuration_f1"]),
    ("Developer setup F1", baseline_metrics["per_class"]["developer_setup"]["f1"], hierarchy_metrics["per_class"]["developer_setup"]["f1"], comparison["delta"]["developer_setup_f1"]),
    ("Model contract F1", baseline_metrics["per_class"]["model_contract"]["f1"], hierarchy_metrics["per_class"]["model_contract"]["f1"], comparison["delta"]["model_contract_f1"]),
    ("Developer setup precision", baseline_metrics["per_class"]["developer_setup"]["precision"], hierarchy_metrics["per_class"]["developer_setup"]["precision"], comparison["delta"]["developer_setup_precision"]),
    ("Developer setup recall", baseline_metrics["per_class"]["developer_setup"]["recall"], hierarchy_metrics["per_class"]["developer_setup"]["recall"], comparison["delta"]["developer_setup_recall"]),
]
results_md = "# Stage-2 hierarchical integration pilot V1\n\n"
results_md += "This is **not external validation**. It is a paired repository-grouped OOF pilot over the frozen 1038-row natural train universe.\n\n"
results_md += f"Decision: **{decision['decision']}**\n\n"
results_md += "| Metric | General MiniLM | Hierarchy | Delta |\n| --- | ---: | ---: | ---: |\n"
for name, base, hier, delta in table_rows:
    results_md += f"| {name} | {base:.4f} | {hier:.4f} | {delta:+.4f} |\n"
results_md += "\n## Routing rule\n\nRoute iff the general prediction is `configuration` or `developer_setup`; otherwise keep the general prediction unchanged.\n\n"
results_md += "## GO / NO-GO gates\n\n```json\n" + json.dumps(gates, indent=2, sort_keys=True) + "\n```\n"
(OUTPUT_DIR / "RESULTS.md").write_text(results_md, encoding="utf-8")

experiment_manifest = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "data_path": str(DATA_PATH),
    "data_sha256": sha256_file(DATA_PATH),
    "row_count": len(rows),
    "category_counts": dict(Counter(y_all)),
    "minilm_model": MINILM_MODEL_NAME,
    "minilm_revision": MINILM_MODEL_REVISION,
    "outer_cv": {"splitter": "StratifiedGroupKFold", "n_splits": outer_n_splits, "shuffle": True, "random_state": SEED},
    "specialist_inner_cv": {"splitter": "StratifiedGroupKFold", "preferred_n_splits": 4, "fallback": 3, "random_state": "42 + outer_fold_id"},
    "routing_rule": "route iff general prediction in {configuration, developer_setup}",
    "confirmation_accessed": False,
    "frozen_322_validation_accessed": False,
}
write_json(OUTPUT_DIR / "experiment_manifest.json", experiment_manifest)

zip_path = Path("/content/stage2_hierarchy_integration_pilot_v1_results.zip")
if zip_path.exists():
    zip_path.unlink()
lightweight_files = [
    "RESULTS.md",
    "experiment_manifest.json",
    "outer_fold_manifest.json",
    "outer_fold_metrics.json",
    "baseline_oof_metrics.json",
    "hierarchy_oof_metrics.json",
    "paired_oof_predictions.jsonl",
    "hierarchy_comparison.json",
    "routing_diagnostics.json",
    "developer_setup_rescue_analysis.json",
    "damage_analysis.json",
    "specialist_selection_by_fold.json",
    "selection_stability.json",
    "repository_diagnostics.json",
    "repository_cluster_bootstrap.json",
    "hierarchy_rescued_errors.jsonl",
    "hierarchy_new_errors.jsonl",
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
files.download("/content/stage2_hierarchy_integration_pilot_v1_results.zip")
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
            nb_cell("code", feature_split),
            nb_cell("code", experiment),
            nb_cell("code", diagnostics),
            nb_cell("code", figures_report),
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
        f"""# Stage-2 hierarchical integration pilot V1

This pilot integrates the frozen four-class MiniLM hybrid model with the nested
cost-sensitive configuration/developer_setup Specialist V2. It is a paired
repository-grouped OOF train-side pilot only.

Data:

- `data/final_v2/architecture_challenge_v1/natural_train_primary_four.jsonl`
- rows: {EXPECTED_TOTAL}
- counts: {EXPECTED_COUNTS}
- SHA256: `{EXPECTED_TRAIN_SHA256}`

Frozen representation:

- encoder: `{MINILM_MODEL_NAME}`
- revision: `{MINILM_MODEL_REVISION}`
- semantic chunking: 1000 chars, max 2 chunks per side
- code TF-IDF: char_wb 3–5 grams, min_df=2, max_features=20000
- classifier family: LogisticRegression only

Routing rule:

Route iff the general four-class prediction is `configuration` or
`developer_setup`. API and model-contract general predictions remain unchanged.

Specialist decision grid:

- class weights: {CLASS_WEIGHT_GRID}
- thresholds: {THRESHOLD_GRID}
- precision floor: {PRECISION_FLOOR}

Notebook: `notebooks/category_stage2_hierarchical_integration_pilot_v1.ipynb`

The frozen 322-row development validation is not required and must not be
loaded by this pilot.
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
                "local_hierarchy_oof_executed": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
