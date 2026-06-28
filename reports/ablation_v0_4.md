# Ablation v0.4

| System | Precision | Recall | F1 | Positive doc category acc. | Positive target file acc. | Positive scenario acc. | Negative acc. | Macro scenario F1 | Macro doc category F1 | Latency |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| rule baseline | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.2238 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| ML-only | 1.0000 | 0.9650 | 0.9822 | 0.9650 | 0.4475 | 0.4450 | 1.0000 | 0.3333 | 0.9444 | 0.0000 |
| deterministic hybrid router | 1.0000 | 0.9650 | 0.9822 | 0.9650 | 0.9650 | 0.9650 | 1.0000 | 0.6905 | 0.9444 | 0.0000 |
| optional LLM-assisted hybrid | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

ML backend used for this ablation: `fallback`.

The optional LLM-assisted hybrid is not run by default on the CPU-only machine. It should be evaluated only on small samples with `qwen2_5_coder_0_5b` or an optional GGUF/llama.cpp backend.
