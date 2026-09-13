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


STRUCTURED_SCHEMAS: dict[str, dict[str, Any]] = {
    "target_decision": {
        "required": ("target_document", "target_section", "confidence", "evidence", "abstain_reason"),
        "shape": {"target_document": "string|null", "target_section": "string|null", "confidence": "number in [0,1]", "evidence": "list", "abstain_reason": "string|null"},
    },
    "documentation_plan": {
        "required": ("update_needed", "target_document", "target_section", "change_type", "developer_facing_effect", "facts_to_document", "facts_not_supported", "style_observations", "minimal_update_intent"),
        "shape": {"update_needed": "bool", "target_document": "string", "target_section": "string|null", "change_type": "string", "developer_facing_effect": "string", "facts_to_document": "list", "facts_not_supported": "list", "style_observations": "list", "minimal_update_intent": "string"},
    },
    "generation": {
        "required": ("target_document", "target_section", "patch_markdown"),
        "shape": {"target_document": "string", "target_section": "string|null", "patch_markdown": "string"},
    },
    "critic": {
        "required": ("grounded", "target_fit", "useful", "style_fit", "unsupported_claims", "unnecessary_content", "decision", "repair_instructions"),
        "shape": {"grounded": "bool", "target_fit": "bool", "useful": "bool", "style_fit": "bool", "unsupported_claims": "list", "unnecessary_content": "list", "decision": "ACCEPT|REPAIR|ABSTAIN", "repair_instructions": "list"},
    },
}


class StructuredSchemaError(ValueError):
    pass


def canonical_schema_purpose(purpose: str) -> str:
    if purpose == "target_decision":
        return "target_decision"
    if purpose == "documentation_plan":
        return "documentation_plan"
    if purpose in {"generation", "repair"}:
        return "generation"
    if purpose in {"critic", "final_critic"}:
        return "critic"
    raise StructuredSchemaError(f"No registered structured schema for purpose: {purpose}")


def validate_structured_output(purpose: str, value: Any) -> list[str]:
    schema_name = canonical_schema_purpose(purpose)
    schema = STRUCTURED_SCHEMAS[schema_name]
    if not isinstance(value, dict):
        return ["response must be a JSON object"]
    errors = [f"missing required key: {key}" for key in schema["required"] if key not in value]
    if schema_name == "target_decision":
        confidence = value.get("confidence")
        if "confidence" in value and (isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or not 0.0 <= float(confidence) <= 1.0):
            errors.append("confidence must be numeric and bounded in [0,1]")
        if "evidence" in value and not isinstance(value["evidence"], list):
            errors.append("evidence must be a list")
    elif schema_name == "documentation_plan":
        if "update_needed" in value and not isinstance(value["update_needed"], bool):
            errors.append("update_needed must be bool")
        for key in ("facts_to_document", "facts_not_supported", "style_observations"):
            if key in value and not isinstance(value[key], list):
                errors.append(f"{key} must be a list")
    elif schema_name == "generation":
        if "patch_markdown" in value and not isinstance(value["patch_markdown"], str):
            errors.append("patch_markdown must be a string")
    elif schema_name == "critic":
        for key in ("grounded", "target_fit", "useful", "style_fit"):
            if key in value and not isinstance(value[key], bool):
                errors.append(f"{key} must be bool")
        for key in ("unsupported_claims", "unnecessary_content", "repair_instructions"):
            if key in value and not isinstance(value[key], list):
                errors.append(f"{key} must be a list")
        if "decision" in value and value["decision"] not in {"ACCEPT", "REPAIR", "ABSTAIN"}:
            errors.append("decision must be one of ACCEPT, REPAIR, ABSTAIN")
    return errors


def schema_correction_prompt(purpose: str, original_prompt: str, initial_value: Any, errors: Sequence[str]) -> str:
    schema_name = canonical_schema_purpose(purpose)
    schema = STRUCTURED_SCHEMAS[schema_name]
    return (
        "SCHEMA-CORRECTION RETRY (the only permitted serialization retry).\n"
        "Return the SAME underlying decision using complete, valid JSON. Do not add facts, change the decision, reinterpret "
        "the evidence, or provide commentary. Python will not invent or default missing values.\n\n"
        f"SCHEMA ERRORS:\n{_json_block(list(errors))}\n\n"
        f"EXACT REQUIRED JSON SHAPE:\n{_json_block(schema['shape'])}\n\n"
        f"INITIAL JSON TO CORRECT WITHOUT CHANGING ITS DECISION:\n{_json_block(initial_value)}\n\n"
        f"ORIGINAL EVIDENCE AND PROMPT (unchanged):\n{original_prompt}"
    )


