# Paper Reading

## Goal

Extract enough detail to reproduce the paper without turning reading into unstructured note taking.

## Read in This Order

1. Read the abstract and introduction to identify the problem, main claim, and target outputs.
2. Read the method, approach, or system design section to capture the core pipeline, components, interfaces, and stated assumptions.
3. Read the experimental setup, implementation details, and evaluation sections to capture datasets, benchmarks, baselines, metrics, and execution conditions.
4. Read the appendix or supplementary material only when a critical implementation detail is still missing.
5. Check the official repository, released artifacts, or cited work only after exhausting the paper itself.

Do not start with Related Work unless it is the only place that defines a reused subsystem.

## Extract These Fields

- Problem definition and task boundary
- Inputs and outputs
- Core method or system pipeline
- Key algorithms, equations, pseudocode, or modules
- Training conditions, runtime conditions, or deployment assumptions
- Evaluation protocol and reported metrics
- Main tables, figures, or claims worth reproducing
- Explicit limitations, ablations, or failure cases

## Separate Facts From Inference

For every important detail, label it as one of:

- Confirmed in the paper
- Confirmed in supplementary or official artifacts
- Inferred from context
- Still unknown

Do not mix inferred defaults into the fact summary.

## Adapt the Reading to the Paper Type

- For machine learning papers, focus on model structure, data preparation, losses, optimization, and evaluation splits.
- For systems papers, focus on architecture, runtime topology, workloads, build steps, measurement methodology, and hardware assumptions.
- For security papers, focus on the threat model, attack or defense pipeline, environment setup, corpus or traces, and evaluation harness.

## Stop Condition

You are ready to move on when you can answer all of these:

- What is the smallest meaningful claim to reproduce?
- What are the paper's main inputs, outputs, and execution stages?
- Which details are confirmed?
- Which details are still missing and must be tracked separately?

Record the answer in `paper_brief.md`.
