# Gate 7 Final Thesis Evidence Synthesis

## Scientific status

This report consolidates the frozen experimental evidence from Gates 1?6 and the separately frozen post-hoc S1 development challenger.

The evidence classes are intentionally kept separate:

- Gate 5: one-shot confirmation evidence.
- Gate 6: frozen human evaluation of the original Stage 3 system.
- Gate 4: development-only Stage 3 evidence.
- S1: post-hoc development-only challenger evidence.

S1 is not treated as confirmation evidence and is not pooled with Gate 5 or Gate 6.

## 1. Frozen classifier confirmation

### Binary classifier

Primary metric: MCC

- Confirmation MCC: **0.538**
- 95% repository-bootstrap CI: **[0.138, 0.789]**
- Development OOF MCC: **0.832**
- Absolute development-to-confirmation change: **-0.294**

The binary model therefore retained meaningful predictive signal on the sealed confirmation set, but performance was materially below the development estimate.

### Category classifier

Primary metric: Macro-F1

- Confirmation Macro-F1: **0.403**
- 95% repository-bootstrap CI: **[0.329, 0.429]**
- Development OOF Macro-F1: **0.861**
- Absolute development-to-confirmation change: **-0.458**

The category classifier exhibits a pronounced generalization gap. This is a central result rather than an artifact to be hidden: the development protocol produced substantially stronger estimates than were observed during the frozen one-shot confirmation.

## 2. Original Stage 3 system

### Development evidence

On the primary Gate 4 development sample:

- sample size: **100**
- retrieval context available: **8**
- Stage 3 invocation rate: **8.0%**
- conditional automated acceptance rate: **25.0%**

These values are development evidence only.

### One-shot confirmation pipeline behavior

Among **454** predicted-positive confirmation cases:

- retrieval context available: **120**
- retrieval context unavailable: **334**
- pipeline accepted outputs: **56**
- human review required: **64**

The high number of retrieval-context-unavailable cases shows that the retrieval stage was a major bottleneck in the original architecture.

## 3. Frozen Gate 6 human evaluation

The primary natural-distribution sample contained **100** cases.

Only **14** cases produced scorable outputs, corresponding to end-to-end system coverage of **14.0%**.

Conditional human quality among those generated outputs was:

- factual correctness: **4.14/5**
- readability: **4.71/5**
- semantic completeness: **4.36/5**
- developer usefulness: **2.00/5**
- style fit: **2.07/5**

Human accept-as-is was:

- conditional on generated output: **0.0%**
- end-to-end: **0.0%**

The results therefore distinguish two issues. When the system produced an output, factual correctness, readability, and semantic completeness were comparatively strong. However, end-to-end coverage was low and outputs were not considered ready for direct acceptance without editing. Developer usefulness and style fit also remained substantially weaker.

## 4. Post-hoc S1 development challenger

S1 was executed only after the frozen final evaluation and is treated strictly as post-hoc development evidence.

The selected prompt was **P1**, chosen by human reviewer preference **16?6**.

No operating threshold was selected.

Threshold-specific development results were:

### t = 0.35

- automated accepted-output coverage: **54.5%**
- abstention: **45.5%**
- execution error rate: **0.0%**
- target-not-retrieved rate: **0.0%**
- unsupported-fact violation rate: **15.0%**

### t = 0.50

- automated accepted-output coverage: **53.0%**
- abstention: **47.0%**
- unsupported-fact violation rate: **15.0%**

### t = 0.65

- automated accepted-output coverage: **52.0%**
- abstention: **48.0%**
- unsupported-fact violation rate: **14.5%**

The challenger therefore demonstrates that substantially higher automated development coverage was technically achievable while eliminating target-not-retrieved failures in the evaluated development population. However, because S1 never accessed the sealed confirmation data, these results cannot establish improved generalization.

Automatic ACCEPTED status in S1 must not be interpreted as human accept-as-is.

## 5. Overall interpretation

The experimental results support a layered conclusion.

First, conventional text-based ML models provided meaningful predictive performance for software-defect triage, particularly for the binary task, but one-shot confirmation exposed a substantial generalization gap relative to development estimates.

Second, the original Stage 3 documentation-generation pipeline demonstrated that generated outputs could often be factually correct, readable, and semantically complete when the required context was available. Its principal practical limitation was low end-to-end coverage, largely associated with retrieval availability, together with low human-rated usefulness/style fit and the absence of outputs that reviewers would accept unchanged.

Third, the post-hoc S1 challenger provides evidence that retrieval and generation design changes can materially improve development-stage coverage. Because this challenger was deliberately kept away from the confirmation population, it should be interpreted as evidence of a promising future direction rather than as a replacement for the frozen final estimates.

## 6. Thesis reporting rules

The primary headline results are the frozen Gate 5 classifier confirmation metrics and Gate 6 human evaluation.

Gate 4 may be used to describe development behavior and the development-to-confirmation transition.

S1 may be reported as a separate post-hoc experiment demonstrating potential improvements, but it must remain explicitly labeled development-only.

No S1 threshold should be presented as selected.

No automatic pipeline acceptance statistic should be described as equivalent to human accept-as-is.

## 7. Main limitations

1. Substantial development-to-confirmation generalization gaps were observed for both classifier tasks.
2. Gate 6 conditional human quality metrics are based on only 14 generated outputs.
3. The original Stage 3 system achieved only 14% system coverage on the primary natural-distribution sample.
4. Reference-based similarity metrics were unavailable in Gate 6.
5. The secondary category-stress sample is supplementary and was not pooled with the primary estimate.
6. S1 has no sealed confirmation evaluation and therefore cannot support claims of improved final-system generalization.
7. S1 operating thresholds remain intentionally unselected.

## Final evidence statement

The final experimental evidence is considered complete while preserving the distinction between development, one-shot confirmation, frozen human evaluation, and post-hoc development evidence.
