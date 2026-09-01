"""Prepare the final Stage-2 frozen development-validation evaluation notebook.

This local script creates a self-contained Colab notebook and methodology
README. It verifies hashes/counts only; it does not run the final 322-row
development-validation evaluation locally.
"""
from __future__ import annotations

import ast
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "final_v2" / "architecture_challenge_v1"
TRAIN_JSONL = DATA_DIR / "natural_train_primary_four.jsonl"
VALIDATION_JSONL = DATA_DIR / "natural_validation_primary_four.jsonl"
EXPORT_MANIFEST = DATA_DIR / "export_manifest.json"
NOTEBOOK_PATH = ROOT / "notebooks" / "category_stage2_final_development_evaluation_v1.ipynb"
README_PATH = ROOT / "experiments" / "category_stage2_final_development_evaluation_v1" / "README.md"

LABELS = ["api_reference", "configuration", "developer_setup", "model_contract"]
COARSE_LABELS = ["api_reference", "config_setup_family", "model_contract"]
SPECIALIST_LABELS = ["configuration", "developer_setup"]
COARSE_MAPPING = {
    "api_reference": "api_reference",
    "configuration": "config_setup_family",
    "developer_setup": "config_setup_family",
    "model_contract": "model_contract",
}
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

EXPECTED_TRAIN_TOTAL = 1038
EXPECTED_TRAIN_COUNTS = {
    "api_reference": 412,
    "configuration": 277,
    "developer_setup": 88,
    "model_contract": 261,
}
EXPECTED_TRAIN_SHA256 = "9dc1136f1cf695eb69c70b763ad051898aa5fae351fcf028eed97116c8891f99"
EXPECTED_VALIDATION_TOTAL = 322
EXPECTED_VALIDATION_COUNTS = {
    "api_reference": 85,
    "configuration": 154,
    "developer_setup": 19,
    "model_contract": 64,
}
EXPECTED_VALIDATION_CASE_IDS_SHA256 = "aac3384de6d482abefb4201091bf828d6d8c1c91c1ddbdad40a4ec7273051e3e"

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
HISTORICAL_BASELINE_MACRO_F1 = 0.45628987455472775
BASELINE_REPRODUCTION_TOLERANCE = 0.005


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def stable_json_hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def verify_artifacts() -> None:
    train_rows = read_jsonl(TRAIN_JSONL)
    validation_rows = read_jsonl(VALIDATION_JSONL)
    manifest = json.loads(EXPORT_MANIFEST.read_text(encoding="utf-8"))

    if len(train_rows) != EXPECTED_TRAIN_TOTAL:
        raise AssertionError("Unexpected train row count")
    if Counter(row["gold_doc_category"] for row in train_rows) != EXPECTED_TRAIN_COUNTS:
        raise AssertionError("Unexpected train class counts")
    if sha256_file(TRAIN_JSONL) != EXPECTED_TRAIN_SHA256:
        raise AssertionError("Unexpected train SHA256")
    if len(validation_rows) != EXPECTED_VALIDATION_TOTAL:
        raise AssertionError("Unexpected development-validation row count")
    if Counter(row["gold_doc_category"] for row in validation_rows) != EXPECTED_VALIDATION_COUNTS:
        raise AssertionError("Unexpected development-validation class counts")
    if stable_json_hash([row["case_id"] for row in validation_rows]) != EXPECTED_VALIDATION_CASE_IDS_SHA256:
        raise AssertionError("Unexpected development-validation case-ID hash")
    if {row["repository"] for row in train_rows} & {row["repository"] for row in validation_rows}:
        raise AssertionError("Train/development-validation repository overlap")
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
# Final Stage-2 development evaluation V1

Full 1038-row train fit plus one frozen 322-row development-validation
comparison between:

1. the original four-class MiniLM hybrid baseline; and
2. the approved coarse-to-fine hierarchy with Specialist V2.

This is **development validation**, not final external testing.
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
EXPECTED_TRAIN_TOTAL = {EXPECTED_TRAIN_TOTAL}
EXPECTED_TRAIN_COUNTS = {py(EXPECTED_TRAIN_COUNTS)}
EXPECTED_TRAIN_SHA256 = "{EXPECTED_TRAIN_SHA256}"
EXPECTED_VALIDATION_TOTAL = {EXPECTED_VALIDATION_TOTAL}
EXPECTED_VALIDATION_COUNTS = {py(EXPECTED_VALIDATION_COUNTS)}
EXPECTED_VALIDATION_CASE_IDS_SHA256 = "{EXPECTED_VALIDATION_CASE_IDS_SHA256}"
SEED = 42

MINILM_MODEL_NAME = "{MINILM_MODEL_NAME}"
MINILM_MODEL_REVISION = "{MINILM_MODEL_REVISION}"
CHUNK_CHARS = 1000
MAX_CHUNKS = 2
EMBEDDING_BATCH_SIZE = 64

