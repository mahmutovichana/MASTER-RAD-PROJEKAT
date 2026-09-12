# S1 runtime

Local CUDA was unavailable during preparation. Repository and Hugging Face caches are runtime-only and ignored. The Kaggle canary must validate sequential model loading, 4-bit NF4 generator placement, peak memory, structured JSON, and one complete S1 case before a full development run.

Expected 2xT4 wall time is approximately 4–8 hours for 200 development cases, subject to the measured canary. Stop instead of substituting a model if the pinned 14B model is unreliable.
