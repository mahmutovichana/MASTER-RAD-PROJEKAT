from __future__ import annotations

import re
from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from docguard_llm_v2.schemas import DocumentCandidate


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in re.findall(r"[A-Za-z0-9_./:-]{2,}", text or "")]


def build_query(*, predicted_category: str, analysis: dict[str, Any], code_diff: str) -> str:
    claims = " ".join(str(item.get("claim") or "") for item in analysis.get("supported_inferences") or [] if item.get("evidence_valid", True))
    return " ".join(
        [
            predicted_category,
            str(analysis.get("change_summary") or ""),
            str(analysis.get("behavior_after") or ""),
            str(analysis.get("documentation_impact") or ""),
            claims,
            " ".join(tokenize(code_diff)[:80]),
        ]
    )


def retrieve_documents(*, predicted_category: str, analysis: dict[str, Any], code_diff: str, documentation_context_candidates: list[dict[str, Any]], top_k: int = 3) -> dict[str, Any]:
    query = build_query(predicted_category=predicted_category, analysis=analysis, code_diff=code_diff)
    raw_candidates: list[tuple[str, str, str]] = []
    for item in documentation_context_candidates:
        path = str(item.get("path") or "")
        excerpt = str(item.get("excerpt") or "")
        if not path or not excerpt:
            continue
        raw_candidates.append((path, excerpt, str(item.get("source_ref") or "")))
    if not raw_candidates:
        return {"top_k": [], "retrieval_method": "tfidf_cosine_semantic_ir_v2", "retrieval_query": query}
    corpus = [query] + [path + "\n" + excerpt for path, excerpt, _ in raw_candidates]
    matrix = TfidfVectorizer(analyzer="word", ngram_range=(1, 2), token_pattern=r"(?u)\b[\w./:@+\-#]+\b", sublinear_tf=True).fit_transform(corpus)
    scores = cosine_similarity(matrix[0], matrix[1:]).ravel()
    candidates = [
        DocumentCandidate(path=path, excerpt=excerpt, source_ref=source_ref, score=float(score))
        for (path, excerpt, source_ref), score in zip(raw_candidates, scores)
    ]
    ranked = sorted(candidates, key=lambda item: (-item.score, item.path))[:top_k]
    return {
        "top_k": ranked,
        "retrieval_method": "tfidf_cosine_semantic_ir_v2",
        "retrieval_query": query,
    }
