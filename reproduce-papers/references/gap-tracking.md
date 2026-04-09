# Gap Tracking

## Goal

Track every missing detail, approximation, and deviation so the reproduction stays auditable and the next step is always clear.

## Gap Categories

Use these categories consistently:

- Missing implementation detail
- Missing environment detail
- Data unavailable
- Resource constraint
- Incomplete evaluation protocol
- Result not directly alignable

## Required Fields for Each Gap

Every entry in `gap_tracker.md` must include:

- A stable ID
- The category
- The missing detail or deviation
- The current assumption or workaround
- The evidence source
- The expected impact
- The next verification action
- The current status

Add a risk label when it helps prioritize work.

## Logging Rules

- Log the gap before relying on a workaround.
- Distinguish unknown information from deliberate simplification.
- Update the same row when the gap changes status instead of duplicating it.
- Keep the evidence source specific enough to revisit later.

## Prioritize the Right Gaps

Treat these as highest priority:

- gaps that block any runnable path
- gaps that can invalidate the paper's main claim
- gaps that change metric definitions or evaluation conditions
- gaps that make a comparison unfair

Treat cosmetic or low-impact gaps as lower priority unless the user asks for publication-grade parity.

## Close a Gap Only When

- the missing detail is confirmed from a trusted source, or
- the reproduction no longer depends on that gap, and the reason is documented

Never close a gap just because the current run happened to succeed.
