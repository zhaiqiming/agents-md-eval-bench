import unittest

from scripts.evaluate_run import score_run, summarize


TASKS = {
    "tasks": [
        {
            "id": "task-a",
            "category": "implementation",
            "required_evidence_refs": 2,
            "rubric_weights": {
                "completion": 25,
                "verification": 25,
                "minimality": 20,
                "evidence": 15,
                "readability": 10,
                "autonomy": 5,
            },
        }
    ]
}


class EvaluateRunTest(unittest.TestCase):
    def test_scores_full_credit_result(self):
        scored = score_run(
            TASKS,
            {
                "results": [
                    {
                        "variant_id": "base",
                        "task_id": "task-a",
                        "completed": True,
                        "verified": True,
                        "unrelated_changes": 0,
                        "evidence_references": 2,
                        "user_readability": 5,
                        "asked_unnecessary_questions": False,
                    }
                ]
            },
        )

        self.assertEqual(scored[0]["score"], 100.0)

    def test_scores_partial_credit_result(self):
        scored = score_run(
            TASKS,
            {
                "results": [
                    {
                        "variant_id": "base",
                        "task_id": "task-a",
                        "completed": True,
                        "verified": False,
                        "unrelated_changes": 1,
                        "evidence_references": 1,
                        "user_readability": 3,
                        "asked_unnecessary_questions": True,
                    }
                ]
            },
        )

        self.assertEqual(scored[0]["score"], 48.5)

    def test_summary_delta_to_baseline(self):
        scored = score_run(
            TASKS,
            {
                "results": [
                    {
                        "variant_id": "base",
                        "task_id": "task-a",
                        "completed": True,
                        "verified": False,
                        "unrelated_changes": 0,
                        "evidence_references": 2,
                        "user_readability": 5,
                        "asked_unnecessary_questions": False,
                    },
                    {
                        "variant_id": "candidate",
                        "task_id": "task-a",
                        "completed": True,
                        "verified": True,
                        "unrelated_changes": 0,
                        "evidence_references": 2,
                        "user_readability": 5,
                        "asked_unnecessary_questions": False,
                    },
                ]
            },
        )

        summary, _ = summarize(scored, "base")
        by_variant = {row["variant_id"]: row for row in summary}
        self.assertEqual(by_variant["candidate"]["delta_to_baseline"], 25.0)


if __name__ == "__main__":
    unittest.main()

