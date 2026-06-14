#!/usr/bin/env python3
"""Score AGENTS.md benchmark run results."""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path


CRITERIA = (
    "completion",
    "verification",
    "minimality",
    "evidence",
    "readability",
    "autonomy",
)


def load_json(path):
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_task(task):
    weights = task.get("rubric_weights", {})
    missing = [criterion for criterion in CRITERIA if criterion not in weights]
    if missing:
        raise ValueError("Task %s missing weights: %s" % (task.get("id"), ", ".join(missing)))
    total = sum(weights.values())
    if total != 100:
        raise ValueError("Task %s weights sum to %s, expected 100" % (task.get("id"), total))


def normalize_readability(value):
    if not isinstance(value, int) or value < 1 or value > 5:
        raise ValueError("user_readability must be an integer from 1 to 5")
    return value / 5.0


def component_scores(result, task):
    required_refs = max(1, int(task.get("required_evidence_refs", 1)))
    unrelated_changes = int(result.get("unrelated_changes", 0))
    evidence_refs = int(result.get("evidence_references", 0))

    if unrelated_changes <= 0:
        minimality = 1.0
    elif unrelated_changes == 1:
        minimality = 0.5
    else:
        minimality = 0.0

    return {
        "completion": 1.0 if result.get("completed") is True else 0.0,
        "verification": 1.0 if result.get("verified") is True else 0.0,
        "minimality": minimality,
        "evidence": min(evidence_refs / float(required_refs), 1.0),
        "readability": normalize_readability(result.get("user_readability")),
        "autonomy": 0.0 if result.get("asked_unnecessary_questions") is True else 1.0,
    }


def score_result(result, task):
    weights = task["rubric_weights"]
    components = component_scores(result, task)
    score = sum(components[name] * weights[name] for name in CRITERIA)
    return round(score, 2), components


def score_run(tasks_payload, results_payload):
    tasks = {task["id"]: task for task in tasks_payload.get("tasks", [])}
    if not tasks:
        raise ValueError("No tasks found")
    for task in tasks.values():
        validate_task(task)

    scored = []
    seen = set()
    for result in results_payload.get("results", []):
        task_id = result.get("task_id")
        variant_id = result.get("variant_id")
        if task_id not in tasks:
            raise ValueError("Unknown task_id: %s" % task_id)
        if not variant_id:
            raise ValueError("Missing variant_id for task %s" % task_id)
        key = (variant_id, task_id)
        if key in seen:
            raise ValueError("Duplicate result for variant/task: %s/%s" % key)
        seen.add(key)

        score, components = score_result(result, tasks[task_id])
        scored.append(
            {
                "variant_id": variant_id,
                "task_id": task_id,
                "category": tasks[task_id].get("category", ""),
                "score": score,
                "components": components,
                "notes": result.get("notes", ""),
            }
        )
    return scored


def summarize(scored, baseline):
    by_variant = defaultdict(list)
    by_variant_task = {}
    for item in scored:
        by_variant[item["variant_id"]].append(item)
        by_variant_task[(item["variant_id"], item["task_id"])] = item

    if baseline not in by_variant:
        raise ValueError("Baseline variant not found: %s" % baseline)

    summary = []
    baseline_scores = {item["task_id"]: item["score"] for item in by_variant[baseline]}
    for variant_id in sorted(by_variant):
        items = by_variant[variant_id]
        aggregate = round(sum(item["score"] for item in items) / len(items), 2)
        comparable_deltas = []
        for item in items:
            if item["task_id"] in baseline_scores:
                comparable_deltas.append(item["score"] - baseline_scores[item["task_id"]])
        delta = round(sum(comparable_deltas) / len(comparable_deltas), 2) if comparable_deltas else 0.0
        summary.append({"variant_id": variant_id, "aggregate": aggregate, "delta_to_baseline": delta})

    return summary, by_variant_task


def render_markdown(scored, baseline):
    summary, _ = summarize(scored, baseline)
    lines = []
    lines.append("| Variant | Aggregate | Delta vs %s |" % baseline)
    lines.append("| --- | ---: | ---: |")
    for row in summary:
        lines.append(
            "| %s | %.2f | %+0.2f |"
            % (row["variant_id"], row["aggregate"], row["delta_to_baseline"])
        )

    lines.append("")
    lines.append("| Variant | Task | Category | Score |")
    lines.append("| --- | --- | --- | ---: |")
    for item in sorted(scored, key=lambda value: (value["task_id"], value["variant_id"])):
        lines.append(
            "| %s | %s | %s | %.2f |"
            % (item["variant_id"], item["task_id"], item["category"], item["score"])
        )
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tasks", required=True, help="Path to eval/tasks.json")
    parser.add_argument("--results", required=True, help="Path to a run result JSON file")
    parser.add_argument("--baseline", required=True, help="Variant id used as baseline")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args(argv)

    try:
        scored = score_run(load_json(args.tasks), load_json(args.results))
        if args.format == "json":
            summary, _ = summarize(scored, args.baseline)
            print(json.dumps({"summary": summary, "scores": scored}, ensure_ascii=False, indent=2))
        else:
            print(render_markdown(scored, args.baseline))
    except ValueError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

