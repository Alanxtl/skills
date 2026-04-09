# Result Comparison

## Goal

Judge the reproduction against the paper's main claims, not just against isolated headline numbers.

## Compare in This Order

1. Compare the main claim or contribution under test.
2. Compare the experimental conditions used to support that claim.
3. Compare the primary metrics, tables, or figures.
4. Compare secondary ablations, variants, or qualitative results only after the main claim is addressed.

## Align Conditions Before Numbers

Before calling a result matched or unmatched, check:

- dataset or benchmark version
- split definition
- evaluation script or metric definition
- hardware and runtime constraints
- model size, configuration, or build target
- seed count or variance handling

If conditions differ, explain the difference before discussing the metric delta.

## Verdict Labels

Use one of these verdicts in `validation_report.md`:

- Reproduced: the main claim is supported under comparable conditions
- Directionally reproduced: the trend or conclusion matches, but setup or numbers differ materially
- Inconclusive: the current evidence is not strong enough to judge
- Not reproduced: the current evidence contradicts the paper's main claim

## Common Sources of Deviation

- incomplete or inferred implementation detail
- missing artifact or environment mismatch
- reduced compute or dataset scope
- benchmark or metric mismatch
- random variation or insufficient reruns
- paper ambiguity or undocumented preprocessing

Explain which source is most likely and what next action would reduce uncertainty.

## Output Shape

Use `validation_report.md` to capture:

- the claim under test
- the paper-side evidence
- the reproduced evidence
- setup parity notes
- the verdict
- the most important deviations
- the next recommended check