CLASS_WEIGHT_GRID = {py(CLASS_WEIGHT_GRID)}
THRESHOLD_GRID = {py(THRESHOLD_GRID)}
PRECISION_FLOOR = {PRECISION_FLOOR}
HISTORICAL_BASELINE = {{
    "macro_f1": 0.45628987455472775,
    "balanced_accuracy": 0.478023538961039,
    "per_class_f1": {{
        "api_reference": 0.5340314136125655,
        "configuration": 0.6824324324324325,
        "developer_setup": 0.0,
        "model_contract": 0.6086956521739131,
    }},
}}
BASELINE_REPRODUCTION_TOLERANCE = {BASELINE_REPRODUCTION_TOLERANCE}

OUTPUT_DIR = Path("/content/experiments/category_stage2_final_development_evaluation_v1")
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
def reject_forbidden_path(path):
    lowered = str(path).replace("\\", "/").lower()
    if any(word in lowered for word in ["confirmation", "refresh", "controlled", "synthetic", "no_update", "other_documentation"]):
        raise ValueError(f"Forbidden artifact path: {path}")


def has_required_files(root):
    data_dir = Path(root) / "data" / "final_v2" / "architecture_challenge_v1"
    return (
        (data_dir / "natural_train_primary_four.jsonl").exists()
        and (data_dir / "natural_validation_primary_four.jsonl").exists()
        and (data_dir / "export_manifest.json").exists()
    )


def locate_root():
    candidates = [
        Path.cwd(),
        Path("/content/MASTER-RAD-PROJEKAT"),
        Path("/content/MASTER RAD PROJEKAT"),
        Path("/content/drive/MyDrive/MASTER-RAD-PROJEKAT"),
        Path("/content/drive/MyDrive/MASTER RAD PROJEKAT"),
    ]
    for candidate in candidates:
        if has_required_files(candidate):
            return candidate
    for manifest in Path("/content").glob("**/export_manifest.json"):
        reject_forbidden_path(manifest)
        if "architecture_challenge_v1" not in manifest.as_posix():
            continue
        possible = manifest.parent.parent.parent.parent
        if has_required_files(possible):
            return possible
    return None


ROOT = locate_root()
if ROOT is None:
    print("Upload repository ZIP or exactly these files: natural_train_primary_four.jsonl, natural_validation_primary_four.jsonl, export_manifest.json")
    from google.colab import files

    uploaded = files.upload()
    upload_root = Path("/content/MASTER-RAD-PROJEKAT")
    data_dir = upload_root / "data" / "final_v2" / "architecture_challenge_v1"
    data_dir.mkdir(parents=True, exist_ok=True)
    for name, payload in uploaded.items():
        reject_forbidden_path(name)
        base = Path(name).name
        if base.lower().endswith(".zip"):
            zip_path = upload_root / base
            zip_path.write_bytes(payload)
            with zipfile.ZipFile(zip_path) as archive:
                for member in archive.namelist():
                    reject_forbidden_path(member)
                archive.extractall(upload_root)
        elif base in {"natural_train_primary_four.jsonl", "natural_validation_primary_four.jsonl", "export_manifest.json"}:
            (data_dir / base).write_bytes(payload)
    ROOT = locate_root()

assert ROOT is not None and has_required_files(ROOT)
DATA_DIR = ROOT / "data" / "final_v2" / "architecture_challenge_v1"
TRAIN_PATH = DATA_DIR / "natural_train_primary_four.jsonl"
VALIDATION_PATH = DATA_DIR / "natural_validation_primary_four.jsonl"
MANIFEST_PATH = DATA_DIR / "export_manifest.json"
print("Using Stage-2 data directory:", DATA_DIR)
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


def read_rows(path, *, expected_partition):
    reject_forbidden_path(path)
    rows = []
    with open(path, encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("partition") != expected_partition:
                raise ValueError(f"{path}:{line_number}: expected partition {expected_partition}")
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


def encode_texts_cached(side, rows_for_encoding, encoder):
    texts = [build_code_text(row) if side.startswith("code") else build_docs_text(row) for row in rows_for_encoding]
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


def lexical_relational_scalars(rows_for_features):
    values = []
    for row in rows_for_features:
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


def labels_for(rows_for_labels):
    return np.asarray([row["gold_doc_category"] for row in rows_for_labels])


def coarse_labels_for(rows_for_labels):
    return np.asarray([coarse_label(row["gold_doc_category"]) for row in rows_for_labels])


def fit_feature_components(train_rows_for_fit, code_embeddings, docs_embeddings):
    vectorizer = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(3, 5),
        min_df=2,
        max_features=20000,
        sublinear_tf=True,
        dtype=np.float32,
    )
    code_tfidf = vectorizer.fit_transform([build_code_text(row) for row in train_rows_for_fit])
    semantic = relational_semantic_features(code_embeddings, docs_embeddings)
    scalars = lexical_relational_scalars(train_rows_for_fit)
    features = sparse.hstack([code_tfidf, sparse.csr_matrix(semantic), sparse.csr_matrix(scalars)], format="csr")
    return vectorizer, features


