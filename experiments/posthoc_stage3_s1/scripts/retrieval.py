from __future__ import annotations

import math
import gc
from dataclasses import dataclass
from typing import Protocol, Sequence

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .repository_corpus import DocumentChunk


EMBEDDING_MODEL_ID = "Qwen/Qwen3-Embedding-0.6B"
EMBEDDING_REVISION = "97b0c614be4d77ee51c0cef4e5f07c00f9eb65b3"
RERANKER_MODEL_ID = "Qwen/Qwen3-Reranker-0.6B"
RERANKER_REVISION = "e61197ed45024b0ed8a2d74b80b4d909f1255473"
RERANKER_MAX_LENGTH = 8192
RERANKER_PROMPT_TEMPLATE = (
    "<|im_start|>system\nJudge whether the Document meets the requirements based on the Query. Answer only yes or no.<|im_end|>\n"
    "<|im_start|>user\n<Query>: {query}\n<Document>: {document}<|im_end|>\n<|im_start|>assistant\n"
)
EMBEDDING_MAX_LENGTH = 8192
EMBEDDING_LOGICAL_BATCH_SIZE = 8


class DenseEncoder(Protocol):
    def encode(self, texts: Sequence[str]) -> np.ndarray: ...


class Reranker(Protocol):
    def score(self, query: str, documents: Sequence[str]) -> list[float]: ...


@dataclass(frozen=True)
class RankedChunk:
    chunk: DocumentChunk
    lexical_score: float
    dense_score: float | None
    reranker_score: float | None = None


def chunk_text(chunk: DocumentChunk) -> str:
    headings = " > ".join(chunk.heading_path)
    return f"PATH: {chunk.path}\nHEADINGS: {headings}\n{chunk.text}"


def lexical_scores(query: str, chunks: Sequence[DocumentChunk]) -> np.ndarray:
    if not chunks:
        return np.zeros(0, dtype=float)
    corpus = [query] + [chunk_text(chunk) for chunk in chunks]
    matrix = TfidfVectorizer(
        analyzer="word",
        ngram_range=(1, 2),
        token_pattern=r"(?u)\b[\w./:@+\-#]+\b",
        sublinear_tf=True,
    ).fit_transform(corpus)
    return cosine_similarity(matrix[0], matrix[1:]).ravel()


def cosine_dense_scores(query_vector: np.ndarray, document_vectors: np.ndarray) -> np.ndarray:
    query = np.asarray(query_vector, dtype=float).reshape(1, -1)
    docs = np.asarray(document_vectors, dtype=float)
    query /= np.maximum(np.linalg.norm(query, axis=1, keepdims=True), 1e-12)
    docs /= np.maximum(np.linalg.norm(docs, axis=1, keepdims=True), 1e-12)
    return (query @ docs.T).ravel()


def hybrid_retrieve(
    query: str,
    chunks: Sequence[DocumentChunk],
    *,
    dense_encoder: DenseEncoder,
    lexical_top_k: int,
    dense_top_k: int,
) -> list[RankedChunk]:
    if lexical_top_k not in {5, 10} or dense_top_k not in {5, 10}:
        raise ValueError("S1 bounded retrieval permits lexical/dense top-k only in {5,10}")
    if not chunks:
        return []
    lexical = lexical_scores(query, chunks)
    embeddings = dense_encoder.encode([query, *[chunk_text(chunk) for chunk in chunks]])
    if embeddings.shape[0] != len(chunks) + 1:
        raise ValueError("Dense encoder returned an unexpected row count")
    dense = cosine_dense_scores(embeddings[0], embeddings[1:])
    lexical_ids = sorted(range(len(chunks)), key=lambda index: (-float(lexical[index]), chunks[index].path, chunks[index].chunk_index))[:lexical_top_k]
    dense_ids = sorted(range(len(chunks)), key=lambda index: (-float(dense[index]), chunks[index].path, chunks[index].chunk_index))[:dense_top_k]
    union = sorted(set(lexical_ids) | set(dense_ids), key=lambda index: (-max(float(lexical[index]), float(dense[index])), chunks[index].path, chunks[index].chunk_index))
    return [RankedChunk(chunks[index], float(lexical[index]), float(dense[index])) for index in union]


