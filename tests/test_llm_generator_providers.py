from __future__ import annotations

import json
import urllib.error

from docguard_llm import llm_generator
from docguard_llm.llm_generator import generate_documentation_patch


class _FakeResponse:
    def __init__(self, payload: dict):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")


def test_openai_compatible_backend_parses_chat_completion(monkeypatch) -> None:
    captured = {}

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["timeout"] = timeout
        captured["payload"] = json.loads(request.data.decode("utf-8"))
        return _FakeResponse({"choices": [{"message": {"content": "@@ Docs\n+Generated patch."}}]})

    monkeypatch.setenv("DOCGUARD_LLM_BASE_URL", "http://localhost:8000/v1")
    monkeypatch.setenv("DOCGUARD_LLM_API_KEY", "test-key")
    monkeypatch.setattr(llm_generator.urllib.request, "urlopen", fake_urlopen)

    result = generate_documentation_patch(
        "Write docs.",
        backend="openai_compatible",
        model_name="strong-doc-model",
        max_new_tokens=64,
        temperature=0.0,
    )

    assert result["generation_status"] == "ok"
    assert result["patch_text"] == "@@ Docs\n+Generated patch."
    assert captured["url"] == "http://localhost:8000/v1/chat/completions"
    assert captured["payload"]["model"] == "strong-doc-model"


def test_ollama_backend_parses_chat_response(monkeypatch) -> None:
    def fake_urlopen(_request, timeout):
        return _FakeResponse({"message": {"content": "@@ Docs\n+Generated from Ollama."}})

    monkeypatch.setattr(llm_generator.urllib.request, "urlopen", fake_urlopen)

    result = generate_documentation_patch(
        "Write docs.",
        backend="ollama",
        model_name="qwen2.5-coder:7b-instruct-q4_K_M",
        max_new_tokens=64,
        temperature=0.0,
    )

    assert result["generation_status"] == "ok"
    assert "Generated from Ollama" in result["patch_text"]


def test_openai_compatible_backend_reports_http_error_body(monkeypatch) -> None:
    class FakeHttpError(urllib.error.HTTPError):
        def read(self) -> bytes:  # type: ignore[override]
            return b'{"error":"model is not available"}'

    def fake_urlopen(_request, timeout):
        raise FakeHttpError("http://localhost/v1/chat/completions", 400, "Bad Request", {}, None)

    monkeypatch.setenv("DOCGUARD_LLM_BASE_URL", "http://localhost/v1")
    monkeypatch.setattr(llm_generator.urllib.request, "urlopen", fake_urlopen)

    result = generate_documentation_patch(
        "Write docs.",
        backend="openai_compatible",
        model_name="missing-model",
    )

    assert result["generation_status"] == "error"
    assert "HTTP 400" in result["error_message"]
    assert "model is not available" in result["error_message"]