def transform_feature_components(vectorizer, rows_for_transform, code_embeddings, docs_embeddings):
    code_tfidf = vectorizer.transform([build_code_text(row) for row in rows_for_transform])
    semantic = relational_semantic_features(code_embeddings, docs_embeddings)
    scalars = lexical_relational_scalars(rows_for_transform)
    return sparse.hstack([code_tfidf, sparse.csr_matrix(semantic), sparse.csr_matrix(scalars)], format="csr")


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


def classifier_probabilities(classifier, features, labels):
    raw = classifier.predict_proba(features)
    output = np.zeros((features.shape[0], len(labels)), dtype=float)
    for source_index, label in enumerate(classifier.classes_):
        output[:, labels.index(str(label))] = raw[:, source_index]
    return output


def setup_probability(classifier, features):
    raw = classifier.predict_proba(features)
    if "developer_setup" not in classifier.classes_:
        return np.zeros(features.shape[0], dtype=float)
    return raw[:, list(classifier.classes_).index("developer_setup")]


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
'''
    train_freeze = r'''
# =========================
# PHASE A: TRAIN FREEZE
# =========================
train_rows = read_rows(TRAIN_PATH, expected_partition="development_train")
manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
assert len(train_rows) == EXPECTED_TRAIN_TOTAL
assert Counter(row["gold_doc_category"] for row in train_rows) == EXPECTED_TRAIN_COUNTS
assert sha256_file(TRAIN_PATH) == EXPECTED_TRAIN_SHA256
assert manifest["artifacts"]["natural_train_primary_four.jsonl"]["sha256"] == EXPECTED_TRAIN_SHA256
assert all(set(row) == set(SAFE_FIELDS) for row in train_rows)
for row in train_rows:
    combined = (build_code_text(row) + "\n" + build_docs_text(row)).lower()
    repo = str(row.get("repository") or "").lower()
    assert not repo or "/" not in repo or repo not in combined

resolved_minilm_sha = HfApi().model_info(MINILM_MODEL_NAME, revision=MINILM_MODEL_REVISION).sha
assert resolved_minilm_sha == MINILM_MODEL_REVISION
encoder = SentenceTransformer(MINILM_MODEL_NAME, revision=MINILM_MODEL_REVISION, device="cuda")
encoder.eval()
for parameter in encoder.parameters():
    parameter.requires_grad_(False)
assert all(not parameter.requires_grad for parameter in encoder.parameters())

train_code_embeddings, train_code_cache = encode_texts_cached("code_train", train_rows, encoder)
train_docs_embeddings, train_docs_cache = encode_texts_cached("docs_train", train_rows, encoder)

train_y = labels_for(train_rows)
train_coarse_y = coarse_labels_for(train_rows)
baseline_vectorizer, baseline_train_x = fit_feature_components(train_rows, train_code_embeddings, train_docs_embeddings)
baseline_clf = LogisticRegression(C=1.0, solver="lbfgs", max_iter=2000, random_state=SEED)
baseline_clf.fit(baseline_train_x, train_y)

coarse_vectorizer, coarse_train_x = fit_feature_components(train_rows, train_code_embeddings, train_docs_embeddings)
coarse_clf = LogisticRegression(C=1.0, solver="lbfgs", max_iter=2000, random_state=SEED)
coarse_clf.fit(coarse_train_x, train_coarse_y)

specialist_train_indices = np.asarray([i for i, row in enumerate(train_rows) if row["gold_doc_category"] in SPECIALIST_LABELS], dtype=int)
specialist_rows = [train_rows[int(i)] for i in specialist_train_indices]
assert Counter(row["gold_doc_category"] for row in specialist_rows) == {"configuration": 277, "developer_setup": 88}


def specialist_grouped_splits(indices):
    for n_splits in [5, 4, 3]:
        idx = np.asarray(indices, dtype=int)
        y = labels_for([train_rows[int(i)] for i in idx])
        groups = np.asarray([train_rows[int(i)]["repository"] for i in idx])
        splitter = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=SEED)
        folds = []
        valid = True
        for train_local, eval_local in splitter.split(np.arange(len(idx)), y, groups):
            train_idx = idx[train_local]
            eval_idx = idx[eval_local]
            y_train = labels_for([train_rows[int(i)] for i in train_idx])
            y_eval = labels_for([train_rows[int(i)] for i in eval_idx])
            g_train = {train_rows[int(i)]["repository"] for i in train_idx}
            g_eval = {train_rows[int(i)]["repository"] for i in eval_idx}
            if g_train & g_eval or set(y_train) != set(SPECIALIST_LABELS) or set(y_eval) != set(SPECIALIST_LABELS):
                valid = False
                break
            folds.append((train_idx, eval_idx))
        if valid:
            return n_splits, folds
    raise RuntimeError("No structurally valid specialist OOF split.")


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