def rerank_top_documents(query: str, candidates: Sequence[RankedChunk], *, reranker: Reranker, final_documents: int = 3) -> list[RankedChunk]:
    if final_documents != 3:
        raise ValueError("S1 reranker final candidate count is fixed at 3")
    if not candidates:
        return []
    scores = reranker.score(query, [chunk_text(item.chunk) for item in candidates])
    if len(scores) != len(candidates):
        raise ValueError("Reranker returned an unexpected score count")
    reranked = [RankedChunk(item.chunk, item.lexical_score, item.dense_score, float(score)) for item, score in zip(candidates, scores)]
    # Keep the highest chunk for each document, then select three documents.
    best_by_path: dict[str, RankedChunk] = {}
    for item in reranked:
        old = best_by_path.get(item.chunk.path)
        item_score = -math.inf if item.reranker_score is None else item.reranker_score
        old_score = -math.inf if old is None or old.reranker_score is None else old.reranker_score
        if old is None or item_score > old_score:
            best_by_path[item.chunk.path] = item
    return sorted(
        best_by_path.values(),
        key=lambda item: (-(-math.inf if item.reranker_score is None else item.reranker_score), item.chunk.path),
    )[:3]


def path_aware_lexical_top_documents(query: str, chunks: Sequence[DocumentChunk], *, final_documents: int = 3) -> list[RankedChunk]:
    if final_documents != 3:
        raise ValueError("S1 compute-constrained lexical fallback is fixed at three distinct documents")
    scores = lexical_scores(query, chunks)
    ordered_indices = sorted(
        range(len(chunks)),
        key=lambda index: (-float(scores[index]), chunks[index].path, chunks[index].chunk_index),
    )
    selected: list[RankedChunk] = []
    seen_paths: set[str] = set()
    for index in ordered_indices:
        chunk = chunks[index]
        if chunk.path in seen_paths:
            continue
        seen_paths.add(chunk.path)
        selected.append(RankedChunk(chunk, float(scores[index]), None, None))
        if len(selected) == final_documents:
            break
    return selected


class QwenDenseEncoder:
    def __init__(self, *, cache_dir: str | None = None, device: str | None = None, batch_size: int = EMBEDDING_LOGICAL_BATCH_SIZE):
        import torch
        from transformers import AutoModel, AutoTokenizer

        if batch_size != EMBEDDING_LOGICAL_BATCH_SIZE:
            raise ValueError("Frozen S1 embedding logical batch size must remain 8")
        self.torch = torch
        self.tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL_ID, revision=EMBEDDING_REVISION, cache_dir=cache_dir)
        self.model = AutoModel.from_pretrained(EMBEDDING_MODEL_ID, revision=EMBEDDING_REVISION, cache_dir=cache_dir, torch_dtype="auto", device_map=device or "auto")
        self.model.eval()
        self.batch_size = batch_size
        self.last_encode_diagnostics: dict[str, object] = {}

    def _encode_batch(self, texts: Sequence[str]) -> np.ndarray:
        torch = self.torch
        batch = None
        output = None
        vectors = None
        try:
            batch = self.tokenizer(list(texts), padding=True, truncation=True, max_length=EMBEDDING_MAX_LENGTH, return_tensors="pt")
            device = next(self.model.parameters()).device
            batch = {key: value.to(device) for key, value in batch.items()}
            with torch.no_grad():
                output = self.model(**batch).last_hidden_state
                indexes = batch["attention_mask"].sum(dim=1) - 1
                vectors = output[torch.arange(output.shape[0], device=device), indexes]
                vectors = torch.nn.functional.normalize(vectors, p=2, dim=1)
            return vectors.float().cpu().numpy()
        finally:
            del vectors
            del output
            del batch

    def _encode_adaptive(self, texts: Sequence[str], diagnostics: dict[str, object]) -> np.ndarray:
        size = len(texts)
        diagnostics["attempted_batch_sizes"].append(size)
        try:
            result = self._encode_batch(texts)
            diagnostics["effective_batch_sizes_used"].append(size)
            return result
        except self.torch.cuda.OutOfMemoryError:
            gc.collect()
            self.torch.cuda.empty_cache()
            if size == 1:
                diagnostics["single_item_oom"] = True
                raise
            diagnostics["oom_split_count"] += 1
            midpoint = size // 2
            left = self._encode_adaptive(texts[:midpoint], diagnostics)
            right = self._encode_adaptive(texts[midpoint:], diagnostics)
            return np.concatenate([left, right], axis=0)

    def encode(self, texts: Sequence[str]) -> np.ndarray:
        diagnostics: dict[str, object] = {
            "configured_max_batch_size": self.batch_size,
            "attempted_batch_sizes": [],
            "effective_batch_sizes_used": [],
            "oom_split_count": 0,
            "minimum_effective_batch_size": None,
            "single_item_oom": False,
        }
        batches = []
        try:
            for start in range(0, len(texts), self.batch_size):
                batches.append(self._encode_adaptive(list(texts[start : start + self.batch_size]), diagnostics))
        finally:
            used = diagnostics["effective_batch_sizes_used"]
            diagnostics["minimum_effective_batch_size"] = min(used) if used else None
            self.last_encode_diagnostics = diagnostics
        return np.concatenate(batches, axis=0) if batches else np.empty((0, 0))


