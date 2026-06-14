# AGENTS.md 评测基准

[English](README.md)

本仓库用于评测不同 `AGENTS.md` 指令对 agent 任务结果的影响。

首个评测版本包含两个指令变体：

- `engineering_behavior`：英文工程行为规则，强调最小改动、行为兼容和验证自动化。
- `context_first_cn`：中文上下文优先规则，覆盖任务启动、实施验证、分析任务和文档写作。

## 仓库结构

| 路径 | 用途 |
| --- | --- |
| `variants/` | 候选 `AGENTS.md` 文件和变体元数据。 |
| `eval/tasks.json` | 评测任务集和每个任务的评分权重。 |
| `eval/rubric.json` | 通用评分字段定义和打分说明。 |
| `scripts/evaluate_run.py` | 对一次运行结果打分，并与基线变体对比。 |
| `examples/sample_results.json` | 用于验证评分链路的合成样例结果。 |
| `skills/agents-eval-bench/` | 维护和运行本评测基准的项目内 skill。 |
| `tests/` | 评分器单元测试。 |

## 评测流程

1. 对每个 `AGENTS.md` 变体运行同一组任务。
2. 按 `examples/sample_results.json` 使用的结果 schema 记录观察到的任务表现。
3. 执行评分：

```bash
python3 scripts/evaluate_run.py \
  --tasks eval/tasks.json \
  --results examples/sample_results.json \
  --baseline engineering_behavior
```

4. 对比聚合分和逐任务差异。

评分器本身不负责运行 agent。它只提供稳定的评分层，agent 执行可以由人工、Codex 线程或后续自动化 runner 完成。

## 结果 Schema

每条结果记录一个变体在一个任务上的表现：

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

## 本地验证

```bash
python3 -m unittest discover -s tests
python3 scripts/evaluate_run.py --tasks eval/tasks.json --results examples/sample_results.json --baseline engineering_behavior
```

## GitHub 仓库

当前仓库已推送到 GitHub：

[zhaiqiming/agents-md-eval-bench](https://github.com/zhaiqiming/agents-md-eval-bench)

如需重新创建远端仓库，需要先确认 owner、仓库名和可见性，再执行类似命令：

```bash
gh repo create <owner>/<repo> --private --source=. --remote=origin --push
```
