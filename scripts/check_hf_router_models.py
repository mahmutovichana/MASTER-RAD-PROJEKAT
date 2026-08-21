from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request


DEFAULT_MODELS = [
    "Qwen/Qwen2.5-Coder-7B-Instruct",
    "Qwen/Qwen2.5-Coder-7B-Instruct:novita",
    "Qwen/Qwen2.5-Coder-32B-Instruct",
    "Qwen/Qwen2.5-Coder-32B-Instruct:novita",
    "Qwen/Qwen2.5-7B-Instruct",
    "Qwen/Qwen2.5-7B-Instruct:nebius",
    "meta-llama/Llama-3.1-8B-Instruct",
    "mistralai/Mistral-7B-Instruct-v0.3",
]


def call_chat(base_url: str, token: str, model: str, timeout: int) -> dict:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Return only a short Markdown patch."},
            {"role": "user", "content": "Return exactly this patch:\n@@ Docs\n+`PING` works."},
        ],
        "max_tokens": 32,
        "temperature": 0.0,
    }
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
            data = json.loads(body)
            text = ((data.get("choices") or [{}])[0].get("message") or {}).get("content", "")
            return {"model": model, "ok": True, "status": response.status, "text": text[:300], "error": ""}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return {"model": model, "ok": False, "status": exc.code, "text": "", "error": body[:800]}
    except Exception as exc:
        return {"model": model, "ok": False, "status": None, "text": "", "error": str(exc)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=os.getenv("DOCGUARD_LLM_BASE_URL", "https://router.huggingface.co/v1"))
    parser.add_argument("--token-env", default="DOCGUARD_LLM_API_KEY")
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--models", nargs="*", default=DEFAULT_MODELS)
    args = parser.parse_args()
    token = os.getenv(args.token_env)
    if not token:
        print(json.dumps({"status": "error", "message": f"Missing environment variable {args.token_env}"}, indent=2))
        return 1
    results = [call_chat(args.base_url, token, model, args.timeout) for model in args.models]
    print(json.dumps({"status": "ok", "base_url": args.base_url, "results": results}, indent=2, ensure_ascii=False))
    return 0 if any(result["ok"] for result in results) else 2


if __name__ == "__main__":
    raise SystemExit(main())
