---
name: reproduce-papers
description: Plan and execute reproducible computer science paper reproductions. Use when Codex needs to extract implementation-critical details from a paper, inventory required artifacts and environments, build a runnable draft reproduction, track missing details and deviations, compare reproduced results with the paper, or package the work into reusable experiment notes.
---

# Reproduce Papers

## Overview

Use this skill to turn a paper into a traceable reproduction workflow. Move from paper reading to artifact inventory, runnable draft implementation, gap tracking, and result comparison without waiting for every missing detail to be resolved.

## Workflow Router

- If the user needs reproduction-critical details from the paper, read `references/paper-reading.md`.
- If the user needs to inventory code, data, weights, binaries, dependencies, hardware, or benchmark assets, read `references/artifact-and-environment.md`.
- If the user needs a runnable first-pass reproduction before exact fidelity, read `references/draft-first-reproduction.md`.
- If the user is blocked by missing details, approximations, or deviations, read `references/gap-tracking.md`.
- If the user needs to compare reproduced results with the paper, read `references/result-comparison.md`.

Use multiple references only when the request spans multiple stages.

## Core Workflow

1. Identify the current stage: paper reading, artifact inventory, draft reproduction, gap resolution, or result comparison.
2. Extract reproduction-critical details first: problem definition, inputs and outputs, system boundaries, core method, training or runtime conditions, evaluation protocol, and reported metrics.
3. Build the smallest runnable draft once the minimum end-to-end path is clear. Do not wait for every hyperparameter or systems detail to be known.
4. Record every unknown, approximation, deviation, and evidence source in `gap_tracker.md`.
5. Compare reproduced results against the paper's main tables, figures, or claims. Explain whether the central conclusion reproduced, not only whether every number matched exactly.

## Working Rules

- Treat the paper as the primary source of truth. Use the appendix, supplementary material, cited work, benchmark documentation, and official repositories only when the paper leaves a critical gap.
- Do not wait for perfect fidelity before building a baseline.
- Keep plans framework-neutral unless the paper or repository forces a specific stack.
- Prefer explicit assumptions over silent guessing.
- Preserve traceability. When you infer or substitute something, state why it is reasonable and where it should be verified.
- When the paper is not training-centered, reinterpret the runnable draft as the smallest executable evaluation path, benchmark harness, detector pass, or system prototype that still exercises the paper's core claim.

## Standard Workspace

Initialize a new case with:

```bash
python scripts/init_repro_case.py --title "Paper Title" --slug paper-slug --out ./cases
```

This creates `<out>/<slug>/` with:
- `paper_brief.md`
- `artifact_inventory.md`
- `implementation_plan.md`
- `gap_tracker.md`
- `experiment_log.csv`
- `validation_report.md`

Template files live under `assets/templates/`. Use them as scaffolding for the reproduction effort rather than as final polished documentation.

## Expected Outputs

- A concise paper brief with the reproduction-critical facts.
- An artifact and environment inventory.
- A runnable draft reproduction plan.
- A gap tracker with assumptions, impacts, and next actions.
- A validation report that compares reproduced findings with the paper's main claims.
