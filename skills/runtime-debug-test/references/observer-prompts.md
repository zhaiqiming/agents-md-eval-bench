# Observer Prompts

Use these prompts when TraeCLI can reduce context cost through bounded read-only observation. Fill every scope field that is known. Remove irrelevant keywords instead of sending a broad prompt.

Run TraeCLI observer commands from the local Codex shell. Do not pass Codex `sandbox_permissions` unless the active runtime explicitly supports and requires it. TraeCLI remains a read-only observer/researcher and must not write config, send requests, send MQ messages, mutate DB/Redis, deploy, restart, clean resources, or make final pass/fail judgments.

Always specify the model with `-c model.name=<model>`. Choose from this ordered list: `Test-O-New-Thinking`, `DeepSeek-V4-Pro`, `MiniMax-M2.7`, `GLM-5.1`. If TraeCLI reports that a model is unavailable, unauthorized, or unsupported, retry the same observer task once with the next model and report the fallback reason. Do not switch models for unrelated failures.

Suggested invocation shape for current TraeCLI versions. Write stdout to a summary file and stderr to a raw log; Codex should read the summary file first and inspect the raw log only when needed:

```bash
traecli -c model.name=<model> -p --output-format text --query-timeout 5m --allowed-tool Bash '<observer prompt>' >/tmp/runtime-observer-summary.md 2>/tmp/runtime-observer-raw.log
```

Do not use the older `traecli exec`, `-m`, `--sandbox`, `--ephemeral`, or `-o` shape unless `traecli --help` proves those flags exist in the installed version.

When the observer prompt includes `bytedcli`, log, metric, TCC, MQ, RDS, Redis, or other shell-based platform commands, use `--allowed-tool` as narrowly as practical only if the installed TraeCLI accepts that syntax. If `Bash(bytedcli *:*)` or similar patterns are denied, use `--allowed-tool Bash` and constrain the prompt to read-only `bytedcli` or local processing commands. Conclusions from local processing must include the raw snippets that support them.

For prompts that ask TraeCLI to run `bytedcli` or another read-only platform CLI, explicitly state that the outer invocation grants shell execution only so the observer can run read-only commands. The observer must attempt the listed read-only command before reporting blocked. Blocked status requires a concrete command result such as auth required, command not found, network failure, permission denied, unsupported model, or tool-denied.

If TraeCLI reports tool execution permission denied for a read-only platform command, retry once with `--allowed-tool Bash` before declaring the observer blocked. Do not use `--permission-mode bypass_permissions`, `-y`, or other yolo-style permission bypasses for observer work.

Every TraeCLI observer prompt must include:

- Task description: the concrete resource, incident, or test case.
- Goal description: the exact signals to confirm or rule out.
- Command reference: preferred read-only commands, env, time range, identifiers, and output limits.
- Prohibited sources/actions: local files/logs that must not be used and all write operations.
- Evidence requirement: every conclusion from log, metric, or raw-output processing must include representative raw snippets and identifiers.
- Early return rule: if enough evidence exists to answer the goal, stop querying and return the summary immediately.
- Assigned-scope rule: if this is one task in a parallel fan-out, observe only the assigned window, task ID, resource, or question; do not expand into neighboring scopes.

For BOE/PPE/online runtime observation, add: "Do not inspect local `output/log`, local files, local grep results, local process state, or local DB files. Use only the platform commands listed below or report blocked."

## Runtime Log Search

```markdown
Observer Task: Runtime Log Search

Role:
- You are a read-only observer and report generator.
- Do not modify files, send HTTP/MQ requests, trigger eval/MR/Bits/callbacks, update TCC/RDS/Redis/MQ/IAM/alerts, change offsets, deploy, or restart services.
- Do not make final pass/fail judgments. Collect evidence and state confidence only.
- The outer TraeCLI invocation grants shell execution only so you can run the listed read-only commands. You remain read-only and must run only those commands, plus bounded local processing of collected raw output when needed.
- Every finding or conclusion derived from raw logs must include representative raw snippets and identifiers.
- Report blocked only when an actual command execution returns auth, network, permission, command, model, or tool-denied error.
- If enough evidence exists to answer the goal, stop querying and return immediately with an evidence-backed summary.
- If this task is part of a parallel fan-out, observe only the assigned window, task ID, or resource; do not expand into neighboring scopes.
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
| Raw Snippet Basis | raw lines or short excerpts supporting each conclusion |
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
- The outer TraeCLI invocation grants shell execution only so you can run the listed read-only commands. You remain read-only and must run only those commands, plus bounded local processing of collected raw output when needed.
- Every finding or conclusion derived from raw logs must include representative raw snippets and identifiers.
- Report blocked only when an actual command execution returns auth, network, permission, command, model, or tool-denied error.
- If enough evidence exists to answer the goal, stop querying and return immediately with an evidence-backed summary.
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
| Raw Snippet Basis | raw lines or short excerpts supporting each conclusion |
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
- When command references are provided and the outer invocation allowlists them, attempt those read-only commands before reporting blocked.
- The outer TraeCLI invocation grants shell execution only so you can run the listed read-only commands. You remain read-only and must run only those commands, plus bounded local processing of collected raw output when needed.
- Every finding or conclusion derived from raw logs or source snippets must include representative raw snippets and identifiers.
- Report blocked only when an actual command execution returns auth, network, permission, command, model, or tool-denied error.
- If enough evidence exists to answer the goal, stop querying and return immediately with an evidence-backed summary.
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
| Raw Snippet Basis | source excerpts or command output snippets supporting each conclusion |
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
- Observe only the assigned bounded window. Do not poll future time, sleep, or extend the window.
- The outer TraeCLI invocation grants shell execution only so you can run the listed read-only commands. You remain read-only and must run only those commands, plus bounded local processing of collected raw output when needed.
- Every finding or conclusion derived from raw logs must include representative raw snippets and identifiers.
- Report blocked only when an actual command execution returns auth, network, permission, command, model, or tool-denied error.
- If enough evidence exists to answer the goal, stop querying and return immediately with an evidence-backed summary.

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
| window_index | latest 0-10 min / latest 10-20 min / exact interval |
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
