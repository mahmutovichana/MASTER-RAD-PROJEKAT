from __future__ import annotations

import importlib
import hashlib
import json
from typing import Any

from docguard_llm_v2.generation_options import GenerationOptions


class HuggingFaceChatBackend:
    """One-load Transformers backend for the frozen Stage 3 call interface."""

    def __init__(self, model_name: str, *, seed: int = 42, device_map: str = "auto", require_cuda: bool = True):
        self.model_name = model_name
        self.seed = int(seed)
        self.call_count = 0
        torch = importlib.import_module("torch")
        transformers = importlib.import_module("transformers")
        if require_cuda and not torch.cuda.is_available():
            raise RuntimeError("CUDA is required for the real Qwen Gate 4 execution")
        self.torch = torch
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(model_name, trust_remote_code=False)
        self.model = transformers.AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map=device_map if torch.cuda.is_available() else None,
            low_cpu_mem_usage=True,
            trust_remote_code=False,
        )
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token_id = self.tokenizer.eos_token_id

    def generate(
        self,
        messages: list[dict[str, str]],
        *,
        model: str | None = None,
        purpose: str | None = None,
        generation_options: GenerationOptions | None = None,
    ) -> str:
        if model != self.model_name:
            raise ValueError(f"Requested model {model!r} does not match loaded frozen model {self.model_name!r}")
        if purpose not in {"analysis", "writer", "repair"}:
            raise ValueError(f"Unsupported generation purpose: {purpose!r}")
        if generation_options is None or generation_options.max_tokens is None or generation_options.temperature is None:
            raise ValueError("Frozen temperature and purpose-specific max_tokens are required")
        prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        encoded = self.tokenizer(prompt, return_tensors="pt")
        device = next(self.model.parameters()).device
        encoded = {key: value.to(device) for key, value in encoded.items()}
        seed_material = json.dumps({"messages": messages, "model": model, "purpose": purpose}, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        request_seed = int(hashlib.sha256(f"{self.seed}:{seed_material}".encode("utf-8")).hexdigest()[:8], 16)
        self.torch.manual_seed(request_seed)
        if self.torch.cuda.is_available():
            self.torch.cuda.manual_seed_all(request_seed)
        self.call_count += 1
        with self.torch.inference_mode():
            output = self.model.generate(
                **encoded,
                max_new_tokens=int(generation_options.max_tokens),
                do_sample=True,
                temperature=float(generation_options.temperature),
                top_p=1.0,
                top_k=0,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                use_cache=True,
            )
        new_tokens = output[0, encoded["input_ids"].shape[1] :]
        return self.tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
