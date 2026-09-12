from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol, Sequence

from docguard_llm_v2.provenance_verifier import extract_atoms

from .repository_corpus import DocumentChunk, extract_identifiers
from .retrieval import RankedChunk


GENERATOR_MODEL_ID = "Qwen/Qwen2.5-Coder-14B-Instruct"
GENERATOR_REVISION = "aedcc2d42b622764e023cf882b6652e646b95671"
FINAL_STATES = {
    "ACCEPTED",
    "ABSTAINED_NO_TARGET",
    "ABSTAINED_INSUFFICIENT_EVIDENCE",
    "ABSTAINED_UNSUPPORTED_CLAIMS",
    "ABSTAINED_LOW_UTILITY",
    "FAILED_EXECUTION",
}
PROMPT_DIR = Path(__file__).resolve().parents[1] / "prompts"


def prompt_template(name: str) -> str:
    return (PROMPT_DIR / name).read_text(encoding="utf-8").strip()


class StructuredGenerator(Protocol):
    def generate_json(self, *, purpose: str, prompt: str) -> dict[str, Any]: ...


class QwenStructuredGenerator:
    """Deterministic 4-bit backend. The token is read by Hugging Face, never logged."""

    def __init__(self, *, cache_dir: str | None = None):
        import os
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

        if not os.environ.get("HF_TOKEN"):
            raise RuntimeError("HF_TOKEN must be provided through the environment")
        self.torch = torch
        self.tokenizer = AutoTokenizer.from_pretrained(
            GENERATOR_MODEL_ID, revision=GENERATOR_REVISION, cache_dir=cache_dir
        )
        quantization = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.float16,
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            GENERATOR_MODEL_ID,
            revision=GENERATOR_REVISION,
            cache_dir=cache_dir,
            quantization_config=quantization,
            device_map="auto",
            torch_dtype=torch.float16,
        )
        self.model.eval()

    def generate_json(self, *, purpose: str, prompt: str) -> dict[str, Any]:
        messages = [
            {"role": "system", "content": f"S1 repository-grounded documentation agent: {purpose}. Output valid JSON only."},
            {"role": "user", "content": prompt},
        ]
        rendered = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        batch = self.tokenizer(rendered, return_tensors="pt", truncation=False)
        if batch["input_ids"].shape[1] > 24576:
            raise ValueError("S1 grounded prompt exceeds the explicit 24576-token input budget")
        device = next(self.model.parameters()).device
        batch = {key: value.to(device) for key, value in batch.items()}
        with self.torch.no_grad():
            output = self.model.generate(
                **batch,
                do_sample=False,
                temperature=None,
                top_p=None,
                max_new_tokens=2048,
                pad_token_id=self.tokenizer.eos_token_id,
            )
        text = self.tokenizer.decode(output[0, batch["input_ids"].shape[1] :], skip_special_tokens=True).strip()
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError("Generator did not return a JSON object")
        value = json.loads(match.group(0))
        if not isinstance(value, dict):
            raise ValueError("Generator JSON must be an object")
        return value


@dataclass(frozen=True)
class S1Configuration:
    lexical_top_k: int
    dense_top_k: int
    reranker_final_candidates: int
    target_confidence_threshold: float
    prompt_variant: str
    max_repairs: int = 1

    def validate(self) -> None:
        if self.lexical_top_k not in {5, 10} or self.dense_top_k not in {5, 10}:
            raise ValueError("Unregistered retrieval top-k")
        if self.reranker_final_candidates != 3:
            raise ValueError("Reranker final candidates must equal 3")
        if self.target_confidence_threshold not in {0.35, 0.50, 0.65}:
            raise ValueError("Unregistered target confidence threshold")
        if self.prompt_variant not in {"P1", "P2"}:
            raise ValueError("Unregistered prompt variant")
        if self.max_repairs != 1:
            raise ValueError("S1 permits exactly one repair at most")


def build_retrieval_query(row: dict[str, Any]) -> str:
    changed = [str(item) for item in row.get("code_changed_files") or []]
    code_diff = str(row.get("code_diff_excerpt") or "")
    identifiers = extract_identifiers(code_diff)
    return "\n".join(
        [
            f"CATEGORY: {row.get('frozen_category_prediction') or row.get('predicted_category') or ''}",
            f"REPOSITORY: {row.get('repository') or ''}",
            f"CHANGED PATHS: {' '.join(changed)}",
            f"IDENTIFIERS: {' '.join(identifiers[:120])}",
            f"CODE DIFF: {code_diff}",
            f"DOCS BEFORE: {row.get('docs_before_excerpt') or ''}",
        ]
    )


