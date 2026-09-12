from __future__ import annotations

import math
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


class DenseEncoder(Protocol):
    def encode(self, texts: Sequence[str]) -> np.ndarray: ...


class Reranker(Protocol):
    def score(self, query: str, documents: Sequence[str]) -> list[float]: ...


@dataclass(frozen=True)
class RankedChunk:
    chunk: DocumentChunk
    lexical_score: float
    dense_score: float
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


class QwenDenseEncoder:
    def __init__(self, *, cache_dir: str | None = None, device: str | None = None, batch_size: int = 8):
        import torch
        from transformers import AutoModel, AutoTokenizer

        self.torch = torch
        self.tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL_ID, revision=EMBEDDING_REVISION, cache_dir=cache_dir)
        self.model = AutoModel.from_pretrained(EMBEDDING_MODEL_ID, revision=EMBEDDING_REVISION, cache_dir=cache_dir, torch_dtype="auto", device_map=device or "auto")
        self.model.eval()
        self.batch_size = batch_size

    def encode(self, texts: Sequence[str]) -> np.ndarray:
        torch = self.torch
        batches = []
        for start in range(0, len(texts), self.batch_size):
            batch = self.tokenizer(list(texts[start : start + self.batch_size]), padding=True, truncation=True, max_length=8192, return_tensors="pt")
            device = next(self.model.parameters()).device
            batch = {key: value.to(device) for key, value in batch.items()}
            with torch.no_grad():
                output = self.model(**batch).last_hidden_state
                indexes = batch["attention_mask"].sum(dim=1) - 1
                vectors = output[torch.arange(output.shape[0], device=device), indexes]
                vectors = torch.nn.functional.normalize(vectors, p=2, dim=1)
            batches.append(vectors.float().cpu().numpy())
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

    def score(self, query: str, documents: Sequence[str]) -> list[float]:
        torch = self.torch
        prompts = [
            "<|im_start|>system\nJudge whether the Document meets the requirements based on the Query. Answer only yes or no.<|im_end|>\n"
            f"<|im_start|>user\n<Query>: {query}\n<Document>: {document}<|im_end|>\n<|im_start|>assistant\n"
            for document in documents
        ]
        batch = self.tokenizer(prompts, padding=True, truncation=True, max_length=8192, return_tensors="pt")
        device = next(self.model.parameters()).device
        batch = {key: value.to(device) for key, value in batch.items()}
        with torch.no_grad():
            logits = self.model(**batch).logits[:, -1, [self.no_id, self.yes_id]]
            probabilities = torch.softmax(logits, dim=1)[:, 1]
        return probabilities.float().cpu().tolist()
