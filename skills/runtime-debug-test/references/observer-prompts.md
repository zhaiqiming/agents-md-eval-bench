# Observer Prompts

Use these prompts when TraeCLI can reduce context cost through bounded read-only observation. Fill every scope field that is known. Remove irrelevant keywords instead of sending a broad prompt.

Run every TraeCLI observer command locally outside the Codex sandbox with `sandbox_permissions="require_escalated"` and a narrow prefix rule such as `["traecli"]`. TraeCLI depends on host-local security context, credentials, and runtime state, so do not first try it inside the Codex sandbox. Keep TraeCLI's own execution mode read-only and non-persistent where possible. If local TraeCLI is unavailable, report TraeCLI observer as unavailable instead of falling back to broad tracing.

Always specify the model. Choose from this ordered list: `Test-O-New-Thinking`, `DeepSeek-V4-Pro`, `MiniMax-M2.7`, `GLM-5.1`. If TraeCLI reports that a model is unavailable, unauthorized, or unsupported, retry the same observer task once with the next model and report the fallback reason. Do not switch models for unrelated failures.

Suggested invocation shape. Use `-c "sandbox_read_only.network_access=true"` immediately after `--sandbox read-only` so read-only runtime observers can perform network-backed platform reads. Write the final response to a summary file and redirect stdout/stderr to a raw log; Codex should read the summary file first and inspect the raw log only when needed:

```bash
traecli exec -m <model> --sandbox read-only -c "sandbox_read_only.network_access=true" --ephemeral -o /tmp/runtime-observer-summary.md '<observer prompt>' >/tmp/runtime-observer-raw.log 2>&1
```

When the observer prompt includes `bytedcli`, log, metric, TCC, MQ, RDS, Redis, or other shell-based read-only commands, keep the prompt explicit that only read-only commands are allowed. If the current TraeCLI version needs tool allowlisting, use `--allowed-tool` narrowly for those read-only commands. The outer TraeCLI command still runs locally outside the Codex sandbox.

```bash
traecli exec -m <model> --sandbox read-only -c "sandbox_read_only.network_access=true" --ephemeral --allowed-tool 'Bash(bytedcli *:*)' -o /tmp/runtime-observer-summary.md '<observer prompt>' >/tmp/runtime-observer-raw.log 2>&1
```

If TraeCLI reports tool execution permission denied for a read-only platform command, retry once with a narrower `--allowed-tool` pattern before declaring the observer blocked. Do not use `--permission-mode bypass_permissions`, `--sandbox danger-full-access`, `-y`, or other yolo-style permission bypasses for observer work.

Every TraeCLI observer prompt must include:

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

## Runtime Snapshot

Use this for BOE/PPE/online runtime checks that need recent logs, metrics, MQ state, RDS state, Redis state, or TCC state. The observer must complete one bounded snapshot and return; it must not sleep, poll in a loop, or wait for future state changes.

```markdown
Observer Task: Runtime Snapshot

Role:
- You are a read-only observer and report generator.
- Complete exactly one bounded snapshot and return immediately.
- Do not run an internal loop, sleep between attempts, or keep watching after the first bounded query set.
- Do not modify files, send HTTP/MQ requests, trigger eval/MR/Bits/callbacks, update TCC/RDS/Redis/MQ/IAM/alerts, change offsets, deploy, or restart services.
- If auth, SSO, permission, model authorization, or login is required, stop and report the exact blocker.

Task Description:
- [What concrete runtime case/resource should be observed?]

Goal Description:
- [What current state or recent signals should be confirmed or ruled out?]

Command Reference:
- [Exact read-only platform command examples, env, time range, identifiers, and output limits.]

Prohibited Sources/Actions:
- Do not inspect local `output/log`, local files, local grep results, local process state, or local DB files for BOE/PPE/online runtime observation.
- Do not perform any write or side-effectful operation.

Scope:
| Field | Value |
| --- | --- |
| psm/service |  |
| site/env | boe/prod/ppe/local |
| lane/vregion |  |
| time_range | latest 10-30 min or exact case timestamps |
| identifiers | task_no/task_id/log_id/msg_id/request path/metric/marker |
| resources | logs/metrics/MQ/RDS/Redis/TCC |
| keywords |  |
| max_logs/max_rows |  |

Return:
| Section | Requirement |
| --- | --- |
| Status | completed / partial / blocked |
| Query Scope | exact site/env/time/psm/filter/tool |
| Current State | latest observed state with timestamp |
| Evidence | snippets plus log_id/task_no/msg_id/metric/query link/resource path |
| Not Observed | expected signal not found in this snapshot |
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
- Complete one bounded monitoring snapshot and return. Do not run internal long-polling loops; the main agent owns repeat cadence and stop decisions.

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
| main-agent timeout |  |

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