specialist_n_splits, specialist_folds = specialist_grouped_splits(specialist_train_indices)
specialist_position = {int(global_index): pos for pos, global_index in enumerate(specialist_train_indices)}
candidate_probs = defaultdict(lambda: np.zeros(len(specialist_train_indices), dtype=float))
specialist_fit_audit = []
for fold_id, (inner_train_idx, inner_eval_idx) in enumerate(specialist_folds, 1):
    inner_train_rows = [train_rows[int(i)] for i in inner_train_idx]
    inner_eval_rows = [train_rows[int(i)] for i in inner_eval_idx]
    inner_vectorizer, x_inner_train = fit_feature_components(inner_train_rows, train_code_embeddings[inner_train_idx], train_docs_embeddings[inner_train_idx])
    x_inner_eval = transform_feature_components(inner_vectorizer, inner_eval_rows, train_code_embeddings[inner_eval_idx], train_docs_embeddings[inner_eval_idx])
    y_inner_train = labels_for(inner_train_rows)
    for weight_spec in CLASS_WEIGHT_GRID:
        clf = LogisticRegression(C=1.0, solver="lbfgs", max_iter=2000, random_state=SEED, class_weight=weight_spec["value"])
        clf.fit(x_inner_train, y_inner_train)
        prob_setup = setup_probability(clf, x_inner_eval)
        for global_index, prob in zip(inner_eval_idx, prob_setup):
            candidate_probs[weight_spec["name"]][specialist_position[int(global_index)]] = float(prob)
        specialist_fit_audit.append({"fold": fold_id, "class_weight": weight_spec["name"], "train_rows": len(inner_train_rows), "eval_rows": len(inner_eval_rows)})

specialist_y = labels_for(specialist_rows)
specialist_grid_scores = []
for weight_spec in CLASS_WEIGHT_GRID:
    for threshold in THRESHOLD_GRID:
        pred = predict_from_threshold(candidate_probs[weight_spec["name"]], threshold)
        metrics = metric_bundle(specialist_y, pred, SPECIALIST_LABELS)
        specialist_grid_scores.append({
            "class_weight": weight_spec["name"],
            "class_weight_value": weight_spec["value"],
            "class_weight_rank": int(weight_spec["rank"]),
            "threshold": float(threshold),
            "precision_floor_satisfied": bool(metrics["per_class"]["developer_setup"]["precision"] >= PRECISION_FLOOR),
            "metrics": metrics,
        })
eligible = [item for item in specialist_grid_scores if item["precision_floor_satisfied"]]
final_specialist_selection = max(eligible if eligible else specialist_grid_scores, key=candidate_sort_key)
final_specialist_oof_metrics = final_specialist_selection["metrics"]

specialist_vectorizer, specialist_train_x = fit_feature_components(specialist_rows, train_code_embeddings[specialist_train_indices], train_docs_embeddings[specialist_train_indices])
specialist_clf = LogisticRegression(C=1.0, solver="lbfgs", max_iter=2000, random_state=SEED, class_weight=final_specialist_selection["class_weight_value"])
specialist_clf.fit(specialist_train_x, specialist_y)

stage2_train_freeze_manifest = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "train_sha256": sha256_file(TRAIN_PATH),
    "train_rows": len(train_rows),
    "train_counts": dict(Counter(train_y)),
    "minilm_model": MINILM_MODEL_NAME,
    "minilm_revision": MINILM_MODEL_REVISION,
    "resolved_minilm_revision": resolved_minilm_sha,
    "baseline_config": {"classifier": "LogisticRegression", "C": 1.0, "solver": "lbfgs", "max_iter": 2000, "random_state": SEED, "class_weight": None},
    "coarse_mapping": COARSE_MAPPING,
    "coarse_classifier_config": {"classifier": "LogisticRegression", "C": 1.0, "solver": "lbfgs", "max_iter": 2000, "random_state": SEED, "class_weight": None},
    "specialist_selected_class_weight": final_specialist_selection["class_weight"],
    "specialist_selected_class_weight_value": final_specialist_selection["class_weight_value"],
    "specialist_selected_threshold": final_specialist_selection["threshold"],
    "specialist_selection_oof_metrics": final_specialist_oof_metrics,
    "specialist_grid_scores": specialist_grid_scores,
    "specialist_oof_splitter": {"splitter": "StratifiedGroupKFold", "n_splits": specialist_n_splits, "shuffle": True, "random_state": SEED},
    "validation_metrics_computed_before_freeze": False,
}
write_json(OUTPUT_DIR / "stage2_train_freeze_manifest.json", stage2_train_freeze_manifest)
write_json(OUTPUT_DIR / "final_specialist_selection.json", final_specialist_selection)
write_json(OUTPUT_DIR / "final_specialist_oof_metrics.json", final_specialist_oof_metrics)
print("STAGE2_TRAIN_FREEZE_COMPLETE")
'''
    validation_eval = r'''
