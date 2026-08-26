from __future__ import annotations

import math
import re
from collections import Counter
from typing import Any

from docguard_llm_v2.schemas import DocumentCandidate


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in re.findall(r"[A-Za-z0-9_./:-]{2,}", text or "")]


def cosine(query: str, document: str) -> float:
    q = Counter(tokenize(query))
    d = Counter(tokenize(document))
    if not q or not d:
        return 0.0
    numerator = sum(q[token] * d.get(token, 0) for token in q)
    q_norm = math.sqrt(sum(value * value for value in q.values()))
    d_norm = math.sqrt(sum(value * value for value in d.values()))
    return numerator / (q_norm * d_norm) if q_norm and d_norm else 0.0


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
    candidates: list[DocumentCandidate] = []
    for item in documentation_context_candidates:
        path = str(item.get("path") or "")
        excerpt = str(item.get("excerpt") or "")
        if not path or not excerpt:
            continue
        score = cosine(query, path + "\n" + excerpt)
        candidates.append(DocumentCandidate(path=path, excerpt=excerpt, source_ref=str(item.get("source_ref") or ""), score=score))
    ranked = sorted(candidates, key=lambda item: (-item.score, item.path))[:top_k]
    return {
        "top_k": ranked,
        "retrieval_method": "token_cosine_semantic_ir_v2",
        "retrieval_query": query,
    }

