from __future__ import annotations

from docguard_llm.fact_extractor import extract_allowed_facts


API_DIFF = """
+router.post('/reviews', createReview);
+res.status(201).json({ id: saved.id, reviewStatus: saved.status });
"""


def test_api_allowed_facts_extract_visible_route_status_and_response_fields() -> None:
    facts = extract_allowed_facts(API_DIFF, "# API", "api_reference", "new_endpoint")
    allowed = facts["allowed_facts"]
    assert "/reviews" in facts["allowed_tokens"]
    assert "POST" in facts["allowed_tokens"]
    assert "201" in facts["allowed_tokens"]
    assert "id" in allowed["response_fields"]
    assert "reviewStatus" in allowed["response_fields"]


def test_api_allowed_facts_do_not_extract_hallucinated_values() -> None:
    facts = extract_allowed_facts(API_DIFF, "# API", "api_reference", "new_endpoint")
    serialized = " ".join(facts["allowed_tokens"])
    assert "title" not in serialized
    assert "pending" not in serialized
    assert "approved" not in serialized
