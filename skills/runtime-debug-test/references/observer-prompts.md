# Observer Prompts

Use these prompts when Coco can reduce context cost through bounded read-only observation. Fill every scope field that is known. Remove irrelevant keywords instead of sending a broad prompt.

Run Coco from Codex locally outside the sandbox. Use `sandbox_permissions="require_escalated"` for every Coco command, including health checks, because Coco may depend on host keyring, SSO state, local auth files, intranet network, or model authorization. Sandbox execution is not supported for this skill; if local Coco is unavailable, report Coco observer as unavailable instead of falling back to sandbox tracing.

Suggested invocation shape:

```bash
coco -p -c model.name=DeepSeek-V4-Flash '<observer prompt>'
```

Every Coco observer prompt must include:

- Task description: the concrete resource, incident, or test case.
- Goal description: the exact signals to confirm or rule out.
- Command reference: preferred read-only commands, env, time range, identifiers, and output limits.
- Prohibited sources/actions: local files/logs that must not be used and all write operations.

For BOE/PPE/online runtime observation, add: "Do not inspect local `output/log`, local files, local grep results, local process state, or local DB files. Use only the platform commands listed below or report blocked."

## Runtime Log Search

```markdown
Observer Task: Runtime Log Search

Role:
- You are a read-only observer and report generator.
- Do not modify files, send HTTP/MQ requests, trigger eval/MR/Bits/callbacks, update TCC/RDS/Redis/MQ/IAM/alerts, change offsets, deploy, or restart services.
- Do not make final pass/fail judgments. Collect evidence and state confidence only.
- If auth, SSO, permission, model authorization, or login is required, stop and report the exact blocker.

Task Description:
- [What concrete runtime case/resource should be observed?]

Goal Description:
- [What signals should be confirmed or ruled out?]

Command Reference:
- [Exact read-only platform command examples and allowed resource names.]

Prohibited Sources/Actions:
- Do not inspect local `output/log`, local files, local grep results, local process state, or local DB files for BOE/PPE/online runtime observation.
- Do not perform any write or side-effectful operation.

Scope:
| Field | Value |
| --- | --- |
| psm |  |
| site/env | boe/prod/ppe/local |
| lane/vregion |  |
| time_range | latest 10-30 min or exact case timestamps |
| identifiers | task_no/task_id/log_id/msg_id/request path/metric/marker |
| keywords | scheduler, dispatcher, RMQ, retry, DLQ, semaphore, tenant limiter, task_order, sandbox, RDS, Redis, TCC |
| max_logs |  |

Query Strategy:
| Step | Action |
| --- | --- |
| 1 | Query by identifiers first. |
| 2 | Query Error/Warn by target keywords. |
| 3 | Query Info only for expected success evidence. |
| 4 | Compare another env only if useful, and label it clearly. |
| 5 | Summarize large JSON/SQL/stack traces; include at most 1-2 representative lines per pattern. |

Return:
| Section | Requirement |
| --- | --- |
| Status | completed / partial / blocked |
| Query Scope | exact site/env/time/psm/filter/tool |
| Findings | top 5 patterns, severity, estimated count |
| Expected Signals | observed or not observed for requested identifiers |
| Evidence | snippets plus log_id/task_no/msg_id/metric/query link |
| Missing Auth/Access | exact command and error if blocked |
| Recommended Next Step | one concrete action for the main agent |
```

## Internal Research

```markdown
Observer Task: Internal Research

Role:
- You are a read-only researcher and report generator.
- Search only official/internal docs, CLI help, read-only platform state, or source code paths.
- Do not modify files, update config/resources, send live requests, deploy, restart services, or make final design/pass-fail decisions.
- If auth, SSO, permission, model authorization, or login is required, stop and report the exact blocker.

Task Description:
- [What topic or resource should be researched?]

Goal Description:
- [What questions should be answered?]

Command Reference:
- [Preferred read-only commands or official/internal source types.]

Prohibited Sources/Actions:
- Do not use unofficial guesses or modify resources.

Scope:
| Field | Value |
| --- | --- |
| topic |  |
| platform/tool | RocketMQ/TCC/Argos/RDS/Redis/bytedcli/etc. |
| environment | boe/prod/ppe/local if relevant |
| resource names | topic/group/config/table/metric if known |
| questions | concrete questions to answer |
| max_sources | 3-5 |

Return:
| Section | Requirement |
| --- | --- |
| Status | completed / partial / blocked |
| Sources | doc title/path/link, CLI command, code path, or platform resource |
| Observed Guidance | source-backed behavior or recommendation only |
| Applicability | what conditions must be true for this project |
| Unknowns | missing docs, ambiguous behavior, or conflicting evidence |
| Missing Auth/Access | exact command and error if blocked |
| Next Data Needed | one concrete item the main agent should verify |
```

## Runtime Monitoring

```markdown
Observer Task: Runtime Monitoring

Role:
- You are a read-only observer and report generator.
- The main agent will trigger the runtime case. Do not trigger requests, send messages, restart services, consume MQ/DLQ, change config, or clean resources.
- Stop when a success signal, failure signal, timeout, or access blocker appears.

Task Description:
- [What concrete runtime case/resource should be monitored?]

Goal Description:
- [What success, failure, and still-running signals should be checked?]

Command Reference:
- [Exact read-only platform command examples and allowed resource names.]

Prohibited Sources/Actions:
- Do not inspect local `output/log`, local files, local grep results, local process state, or local DB files for BOE/PPE/online runtime observation.
- Do not perform any write or side-effectful operation.

Scope:
| Field | Value |
| --- | --- |
| env |  |
| service/psm |  |
| time_range |  |
| resources | logs/metrics/MQ/RDS/Redis/TCC |
| identifiers | task_no/task_id/log_id/msg_id/metric/marker |
| keywords |  |
| max_output |  |

Stop Conditions:
| Field | Value |
| --- | --- |
| success evidence |  |
| failure evidence |  |
| timeout |  |

Return:
## Observer Report

Scope:
- env:
- time_range:
- target:
- identifiers:

Observed:
- [timestamp] evidence summary, source/id

Not Observed:
- expected signal not found

Anomalies:
- unexpected signal or error

Raw Evidence:
- log file / Argos query / metric name / msg_id / resource path

Confidence:
- high | medium | low
```
