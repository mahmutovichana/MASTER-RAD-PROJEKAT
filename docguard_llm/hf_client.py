from __future__ import annotations

import json
import os
import time
import urllib.request

from docguard_llm.model_registry import get_model_config


BACKENDS = {"mock", "transformers_local", "text_generation_inference"}


class HFClient:
    def __init__(self, model_key: str, backend: str | None = None):
        self.model_key = model_key
        self.model_config = get_model_config(model_key)
        self.model_id = self.model_config["model_id"]
        self.backend = backend or os.getenv("DOCGUARD_LLM_BACKEND", "mock")
        if self.backend not in BACKENDS:
            raise ValueError(f"Unsupported backend {self.backend}. Use one of {sorted(BACKENDS)}")
        self.max_new_tokens = int(os.getenv("DOCGUARD_MAX_NEW_TOKENS", "800"))
        self.temperature = float(os.getenv("DOCGUARD_TEMPERATURE", "0.0"))

    def generate(self, messages: list[dict]) -> tuple[str, float]:
        start = time.perf_counter()
        if self.backend == "mock":
            output = self._mock_generate(messages)
        elif self.backend == "text_generation_inference":
            output = self._tgi_generate(messages)
        else:
            output = self._transformers_generate(messages)
        return output, time.perf_counter() - start

    def _mock_generate(self, messages: list[dict]) -> str:
        payload = json.loads(messages[-1]["content"])
        record = payload["record"]
        diff = record["code_diff"]
        changed_files = record["changed_files"]
        positive = any(signal in diff for signal in ["Router.", "z.", "res.status", "Deprecated:", "scheduleJob", "rateLimit", "FEATURE_FLAG", "Dto", "tsx watch", "vitest"])
        if "diff --git a/docs/api.md" in diff or "package.json" in " ".join(changed_files) and "docguard:" in diff:
            positive = False
        scenario = "unknown_change"
        category = "unknown"
        target = ""
        section = record.get("target_section", "")
        patch = None
        facts: list[str] = []
        if "Router.get" in diff or ".get(" in diff and "+// Deprecated" not in diff:
            scenario, category, target = "new_endpoint", "api_reference", "docs/api.md"
        elif ".min(" in diff:
            scenario, category, target = "changed_validation_min", "api_reference", "docs/api.md"
        elif "require" in diff and "Router.post" in diff:
            scenario, category, target = "changed_auth_requirement", "api_reference", "docs/api.md"
        elif ": string;" in diff:
            scenario, category, target = "added_response_field", "api_reference", "docs/api.md"
        elif "audit" in diff and "middleware" in diff.lower():
            category, target = "architecture_flow", "docs/architecture.md"
        elif "Dto" in diff:
            category, target = "model_contract", "docs/models.md"
        elif "tsx watch" in diff:
            category, target = "developer_setup", "docs/developer-setup.md"
        elif "vitest" in diff:
            category, target = "testing_instructions", "docs/testing.md"
        elif "FEATURE_FLAG" in diff:
            category, target = "configuration", "docs/configuration.md"
        elif "scheduleJob" in diff or "reserve" in diff:
            category, target = "workflow_documentation", "docs/workflows.md"
        if positive:
            target = target or "docs/api.md"
            patch = f"@@ {section}\n+Update documentation for the changed behavior."
            facts = ["documentation update required"]
        return json.dumps({
            "docs_update_required": positive,
            "scenario_type": scenario,
            "doc_category": category,
            "target_doc_file": target,
            "target_section": section,
            "generated_doc_patch": patch,
            "change_intent_summary": "Mock backend inferred the change from deterministic diff signals.",
            "primary_documentation_reason": "Documentation update required." if positive else "No documented behavior change detected.",
            "expected_facts_covered": facts,
            "confidence": 0.75 if positive else 0.55,
        })

    def _tgi_generate(self, messages: list[dict]) -> str:
        base_url = os.getenv("DOCGUARD_TGI_BASE_URL", "http://localhost:8000/v1").rstrip("/")
        body = json.dumps({
            "model": self.model_id,
            "messages": messages,
            "max_tokens": self.max_new_tokens,
            "temperature": self.temperature,
        }).encode("utf-8")
        request = urllib.request.Request(
            f"{base_url}/chat/completions",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=120) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return payload["choices"][0]["message"]["content"]

    def _transformers_generate(self, messages: list[dict]) -> str:
        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "transformers_local requires optional dependencies: install torch and transformers. "
                "7B models may require a GPU or quantized/local serving setup; use qwen2_5_coder_3b "
                "as the lightweight option or backend=text_generation_inference for vLLM/TGI."
            ) from exc
        token = os.getenv("HF_TOKEN")
        tokenizer = AutoTokenizer.from_pretrained(self.model_id, token=token)
        model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            token=token,
            torch_dtype="auto",
            device_map="auto",
        )
        if hasattr(tokenizer, "apply_chat_template"):
            prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        else:
            prompt = "\n".join(f"{m['role']}: {m['content']}" for m in messages)
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=self.max_new_tokens, do_sample=False)
        generated = outputs[0][inputs["input_ids"].shape[-1]:]
        return tokenizer.decode(generated, skip_special_tokens=True)