# =========================
# PHASE B: ONE FROZEN DEVELOPMENT-VALIDATION SCORING
# =========================
validation_rows = read_rows(VALIDATION_PATH, expected_partition="development_validation")
assert len(validation_rows) == EXPECTED_VALIDATION_TOTAL
assert Counter(row["gold_doc_category"] for row in validation_rows) == EXPECTED_VALIDATION_COUNTS
assert stable_json_hash([row["case_id"] for row in validation_rows]) == EXPECTED_VALIDATION_CASE_IDS_SHA256
assert not ({row["repository"] for row in train_rows} & {row["repository"] for row in validation_rows})

validation_code_embeddings, validation_code_cache = encode_texts_cached("code_development_validation", validation_rows, encoder)
validation_docs_embeddings, validation_docs_cache = encode_texts_cached("docs_development_validation", validation_rows, encoder)
validation_y = labels_for(validation_rows)
validation_coarse_y = coarse_labels_for(validation_rows)

baseline_validation_x = transform_feature_components(baseline_vectorizer, validation_rows, validation_code_embeddings, validation_docs_embeddings)
baseline_validation_predictions = baseline_clf.predict(baseline_validation_x)
baseline_validation_probabilities = classifier_probabilities(baseline_clf, baseline_validation_x, LABELS)

coarse_validation_x = transform_feature_components(coarse_vectorizer, validation_rows, validation_code_embeddings, validation_docs_embeddings)
coarse_validation_predictions = coarse_clf.predict(coarse_validation_x)
coarse_validation_probabilities = classifier_probabilities(coarse_clf, coarse_validation_x, COARSE_LABELS)

specialist_validation_x = transform_feature_components(specialist_vectorizer, validation_rows, validation_code_embeddings, validation_docs_embeddings)
specialist_validation_scores = setup_probability(specialist_clf, specialist_validation_x)
specialist_validation_predictions = predict_from_threshold(specialist_validation_scores, final_specialist_selection["threshold"])

hierarchy_validation_predictions = []
for coarse_pred, specialist_pred in zip(coarse_validation_predictions, specialist_validation_predictions):
    if coarse_pred == "api_reference":
        hierarchy_validation_predictions.append("api_reference")
    elif coarse_pred == "model_contract":
        hierarchy_validation_predictions.append("model_contract")
    elif coarse_pred == "config_setup_family":
        hierarchy_validation_predictions.append(str(specialist_pred))
    else:
        raise AssertionError("Unexpected coarse prediction")
hierarchy_validation_predictions = np.asarray(hierarchy_validation_predictions, dtype=object)

baseline_validation_metrics = metric_bundle(validation_y, baseline_validation_predictions, LABELS)
hierarchy_validation_metrics = metric_bundle(validation_y, hierarchy_validation_predictions, LABELS)
coarse_validation_metrics = metric_bundle(validation_coarse_y, coarse_validation_predictions, COARSE_LABELS)
baseline_macro_delta = abs(baseline_validation_metrics["macro_f1"] - HISTORICAL_BASELINE["macro_f1"])
baseline_reproduction_warning = bool(baseline_macro_delta > BASELINE_REPRODUCTION_TOLERANCE)
baseline_audit = {
    "baseline_reproduction_warning": baseline_reproduction_warning,
    "tolerance": BASELINE_REPRODUCTION_TOLERANCE,
    "historical_result": HISTORICAL_BASELINE,
    "new_result": baseline_validation_metrics,
    "macro_f1_absolute_delta": float(baseline_macro_delta),
    "possible_causes_if_warning": [
        "implementation mismatch",
        "dependency/library numeric change",
        "data/hash mismatch",
        "feature construction mismatch",
    ] if baseline_reproduction_warning else [],
}
baseline_audit_md = "# Baseline reproduction audit\n\n"
baseline_audit_md += f"baseline_reproduction_warning: **{baseline_reproduction_warning}**\n\n"
baseline_audit_md += f"Historical Macro-F1: `{HISTORICAL_BASELINE['macro_f1']}`\n\n"
baseline_audit_md += f"New Macro-F1: `{baseline_validation_metrics['macro_f1']}`\n\n"
baseline_audit_md += f"Absolute delta: `{baseline_macro_delta}`\n\n"
if baseline_reproduction_warning:
    baseline_audit_md += "Do not claim apples-to-apples equivalence until audited. No parameters were changed to force reproduction.\n"
else:
    baseline_audit_md += "Baseline reproduction is within tolerance.\n"
(OUTPUT_DIR / "BASELINE_REPRODUCTION_AUDIT.md").write_text(baseline_audit_md, encoding="utf-8")