class SchemaRetryingGenerator:
    """Validate every structured decision and allow one serialization-only retry."""

    maximum_schema_retries = 1

    def __init__(self, backend: StructuredGenerator):
        self.backend = backend
        self.diagnostics: list[dict[str, Any]] = []

    def generate_json(self, *, purpose: str, prompt: str) -> dict[str, Any]:
        initial = self.backend.generate_json(purpose=purpose, prompt=prompt)
        initial_errors = validate_structured_output(purpose, initial)
        diagnostic = {
            "purpose": purpose,
            "initial_schema_valid": not initial_errors,
            "schema_retry_used": bool(initial_errors),
            "schema_retry_valid": None,
            "schema_errors": list(initial_errors),
        }
        if not initial_errors:
            self.diagnostics.append(diagnostic)
            return initial
        retry = self.backend.generate_json(
            purpose=f"{purpose}_schema_correction",
            prompt=schema_correction_prompt(purpose, prompt, initial, initial_errors),
        )
        retry_errors = validate_structured_output(purpose, retry)
        diagnostic["schema_retry_valid"] = not retry_errors
        if retry_errors:
            diagnostic["schema_errors"].extend(f"retry: {error}" for error in retry_errors)
        self.diagnostics.append(diagnostic)
        if retry_errors:
            raise StructuredSchemaError(f"{purpose} schema invalid after one correction retry: {retry_errors}")
        return retry


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
        self.backend = backend if isinstance(backend, SchemaRetryingGenerator) else SchemaRetryingGenerator(backend)
        self.config = config

    def run(self, row: dict[str, Any], candidates: Sequence[RankedChunk], *, document_corpus: Sequence[DocumentChunk] = ()) -> dict[str, Any]:
        diagnostic_start = len(self.backend.diagnostics)

        def finish(value: dict[str, Any]) -> dict[str, Any]:
            value["structured_call_diagnostics"] = self.backend.diagnostics[diagnostic_start:]
            return value

        if not candidates:
            return finish({"state": "ABSTAINED_NO_TARGET", "repair_count": 0, "target_decision": None})
        try:
            query = build_retrieval_query(row)
            target = self.backend.generate_json(purpose="target_decision", prompt=target_prompt(query, candidates))
            target_path = str(target.get("target_document") or "")
            confidence = float(target.get("confidence") or 0.0)
            by_path = {item.chunk.path: item for item in candidates}
            if not target_path or target_path not in by_path or confidence < self.config.target_confidence_threshold:
                return finish({"state": "ABSTAINED_NO_TARGET", "repair_count": 0, "target_decision": target})
            selected = by_path[target_path]
            same_document = sorted(
                [item for item in document_corpus if item.path == target_path and item.chunk_index != selected.chunk.chunk_index],
                key=lambda item: (abs(item.chunk_index - selected.chunk.chunk_index), item.chunk_index),
            )[:3]
            plan = self.backend.generate_json(purpose="documentation_plan", prompt=plan_prompt(row, selected, target))
            if not bool(plan.get("update_needed")):
                return finish({"state": "ABSTAINED_LOW_UTILITY", "repair_count": 0, "target_decision": target, "plan": plan})
            if not (plan.get("facts_to_document") or []):
                return finish({"state": "ABSTAINED_INSUFFICIENT_EVIDENCE", "repair_count": 0, "target_decision": target, "plan": plan})
            patch = self.backend.generate_json(purpose="generation", prompt=generation_prompt(row, selected, plan, variant=self.config.prompt_variant, style_examples=same_document))
            if str(patch.get("target_document") or "") != target_path:
                return finish({"state": "ABSTAINED_NO_TARGET", "repair_count": 0, "target_decision": target, "plan": plan, "patch": patch})
            evidence = "\n".join([str(row.get("code_diff_excerpt") or ""), str(row.get("docs_before_excerpt") or ""), selected.chunk.text, *[str(item) for item in plan.get("facts_to_document") or []]])
            deterministic_unsupported = deterministic_unsupported_claims(str(patch.get("patch_markdown") or ""), evidence=evidence)
            critic = self.backend.generate_json(purpose="critic", prompt=critic_prompt(row, selected, plan, patch))
            if deterministic_unsupported or critic.get("unsupported_claims"):
                if critic.get("decision") != "REPAIR":
                    return finish({"state": "ABSTAINED_UNSUPPORTED_CLAIMS", "repair_count": 0, "target_decision": target, "plan": plan, "patch": patch, "critic": critic, "deterministic_unsupported_claims": deterministic_unsupported})
            if critic.get("decision") == "ACCEPT" and all(bool(critic.get(key)) for key in ("grounded", "target_fit", "useful", "style_fit")) and not deterministic_unsupported:
                return finish({"state": "ACCEPTED", "repair_count": 0, "target_decision": target, "plan": plan, "patch": patch, "critic": critic})
            if critic.get("decision") != "REPAIR":
                state = "ABSTAINED_LOW_UTILITY" if not critic.get("useful") or not critic.get("style_fit") else "ABSTAINED_UNSUPPORTED_CLAIMS"
                return finish({"state": state, "repair_count": 0, "target_decision": target, "plan": plan, "patch": patch, "critic": critic})
            repaired = self.backend.generate_json(purpose="repair", prompt=repair_prompt(row, selected, plan, patch, critic, style_examples=same_document))
            final_critic = self.backend.generate_json(purpose="final_critic", prompt=critic_prompt(row, selected, plan, repaired))
            final_unsupported = deterministic_unsupported_claims(str(repaired.get("patch_markdown") or ""), evidence=evidence)
            if final_critic.get("decision") == "ACCEPT" and all(bool(final_critic.get(key)) for key in ("grounded", "target_fit", "useful", "style_fit")) and not final_unsupported and not final_critic.get("unsupported_claims"):
                return finish({"state": "ACCEPTED", "repair_count": 1, "target_decision": target, "plan": plan, "patch": repaired, "critic": final_critic})
            state = "ABSTAINED_LOW_UTILITY" if not final_critic.get("useful") or not final_critic.get("style_fit") else "ABSTAINED_UNSUPPORTED_CLAIMS"
            return finish({"state": state, "repair_count": 1, "target_decision": target, "plan": plan, "patch": repaired, "critic": final_critic, "deterministic_unsupported_claims": final_unsupported})
        except Exception as exc:
            return finish({"state": "FAILED_EXECUTION", "repair_count": 0, "error_type": type(exc).__name__, "error": str(exc)})


def load_prompt(path: Path) -> str:
    return path.read_text(encoding="utf-8")