def _json_block(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)


def target_prompt(query: str, candidates: Sequence[RankedChunk]) -> str:
    documents = [
        {
            "path": item.chunk.path,
            "headings": list(item.chunk.heading_path),
            "relevant_section": item.chunk.text,
            "lexical_score": item.lexical_score,
            "dense_score": item.dense_score,
            "reranker_score": item.reranker_score,
        }
        for item in candidates
    ]
    return (
        prompt_template("target_decision.txt")
        + "\nSchema keys: target_document, target_section, confidence, evidence, abstain_reason.\n\nQUERY:\n"
        + query
        + "\n\nCANDIDATES:\n"
        + _json_block(documents)
    )


def plan_prompt(row: dict[str, Any], selected: RankedChunk, target: dict[str, Any]) -> str:
    return (
        prompt_template("documentation_plan.txt")
        + "\nSchema keys: update_needed, target_document, target_section, change_type, developer_facing_effect, facts_to_document, facts_not_supported, style_observations, minimal_update_intent.\n\n"
        f"CODE EVIDENCE:\n{row.get('code_diff_excerpt') or ''}\n\nTARGET DECISION:\n{_json_block(target)}\n\n"
        f"PRE-CHANGE DOCUMENT SECTION:\n{selected.chunk.text}"
    )


def generation_prompt(row: dict[str, Any], selected: RankedChunk, plan: dict[str, Any], *, variant: str, style_examples: Sequence[DocumentChunk] = ()) -> str:
    style = prompt_template(f"{variant}_generation.txt")
    return (
        f"{style}\nSchema keys: target_document, target_section, patch_markdown.\n\nCHANGED PATHS:\n{_json_block(row.get('code_changed_files') or [])}\n\n"
        f"DIFF:\n{row.get('code_diff_excerpt') or ''}\n\nIDENTIFIERS:\n{_json_block(extract_identifiers(str(row.get('code_diff_excerpt') or '')))}\n\n"
        f"TARGET PATH: {selected.chunk.path}\nTARGET SECTION: {plan.get('target_section') or selected.chunk.heading}\n\n"
        f"NEARBY HEADINGS:\n{_json_block(list(selected.chunk.heading_path))}\n\nTARGET DOCUMENT BEFORE:\n{selected.chunk.text}\n\n"
        f"NEIGHBORING SAME-DOCUMENT STYLE EXAMPLES (maximum 3):\n{_json_block([item.text for item in style_examples[:3]])}\n\nPLAN:\n{_json_block(plan)}"
    )


def critic_prompt(row: dict[str, Any], selected: RankedChunk, plan: dict[str, Any], patch: dict[str, Any]) -> str:
    return (
        prompt_template("critic.txt")
        + "\nSchema keys: grounded, target_fit, useful, style_fit, unsupported_claims, unnecessary_content, decision (ACCEPT|REPAIR|ABSTAIN), repair_instructions.\n\n"
        f"DIFF:\n{row.get('code_diff_excerpt') or ''}\n\nDOCUMENT BEFORE:\n{selected.chunk.text}\n\n"
        f"PLAN:\n{_json_block(plan)}\n\nPATCH:\n{_json_block(patch)}"
    )


def repair_prompt(row: dict[str, Any], selected: RankedChunk, plan: dict[str, Any], patch: dict[str, Any], critic: dict[str, Any], *, style_examples: Sequence[DocumentChunk] = ()) -> str:
    return prompt_template("repair.txt") + "\n\n" + generation_prompt(row, selected, plan, variant="P2", style_examples=style_examples) + "\n\nORIGINAL PATCH:\n" + _json_block(patch) + "\n\nREPAIR INSTRUCTIONS:\n" + _json_block(critic.get("repair_instructions") or [])


def deterministic_unsupported_claims(patch: str, *, evidence: str) -> list[str]:
    evidence_norm = " ".join(evidence.casefold().split())
    unsupported = []
    for atom in extract_atoms(patch):
        if " ".join(str(atom).casefold().split()) not in evidence_norm:
            unsupported.append(str(atom))
    return unsupported