comparison = {
    "baseline": baseline_validation_metrics,
    "hierarchy": hierarchy_validation_metrics,
    "delta": {
        "accuracy": hierarchy_validation_metrics["accuracy"] - baseline_validation_metrics["accuracy"],
        "macro_f1": hierarchy_validation_metrics["macro_f1"] - baseline_validation_metrics["macro_f1"],
        "balanced_accuracy": hierarchy_validation_metrics["balanced_accuracy"] - baseline_validation_metrics["balanced_accuracy"],
        "api_reference_f1": hierarchy_validation_metrics["per_class"]["api_reference"]["f1"] - baseline_validation_metrics["per_class"]["api_reference"]["f1"],
        "configuration_f1": hierarchy_validation_metrics["per_class"]["configuration"]["f1"] - baseline_validation_metrics["per_class"]["configuration"]["f1"],
        "developer_setup_precision": hierarchy_validation_metrics["per_class"]["developer_setup"]["precision"] - baseline_validation_metrics["per_class"]["developer_setup"]["precision"],
        "developer_setup_recall": hierarchy_validation_metrics["per_class"]["developer_setup"]["recall"] - baseline_validation_metrics["per_class"]["developer_setup"]["recall"],
        "developer_setup_f1": hierarchy_validation_metrics["per_class"]["developer_setup"]["f1"] - baseline_validation_metrics["per_class"]["developer_setup"]["f1"],
        "model_contract_f1": hierarchy_validation_metrics["per_class"]["model_contract"]["f1"] - baseline_validation_metrics["per_class"]["model_contract"]["f1"],
    },
}

setup_mask = validation_y == "developer_setup"
configuration_mask = validation_y == "configuration"
validation_setup_family_routing_recall = float(np.mean(coarse_validation_predictions[setup_mask] == "config_setup_family"))
configuration_family_routing_recall = float(np.mean(coarse_validation_predictions[configuration_mask] == "config_setup_family"))
setup_validation_path_analysis = defaultdict(list)
for row, coarse_pred, specialist_pred, final_pred in zip(validation_rows, coarse_validation_predictions, specialist_validation_predictions, hierarchy_validation_predictions):
    if row["gold_doc_category"] != "developer_setup":
        continue
    item = {"case_id": row["case_id"], "repository": row["repository"], "coarse_prediction": str(coarse_pred), "specialist_prediction": str(specialist_pred), "final_prediction": str(final_pred)}
    if coarse_pred == "api_reference":
        setup_validation_path_analysis["level1_api_specialist_never_reached"].append(item)
    elif coarse_pred == "model_contract":
        setup_validation_path_analysis["level1_model_contract_specialist_never_reached"].append(item)
    elif coarse_pred == "config_setup_family" and specialist_pred == "configuration":
        setup_validation_path_analysis["level1_family_specialist_configuration"].append(item)
    elif coarse_pred == "config_setup_family" and specialist_pred == "developer_setup":
        setup_validation_path_analysis["level1_family_specialist_developer_setup"].append(item)
setup_validation_path_report = {key: {"count": len(value), "cases": value} for key, value in setup_validation_path_analysis.items()}

development_gates = {
    "hierarchy_macro_f1_gt_baseline_macro_f1": hierarchy_validation_metrics["macro_f1"] > baseline_validation_metrics["macro_f1"],
    "hierarchy_balanced_accuracy_ge_baseline_minus_0_01": hierarchy_validation_metrics["balanced_accuracy"] >= baseline_validation_metrics["balanced_accuracy"] - 0.01,
    "hierarchy_developer_setup_f1_gt_baseline": hierarchy_validation_metrics["per_class"]["developer_setup"]["f1"] > baseline_validation_metrics["per_class"]["developer_setup"]["f1"],
    "api_configuration_model_contract_no_f1_loss_gt_0_07": all(comparison["delta"][key] >= -0.07 for key in ["api_reference_f1", "configuration_f1", "model_contract_f1"]),
}
development_decision = {
    "decision": "HIERARCHY_SELECTED" if all(development_gates.values()) else "BASELINE_RETAINED",
    "gates": development_gates,
    "baseline_reproduction_warning": baseline_reproduction_warning,
}

with open(OUTPUT_DIR / "paired_validation_predictions.jsonl", "w", encoding="utf-8", newline="\n") as out:
    for row, base_pred, coarse_pred, spec_pred, final_pred, spec_score, base_probs, coarse_probs in zip(validation_rows, baseline_validation_predictions, coarse_validation_predictions, specialist_validation_predictions, hierarchy_validation_predictions, specialist_validation_scores, baseline_validation_probabilities, coarse_validation_probabilities):
        out.write(json.dumps({
            "case_id": row["case_id"],
            "repository": row["repository"],
            "language": row["language"],
            "gold": row["gold_doc_category"],
            "baseline_prediction": str(base_pred),
            "baseline_probabilities": {label: float(base_probs[LABELS.index(label)]) for label in LABELS},
            "coarse_prediction": str(coarse_pred),
            "coarse_probabilities": {label: float(coarse_probs[COARSE_LABELS.index(label)]) for label in COARSE_LABELS},
            "specialist_prediction_if_family": str(spec_pred) if coarse_pred == "config_setup_family" else None,
            "specialist_score_if_family": float(spec_score) if coarse_pred == "config_setup_family" else None,
            "hierarchy_prediction": str(final_pred),
        }, ensure_ascii=False, sort_keys=True) + "\n")