class QwenReranker:
    def __init__(self, *, cache_dir: str | None = None, device: str | None = None):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        self.torch = torch
        self.tokenizer = AutoTokenizer.from_pretrained(RERANKER_MODEL_ID, revision=RERANKER_REVISION, cache_dir=cache_dir, padding_side="left")
        self.model = AutoModelForCausalLM.from_pretrained(RERANKER_MODEL_ID, revision=RERANKER_REVISION, cache_dir=cache_dir, torch_dtype="auto", device_map=device or "auto")
        self.model.eval()
        self.yes_id = self.tokenizer.convert_tokens_to_ids("yes")
        self.no_id = self.tokenizer.convert_tokens_to_ids("no")
        self.last_score_diagnostics: dict[str, object] = {}

    def _tokenized_batch(self, query: str, documents: Sequence[str]):
        prompts = [RERANKER_PROMPT_TEMPLATE.format(query=query, document=document) for document in documents]
        batch = self.tokenizer(prompts, padding=True, truncation=True, max_length=RERANKER_MAX_LENGTH, return_tensors="pt")
        device = next(self.model.parameters()).device
        return {key: value.to(device) for key, value in batch.items()}, device

    def _record_peak_cuda_memory(self, device) -> None:
        if getattr(device, "type", str(device).split(":", 1)[0]) != "cuda":
            return
        with self.torch.cuda.device(device):
            peak = int(self.torch.cuda.max_memory_allocated())
        previous = self._score_peak_allocated_cuda_bytes
        self._score_peak_allocated_cuda_bytes = peak if previous is None else max(previous, peak)

    def _score_batch(self, query: str, documents: Sequence[str]) -> list[float]:
        torch = self.torch
        batch = None
        outputs = None
        logits = None
        probabilities = None
        device = None
        try:
            batch, device = self._tokenized_batch(query, documents)
            with torch.inference_mode():
                outputs = self.model(**batch, logits_to_keep=1, use_cache=False)
                logits = outputs.logits[:, -1, [self.no_id, self.yes_id]]
                probabilities = torch.softmax(logits, dim=1)[:, 1]
            self._record_peak_cuda_memory(device)
            return probabilities.float().cpu().tolist()
        finally:
            del probabilities
            del logits
            del outputs
            del batch

    def verify_last_token_equivalence(self, query: str, documents: Sequence[str], *, rtol: float = 1e-6, atol: float = 1e-7) -> dict[str, object]:
        torch = self.torch
        full_batch = None
        optimized_batch = None
        full_outputs = None
        optimized_outputs = None
        cache_enabled_outputs = None
        old_probability = None
        new_probability = None
        cache_enabled_probability = None
        try:
            full_batch, _ = self._tokenized_batch(query, documents)
            optimized_batch, _ = self._tokenized_batch(query, documents)
            tokenizer_output_identical = set(full_batch) == set(optimized_batch) and all(
                torch.equal(full_batch[key], optimized_batch[key]) for key in full_batch
            )
            if not tokenizer_output_identical:
                raise RuntimeError("Old and optimized reranker paths received different tokenized inputs")
            with torch.inference_mode():
                full_outputs = self.model(**full_batch, use_cache=False, logits_to_keep=0)
                old_logits = full_outputs.logits[:, -1, [self.no_id, self.yes_id]]
                old_probability = torch.softmax(old_logits, dim=1)[:, 1]
                optimized_outputs = self.model(**optimized_batch, use_cache=False, logits_to_keep=1)
                new_logits = optimized_outputs.logits[:, -1, [self.no_id, self.yes_id]]
                new_probability = torch.softmax(new_logits, dim=1)[:, 1]
                cache_enabled_outputs = self.model(**optimized_batch, use_cache=True, logits_to_keep=1)
                cache_enabled_logits = cache_enabled_outputs.logits[:, -1, [self.no_id, self.yes_id]]
                cache_enabled_probability = torch.softmax(cache_enabled_logits, dim=1)[:, 1]
            equivalent = bool(torch.allclose(old_probability, new_probability, rtol=rtol, atol=atol))
            cache_setting_equivalent = bool(torch.allclose(cache_enabled_probability, new_probability, rtol=rtol, atol=atol))
            maximum_absolute_difference = float(torch.max(torch.abs(old_probability - new_probability)).item()) if len(documents) else 0.0
            if not equivalent:
                raise RuntimeError(f"Full-logits and last-token-only reranker probabilities differ: max_abs={maximum_absolute_difference}")
            if not cache_setting_equivalent:
                raise RuntimeError("use_cache=False changed the last-token reranker probability")
            return {
                "pair_count": len(documents),
                "tokenizer_output_identical": True,
                "yes_token_id": self.yes_id,
                "no_token_id": self.no_id,
                "old_scores": old_probability.float().cpu().tolist(),
                "new_scores": new_probability.float().cpu().tolist(),
                "maximum_absolute_difference": maximum_absolute_difference,
                "rtol": rtol,
                "atol": atol,
                "equivalent": True,
                "use_cache_false_probability_equivalent": True,
                "full_logits_to_keep": 0,
                "optimized_logits_to_keep": 1,
                "use_cache": False,
            }
        finally:
            del cache_enabled_probability
            del new_probability
            del old_probability
            del cache_enabled_outputs
            del optimized_outputs
            del full_outputs
            del optimized_batch
            del full_batch

    def _score_adaptive(self, query: str, documents: Sequence[str], diagnostics: dict[str, object]) -> list[float]:
        size = len(documents)
        diagnostics["attempted_batch_sizes"].append(size)
        try:
            scores = self._score_batch(query, documents)
            diagnostics["effective_batch_sizes_used"].append(size)
            return scores
        except self.torch.cuda.OutOfMemoryError:
            gc.collect()
            self.torch.cuda.empty_cache()
            if size == 1:
                diagnostics["single_item_oom"] = True
                raise
            diagnostics["oom_split_count"] += 1
            midpoint = size // 2
            left = self._score_adaptive(query, documents[:midpoint], diagnostics)
            right = self._score_adaptive(query, documents[midpoint:], diagnostics)
            return [*left, *right]

    def score(self, query: str, documents: Sequence[str]) -> list[float]:
        document_list = list(documents)
        diagnostics: dict[str, object] = {
            "candidate_count": len(document_list),
            "logits_to_keep": 1,
            "use_cache": False,
            "forward_mode": "LAST_TOKEN_ONLY",
            "exact_execution_optimization_not_scoring_change": True,
            "attempted_batch_sizes": [],
            "effective_batch_sizes_used": [],
            "oom_split_count": 0,
            "minimum_effective_batch_size": None,
            "single_item_oom": False,
            "output_count": 0,
            "peak_allocated_cuda_bytes": None,
        }
        self._score_peak_allocated_cuda_bytes = None
        try:
            scores = self._score_adaptive(query, document_list, diagnostics) if document_list else []
            if len(scores) != len(document_list):
                raise RuntimeError("Reranker score count does not match document count")
            if not all(math.isfinite(value) and 0.0 <= value <= 1.0 for value in scores):
                raise RuntimeError("Reranker returned a non-finite or out-of-range score")
            diagnostics["output_count"] = len(scores)
            return scores
        finally:
            used = diagnostics["effective_batch_sizes_used"]
            diagnostics["minimum_effective_batch_size"] = min(used) if used else None
            diagnostics["peak_allocated_cuda_bytes"] = self._score_peak_allocated_cuda_bytes
            self.last_score_diagnostics = diagnostics
