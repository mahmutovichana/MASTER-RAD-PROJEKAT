from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from docguard_llm_v2.pipeline import generate_semantic_documentation_patch


class MockStage3Llm:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def generate(self, messages, model=None, purpose=None):
        self.calls.append(str(purpose))
        if purpose == "analysis":
            return json.dumps(
                {
                    "change_summary": "Adds REVIEW_WINDOW configuration.",
                    "behavior_before": "The review window was not configurable.",
                    "behavior_after": "REVIEW_WINDOW controls the review window and defaults to 7d.",
                    "developer_or_user_impact": "Operators can configure how long reviews stay open.",
                    "documentation_impact": "Configuration documentation should mention REVIEW_WINDOW.",
                    "supported_inferences": [
                        {
                            "claim": "REVIEW_WINDOW is read from process.env and defaults to 7d.",
                            "evidence_source": "code_diff",
                            "evidence_quote": "process.env.REVIEW_WINDOW || '7d'",
                        }
                    ],
                    "uncertainties": [],
                }
            )
        if purpose == "writer":
            return json.dumps(
                {
                    "target_document_path": "docs/configuration.md",
                    "target_section": "Environment Variables",
                    "patch_markdown": "- `REVIEW_WINDOW` controls the review window and defaults to `7d`.",
                    "writer_confidence": 0.82,
                }
            )
        raise AssertionError(f"unexpected mock LLM purpose: {purpose}")


def main() -> int:
    result = generate_semantic_documentation_patch(
        docs_update_required=True,
        predicted_category="configuration",
        code_diff="+export const reviewWindow = process.env.REVIEW_WINDOW || '7d';",
        docs_before="# Configuration\n\n## Environment Variables\n- `PORT` controls the HTTP port.",
        documentation_context_candidates=[
            {
                "path": "docs/configuration.md",
                "excerpt": "# Configuration\n\n## Environment Variables\n- `PORT` controls the HTTP port.",
                "source_ref": "base123",
            }
        ],
        llm_backend=MockStage3Llm(),
        config={"top_k_documents": 1, "max_repair_attempts": 1},
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["final_status"] == "accepted_first_pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