write_json(OUTPUT_DIR / "baseline_validation_metrics.json", baseline_validation_metrics)
write_json(OUTPUT_DIR / "hierarchy_validation_metrics.json", hierarchy_validation_metrics)
write_json(OUTPUT_DIR / "coarse_validation_metrics.json", coarse_validation_metrics)
write_json(OUTPUT_DIR / "hierarchy_validation_comparison.json", comparison)
write_json(OUTPUT_DIR / "setup_validation_path_analysis.json", setup_validation_path_report)
write_json(OUTPUT_DIR / "development_decision.json", development_decision)
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


plot_confusion(baseline_validation_metrics["confusion_matrix"], LABELS, FIGURES_DIR / "baseline_validation_confusion_matrix.png", "Baseline development-validation confusion matrix")
plot_confusion(hierarchy_validation_metrics["confusion_matrix"], LABELS, FIGURES_DIR / "hierarchy_validation_confusion_matrix.png", "Hierarchy development-validation confusion matrix")
plot_confusion(hierarchy_validation_metrics["normalized_confusion_matrix"], LABELS, FIGURES_DIR / "hierarchy_validation_normalized_confusion_matrix.png", "Hierarchy normalized development-validation confusion matrix", normalized=True)
simple_bar(FIGURES_DIR / "baseline_vs_hierarchy_macro_f1.png", ["baseline", "hierarchy"], [baseline_validation_metrics["macro_f1"], hierarchy_validation_metrics["macro_f1"]], "Development-validation Macro-F1", "Macro-F1")
simple_bar(FIGURES_DIR / "baseline_vs_hierarchy_balanced_accuracy.png", ["baseline", "hierarchy"], [baseline_validation_metrics["balanced_accuracy"], hierarchy_validation_metrics["balanced_accuracy"]], "Development-validation balanced accuracy", "Balanced accuracy")
simple_bar(FIGURES_DIR / "baseline_vs_hierarchy_per_class_f1.png", LABELS, [comparison["delta"][f"{label}_f1"] for label in LABELS], "Per-class F1 delta", "Hierarchy - baseline")
simple_bar(FIGURES_DIR / "baseline_vs_hierarchy_setup_f1.png", ["baseline", "hierarchy"], [baseline_validation_metrics["per_class"]["developer_setup"]["f1"], hierarchy_validation_metrics["per_class"]["developer_setup"]["f1"]], "developer_setup F1", "F1")
simple_bar(FIGURES_DIR / "baseline_vs_hierarchy_setup_recall.png", ["baseline", "hierarchy"], [baseline_validation_metrics["per_class"]["developer_setup"]["recall"], hierarchy_validation_metrics["per_class"]["developer_setup"]["recall"]], "developer_setup recall", "Recall")

table_rows = [
    ("Accuracy", baseline_validation_metrics["accuracy"], hierarchy_validation_metrics["accuracy"], comparison["delta"]["accuracy"]),
    ("Macro-F1", baseline_validation_metrics["macro_f1"], hierarchy_validation_metrics["macro_f1"], comparison["delta"]["macro_f1"]),
    ("Balanced accuracy", baseline_validation_metrics["balanced_accuracy"], hierarchy_validation_metrics["balanced_accuracy"], comparison["delta"]["balanced_accuracy"]),
    ("API F1", baseline_validation_metrics["per_class"]["api_reference"]["f1"], hierarchy_validation_metrics["per_class"]["api_reference"]["f1"], comparison["delta"]["api_reference_f1"]),
    ("Configuration F1", baseline_validation_metrics["per_class"]["configuration"]["f1"], hierarchy_validation_metrics["per_class"]["configuration"]["f1"], comparison["delta"]["configuration_f1"]),
    ("Developer setup precision", baseline_validation_metrics["per_class"]["developer_setup"]["precision"], hierarchy_validation_metrics["per_class"]["developer_setup"]["precision"], comparison["delta"]["developer_setup_precision"]),
    ("Developer setup recall", baseline_validation_metrics["per_class"]["developer_setup"]["recall"], hierarchy_validation_metrics["per_class"]["developer_setup"]["recall"], comparison["delta"]["developer_setup_recall"]),
    ("Developer setup F1", baseline_validation_metrics["per_class"]["developer_setup"]["f1"], hierarchy_validation_metrics["per_class"]["developer_setup"]["f1"], comparison["delta"]["developer_setup_f1"]),
    ("Model contract F1", baseline_validation_metrics["per_class"]["model_contract"]["f1"], hierarchy_validation_metrics["per_class"]["model_contract"]["f1"], comparison["delta"]["model_contract_f1"]),
]
results_md = "# Final Stage-2 development evaluation V1\n\n"
results_md += "**THIS IS DEVELOPMENT VALIDATION, NOT FINAL EXTERNAL TESTING.**\n\n"
results_md += f"Training universe: **{len(train_rows)} natural rows**\n\n"
results_md += f"Validation: **{len(validation_rows)} frozen development rows**\n\n"
results_md += "Repository overlap: **0**\n\n"
results_md += f"Selected final specialist class weight: `{final_specialist_selection['class_weight']}`\n\n"
results_md += f"Selected final specialist threshold: `{final_specialist_selection['threshold']}`\n\n"
results_md += f"Final development decision: **{development_decision['decision']}**\n\n"
results_md += "| Metric | Original MiniLM baseline | Coarse-to-fine hierarchy | Delta |\n| --- | ---: | ---: | ---: |\n"
for name, base, hier, delta in table_rows:
    results_md += f"| {name} | {base:.4f} | {hier:.4f} | {delta:+.4f} |\n"
