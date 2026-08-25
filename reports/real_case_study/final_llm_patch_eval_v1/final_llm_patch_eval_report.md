# DocGuard LLM Patch Evaluation V1

## Final protocol

- Language: TypeScript
- Frozen sample size: 100 predicted-positive cases
- Model: Qwen/Qwen2.5-Coder-7B-Instruct
- Temperature: 0.1
- Max new tokens: 512
- Sampling seed: 42
- Gold labels were not used for generation or sampling.
- Failed provider calls were retried without changing the model, prompt, sample, or generation parameters.

## Provider reliability

- Initial successful generations: 18
- Initial provider failures: 82
- Successful retries: 82
- Final successful generations: 100/100

## Scope: all_predicted_positive

- Cases: 100
- Grounded acceptable rate: 0.7600
- Qwen acceptable rate: 0.6700
- Final cascade acceptable rate: 0.8700

## Scope: gold_true_positive

- Cases: 88
- Grounded acceptable rate: 0.7273
- Qwen acceptable rate: 0.6705
- Final cascade acceptable rate: 0.8523

## Scope: binary_and_category_correct

- Cases: 41
- Grounded acceptable rate: 0.7561
- Qwen acceptable rate: 0.6585
- Final cascade acceptable rate: 0.8293
