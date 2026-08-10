# Research Reframing 2026-08

Thesis title remains: "Inteligentni NLP agent za analizu konzistentnosti softverskih projekata"

## Proposed Research Questions

RQ1: Can an NLP-based agent detect whether a code change requires documentation or comment update?

RQ2: How does performance differ between controlled synthetic DocGuard data and real-world mined code-documentation change data?

RQ3: Can the trained model be integrated into a developer workflow, e.g. a VS Code extension, to provide actionable documentation update suggestions?

## Repositioning Existing Work

- Synthetic DocGuard v0.4 becomes the controlled prototype benchmark.
- External dataset validation becomes necessary for credible evaluation.
- VS Code extension v0.5 remains a practical demonstration/proof of applicability.

## What We Are Not Discarding

The synthetic dataset, HF classifier, hybrid router, runtime, figures, and extension work remain useful. The change is methodological: strong synthetic results are not enough. They must be tested against real-world mined data before being treated as thesis-level evidence.

## Stronger Thesis Structure

1. Controlled benchmark: synthetic DocGuard v0.4.
2. External benchmark: CoDocBench or comment-update dataset mapped to a normalized schema.
3. Practical artifact: VS Code extension using the runtime and classifier/router pipeline.