results_md += f"\nvalidation_setup_family_routing_recall: **{validation_setup_family_routing_recall:.4f}**\n\n"
results_md += f"configuration_family_routing_recall: **{configuration_family_routing_recall:.4f}**\n\n"
results_md += "## Development decision gates\n\n```json\n" + json.dumps(development_gates, indent=2, sort_keys=True) + "\n```\n"
(OUTPUT_DIR / "RESULTS.md").write_text(results_md, encoding="utf-8")

experiment_manifest = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "status": "final_stage2_development_validation",
    "not_final_external_testing": True,
    "train_path": str(TRAIN_PATH),
    "train_sha256": sha256_file(TRAIN_PATH),
    "train_counts": dict(Counter(train_y)),
    "validation_path": str(VALIDATION_PATH),
    "validation_case_ids_sha256": stable_json_hash([row["case_id"] for row in validation_rows]),
    "validation_counts": dict(Counter(validation_y)),
    "repository_overlap": [],
    "minilm_model": MINILM_MODEL_NAME,
    "minilm_revision": MINILM_MODEL_REVISION,
    "coarse_mapping": COARSE_MAPPING,
    "specialist_selection": final_specialist_selection,
    "development_decision_rule": development_gates,
    "confirmation_accessed": False,
}
write_json(OUTPUT_DIR / "experiment_manifest.json", experiment_manifest)

zip_path = Path("/content/stage2_final_development_evaluation_v1_results.zip")
if zip_path.exists():
    zip_path.unlink()
lightweight_files = [
    "RESULTS.md",
    "stage2_train_freeze_manifest.json",
    "experiment_manifest.json",
    "final_specialist_selection.json",
    "final_specialist_oof_metrics.json",
    "baseline_validation_metrics.json",
    "hierarchy_validation_metrics.json",
    "coarse_validation_metrics.json",
    "paired_validation_predictions.jsonl",
    "hierarchy_validation_comparison.json",
    "setup_validation_path_analysis.json",
    "development_decision.json",
    "BASELINE_REPRODUCTION_AUDIT.md",
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
files.download("/content/stage2_final_development_evaluation_v1_results.zip")
"""
    return {
        "cells": [
            nb_cell("markdown", title),
            nb_cell("code", deps),
            nb_cell("code", imports),
            nb_cell("code", constants),
            nb_cell("code", data_helpers),
            nb_cell("code", helpers),
            nb_cell("code", train_freeze),
            nb_cell("code", validation_eval),
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
        f"""# Final Stage-2 development evaluation V1

This notebook performs the final Stage-2 development-validation comparison.
It is not final external testing.

Candidates:

1. original four-class MiniLM hybrid baseline
2. approved coarse-to-fine hierarchy with Specialist V2

Train:

- path: `data/final_v2/architecture_challenge_v1/natural_train_primary_four.jsonl`
- rows: {EXPECTED_TRAIN_TOTAL}
- counts: {EXPECTED_TRAIN_COUNTS}
- SHA256: `{EXPECTED_TRAIN_SHA256}`

Frozen development validation:

- path: `data/final_v2/architecture_challenge_v1/natural_validation_primary_four.jsonl`
- rows: {EXPECTED_VALIDATION_TOTAL}
- counts: {EXPECTED_VALIDATION_COUNTS}
- case-ID SHA256: `{EXPECTED_VALIDATION_CASE_IDS_SHA256}`

Frozen representation:

- encoder: `{MINILM_MODEL_NAME}`
- revision: `{MINILM_MODEL_REVISION}`
- semantic chunking: 1000 chars, max 2 chunks per side
- code TF-IDF: char_wb 3–5 grams, min_df=2, max_features=20000

Final specialist policy is selected from train data only before validation
scoring. After `STAGE2_TRAIN_FREEZE_COMPLETE`, the notebook evaluates both
candidates once on the same frozen 322-row development-validation split.
""",
        encoding="utf-8",
    )


def main() -> None:
    verify_artifacts()
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
                "train": str(TRAIN_JSONL.relative_to(ROOT)),
                "train_sha256": sha256_file(TRAIN_JSONL),
                "validation": str(VALIDATION_JSONL.relative_to(ROOT)),
                "validation_case_ids_sha256": stable_json_hash([row["case_id"] for row in read_jsonl(VALIDATION_JSONL)]),
                "validation_metrics_computed_locally": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