class S1Agent:
    def __init__(self, backend: StructuredGenerator, config: S1Configuration):
        config.validate()
        self.backend = backend
        self.config = config

    def run(self, row: dict[str, Any], candidates: Sequence[RankedChunk], *, document_corpus: Sequence[DocumentChunk] = ()) -> dict[str, Any]:
        if not candidates:
            return {"state": "ABSTAINED_NO_TARGET", "repair_count": 0, "target_decision": None}
        try:
            query = build_retrieval_query(row)
            target = self.backend.generate_json(purpose="target_decision", prompt=target_prompt(query, candidates))
            target_path = str(target.get("target_document") or "")
            confidence = float(target.get("confidence") or 0.0)
            by_path = {item.chunk.path: item for item in candidates}
            if not target_path or target_path not in by_path or confidence < self.config.target_confidence_threshold:
                return {"state": "ABSTAINED_NO_TARGET", "repair_count": 0, "target_decision": target}
            selected = by_path[target_path]
            same_document = sorted(
                [item for item in document_corpus if item.path == target_path and item.chunk_index != selected.chunk.chunk_index],
                key=lambda item: (abs(item.chunk_index - selected.chunk.chunk_index), item.chunk_index),
            )[:3]
            plan = self.backend.generate_json(purpose="documentation_plan", prompt=plan_prompt(row, selected, target))
            if not bool(plan.get("update_needed")):
                return {"state": "ABSTAINED_LOW_UTILITY", "repair_count": 0, "target_decision": target, "plan": plan}
            if not (plan.get("facts_to_document") or []):
                return {"state": "ABSTAINED_INSUFFICIENT_EVIDENCE", "repair_count": 0, "target_decision": target, "plan": plan}
            patch = self.backend.generate_json(purpose="generation", prompt=generation_prompt(row, selected, plan, variant=self.config.prompt_variant, style_examples=same_document))
            if str(patch.get("target_document") or "") != target_path:
                return {"state": "ABSTAINED_NO_TARGET", "repair_count": 0, "target_decision": target, "plan": plan, "patch": patch}
            evidence = "\n".join([str(row.get("code_diff_excerpt") or ""), str(row.get("docs_before_excerpt") or ""), selected.chunk.text, *[str(item) for item in plan.get("facts_to_document") or []]])
            deterministic_unsupported = deterministic_unsupported_claims(str(patch.get("patch_markdown") or ""), evidence=evidence)
            critic = self.backend.generate_json(purpose="critic", prompt=critic_prompt(row, selected, plan, patch))
            if deterministic_unsupported or critic.get("unsupported_claims"):
                if critic.get("decision") != "REPAIR":
                    return {"state": "ABSTAINED_UNSUPPORTED_CLAIMS", "repair_count": 0, "target_decision": target, "plan": plan, "patch": patch, "critic": critic, "deterministic_unsupported_claims": deterministic_unsupported}
            if critic.get("decision") == "ACCEPT" and all(bool(critic.get(key)) for key in ("grounded", "target_fit", "useful", "style_fit")) and not deterministic_unsupported:
                return {"state": "ACCEPTED", "repair_count": 0, "target_decision": target, "plan": plan, "patch": patch, "critic": critic}
            if critic.get("decision") != "REPAIR":
                state = "ABSTAINED_LOW_UTILITY" if not critic.get("useful") or not critic.get("style_fit") else "ABSTAINED_UNSUPPORTED_CLAIMS"
                return {"state": state, "repair_count": 0, "target_decision": target, "plan": plan, "patch": patch, "critic": critic}
            repaired = self.backend.generate_json(purpose="repair", prompt=repair_prompt(row, selected, plan, patch, critic, style_examples=same_document))
            final_critic = self.backend.generate_json(purpose="final_critic", prompt=critic_prompt(row, selected, plan, repaired))
            final_unsupported = deterministic_unsupported_claims(str(repaired.get("patch_markdown") or ""), evidence=evidence)
            if final_critic.get("decision") == "ACCEPT" and all(bool(final_critic.get(key)) for key in ("grounded", "target_fit", "useful", "style_fit")) and not final_unsupported and not final_critic.get("unsupported_claims"):
                return {"state": "ACCEPTED", "repair_count": 1, "target_decision": target, "plan": plan, "patch": repaired, "critic": final_critic}
            state = "ABSTAINED_LOW_UTILITY" if not final_critic.get("useful") or not final_critic.get("style_fit") else "ABSTAINED_UNSUPPORTED_CLAIMS"
            return {"state": state, "repair_count": 1, "target_decision": target, "plan": plan, "patch": repaired, "critic": final_critic, "deterministic_unsupported_claims": final_unsupported}
        except Exception as exc:
            return {"state": "FAILED_EXECUTION", "repair_count": 0, "error_type": type(exc).__name__, "error": str(exc)}


def load_prompt(path: Path) -> str:
    return path.read_text(encoding="utf-8")
