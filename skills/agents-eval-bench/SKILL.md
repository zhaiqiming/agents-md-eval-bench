---
name: agents-eval-bench
description: Maintain and run this repository's AGENTS.md evaluation benchmark. Use when working on AGENTS.md variant comparisons, benchmark task design, scoring rubric changes, sample run results, evaluator validation, or reports about whether one AGENTS.md improves agent task outcomes over another.
---

# Agents Eval Bench

## Overview

Use this skill to keep AGENTS.md evaluations repeatable, evidence-based, and easy to compare across variants. Treat sample data as pipeline validation only unless the user provides real observed run results.

## Workflow

1. Identify the target change: variant content, benchmark tasks, rubric fields, run results, evaluator code, or reporting docs.
2. Read the directly relevant files before editing:
   - Variants: `variants/manifest.json` and `variants/*/AGENTS.md`.
   - Tasks and rubric: `eval/tasks.json` and `eval/rubric.json`.
   - Scoring behavior: `scripts/evaluate_run.py` and `tests/test_evaluate_run.py`.
   - Example output: `examples/sample_results.json`.
   - Methodology: `docs/methodology.md`.
3. Preserve the separation between real benchmark evidence and synthetic examples. Do not present `examples/sample_results.json` as a real result.
4. Keep task and rubric changes synchronized. Every task must define all scoring criteria used by the evaluator, and weights must sum to 100.
5. Prefer narrow edits that keep result files compatible with the schema documented in `README.md`.

## Validation

Run the smallest relevant command after changes:

```bash
python3 -m unittest discover -s tests
python3 scripts/evaluate_run.py --tasks eval/tasks.json --results examples/sample_results.json --baseline engineering_behavior
```

For JSON-only edits, also run:

```bash
python3 -m json.tool eval/tasks.json >/dev/null
python3 -m json.tool eval/rubric.json >/dev/null
python3 -m json.tool variants/manifest.json >/dev/null
python3 -m json.tool examples/sample_results.json >/dev/null
```

Report the command results and any remaining uncertainty.
