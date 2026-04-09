# Artifact and Environment Inventory

## Goal

Inventory every artifact and execution dependency required to reproduce the paper before implementation drifts too far from reality.

## Inventory Categories

Review these categories and record the status of each item in `artifact_inventory.md`:

- Source code or official repositories
- Released checkpoints, pretrained weights, binaries, or packaged artifacts
- Datasets, splits, preprocessing scripts, or synthetic data generators
- Configuration files, command-line entry points, and seed handling
- Language runtimes, compiler versions, libraries, frameworks, and drivers
- Operating system, container images, hardware, memory, and storage expectations
- External services, APIs, databases, or benchmark harnesses
- Evaluation scripts, scoring code, workload generators, or trace replay tools

## Questions to Answer

- Is there an official implementation or only paper text?
- Which artifacts are mandatory for the first runnable draft?
- Which artifacts are optional but needed for higher fidelity?
- Which items are unavailable, restricted, or expensive to recreate?
- Which environment details can materially affect results?

## Domain-Specific Reminders

- For machine learning papers, capture dataset versions, split definitions, feature preprocessing, checkpoint formats, and accelerator requirements.
- For systems papers, capture build toolchains, deployment topology, traffic generators, benchmark harnesses, and machine specifications.
- For security papers, capture threat-model assumptions, sandboxing requirements, traces, malicious samples, safe execution constraints, and detector or attack tooling.

## Minimal Runnable Path

After the inventory, identify the shortest end-to-end path that can produce one paper-like output:

- one training or inference run
- one benchmark execution
- one analysis pass
- one attack or defense evaluation

Do not inventory forever. Inventory until you know what is available, what is missing, and what must be approximated for the first real run.

## Escalate Missing Items

If any required artifact or environment detail is missing:

1. Record it in `gap_tracker.md`.
2. State the current workaround or assumption.
3. Estimate whether the gap blocks execution or only affects fidelity.
