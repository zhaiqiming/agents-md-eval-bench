# AGENTS.md Evaluation Bench

[中文说明](README.zh-CN.md)

This repository evaluates how different `AGENTS.md` instructions affect agent task outcomes.

The first benchmark version contains two instruction variants:

- `engineering_behavior`: concise English engineering behavior rules.
- `context_first_cn`: Chinese context-first rules covering task startup, validation, analysis, and documentation.

## Repository Layout

| Path | Purpose |
| --- | --- |
| `variants/` | Candidate `AGENTS.md` files and variant metadata. |
| `eval/tasks.json` | Benchmark task set and per-task rubric weights. |
| `eval/rubric.json` | Shared field definitions and scoring notes. |
| `scripts/evaluate_run.py` | Scores one run result file and compares variants against a baseline. |
| `examples/sample_results.json` | Synthetic example results for validating the pipeline. |
| `skills/agents-eval-bench/` | Project-local skill for maintaining and running this benchmark. |
| `tests/` | Unit tests for the evaluator. |

## Evaluation Flow

1. Run the same task set once per `AGENTS.md` variant.
2. Record observed outcomes in the result JSON schema used by `examples/sample_results.json`.
3. Score the run:

```bash
python3 scripts/evaluate_run.py \
  --tasks eval/tasks.json \
  --results examples/sample_results.json \
  --baseline engineering_behavior
```

4. Compare the aggregate score and per-task deltas.

The evaluator does not run an agent by itself. It provides a stable scoring layer so agent execution can be done manually, by Codex threads, or by a future automation runner.

## Result Schema

Each result item records one variant's outcome on one task:

```json
{
  "variant_id": "context_first_cn",
  "task_id": "doc-evidence-update",
  "completed": true,
  "verified": true,
  "unrelated_changes": 0,
  "evidence_references": 4,
  "user_readability": 5,
  "asked_unnecessary_questions": false,
  "notes": "Optional short observation."
}
```

## Local Validation

```bash
python3 -m unittest discover -s tests
python3 scripts/evaluate_run.py --tasks eval/tasks.json --results examples/sample_results.json --baseline engineering_behavior
```

## GitHub Setup

The repository is initialized locally with GitHub Actions CI. To create a remote GitHub repository, choose the owner, name, and visibility first, then run a command such as:

```bash
gh repo create <owner>/<repo> --private --source=. --remote=origin --push
```
