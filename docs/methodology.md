# Evaluation Methodology

## Goal

Compare whether a candidate `AGENTS.md` improves agent task outcomes relative to a baseline instruction file.

## Context

Instruction files can affect different dimensions of agent behavior. A concise engineering rule set may improve small implementation tasks, while a context-first rule set may improve analysis and documentation tasks that need evidence and uncertainty handling.

## Constraints

- Use the same task prompt, repository fixture, model, tool availability, and time budget for every variant.
- Record observable outcomes instead of subjective impressions.
- Keep scoring criteria stable across runs.
- Treat sample results as pipeline fixtures only, not benchmark evidence.

## Completion Standard

An evaluation run is complete when every variant has one result entry for every task in `eval/tasks.json`, the evaluator exits successfully, and the summary reports aggregate scores plus deltas against the selected baseline.

## Evidence Capture

Use concrete evidence references in result notes when possible:

| Evidence Type | Example |
| --- | --- |
| File path | `src/service.py` |
| Test command | `pytest tests/test_service.py` |
| Config key | `feature.newCheckout.enabled` |
| Runtime artifact | Log ID, screenshot path, generated report |

## Interpreting Deltas

| Delta | Meaning |
| ---: | --- |
| `> 5` | Candidate likely improves this task mix. |
| `-5` to `5` | Difference is small; inspect per-task behavior before concluding. |
| `< -5` | Candidate likely hurts this task mix or mismatches the task type. |

The threshold is intentionally conservative for early versions. Increase confidence with repeated runs, more task fixtures, and blind scoring.

