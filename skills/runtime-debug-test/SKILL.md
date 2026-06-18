---
name: runtime-debug-test
description: Plan and execute runtime debug/test work after backend changes. Use when Codex must validate local or BOE/PPE service behavior, construct runtime test data, inspect TCC/local config/MQ/MySQL/Redis dependencies, start services, send real test requests, trace logs/metrics, coordinate TraeCLI as a read-only observer, maintain project-local runtime lessons, or produce a runtime test report.
---

# Runtime Debug/Test

## Operating Principle

Move from "what changed" to reproducible runtime evidence.

Run the work in two phases:

1. Plan and dependency readiness.
2. Runtime execution, observation, cleanup, and report.

Do not jump directly to curl examples. First understand the feature, enumerate dependencies, classify side effects, and verify that the runtime can be started and observed.

## Ownership Model

The main agent owns runtime safety and final judgment. It designs the test plan, executes any side-effectful action, starts or stops services, sends requests or messages, changes config/resources, performs cleanup, and decides pass/fail.

Within this skill, TraeCLI is restricted to bounded read-only observer or researcher work when it reduces context cost. TraeCLI can search logs, metrics, Argos, read-only MQ/RDS/Redis/TCC state, internal docs, or source paths. This restriction is local to `runtime-debug-test` and does not change TraeCLI's behavior in other contexts. In this skill, TraeCLI must not execute real requests, send MQ messages, update config or data, change offsets, deploy, restart services, edit files, clean resources, or make final pass/fail decisions.

For BOE/PPE/online logs, metrics, multi-task tracing, multi-window巡检, and internal best-practice research, delegate to TraeCLI first whenever `traecli` is available and the needed auth/network is ready. The main agent should query platforms directly only when TraeCLI is unavailable, blocked, incomplete, internally inconsistent, or when a narrow second check is needed to verify a critical conclusion. Record the delegation outcome before any fallback query.

Do not ask TraeCLI to run internal long-polling loops. For long-running observation or巡检, split observation into bounded newest-first windows instead of one broad query: window 1 latest 0-10 min, window 2 latest 10-20 min, and window 3 latest 20-30 min only if needed. Each delegated TraeCLI task observes exactly one window and returns; the main agent decides whether another window is needed. Independent windows or independent task IDs may be delegated to multiple TraeCLI processes in parallel when the platform query is bounded and each process has a unique summary/raw output path. Keep parallel fan-out small, normally at most 3 observers, and stop parallel delegation if auth, rate-limit, permission, or inconsistent-evidence failures appear. If TraeCLI snapshots are unavailable or repeatedly incomplete, report long-running tracing as unavailable or blocked; do not replace it with main-agent long-cycle log/metric/trace polling, broad historical tracing, or extended platform observation.

Accept TraeCLI output only when it includes evidence identifiers such as `task_no`, `task_id`, `msg_id`, `log_id`, metric name, query link, resource name/version, or source path. Conclusions produced from log or metric processing must include representative raw evidence snippets that support the conclusion. If identifiers or raw snippets are missing, ask for a narrower follow-up or treat the output as low confidence.

Run every TraeCLI command from Codex locally with `sandbox_permissions="require_escalated"` and a narrow prefix such as `["traecli"]`; do not try TraeCLI inside the Codex sandbox first.

Before first TraeCLI delegation in a session, check availability locally without triggering a real runtime action:

```bash
command -v traecli
traecli --version
traecli login status
```

Always specify the TraeCLI observer model explicitly. Choose from this ordered list: `Test-O-New-Thinking`, `DeepSeek-V4-Pro`, `MiniMax-M2.7`, `GLM-5.1`. If a model is unavailable, unauthorized, or unsupported, retry the same observer task once with the next model and report the fallback reason. Do not switch models for other failures such as sandbox, auth, network, or tool permission errors.

Run TraeCLI observer work with `--sandbox danger-full-access` so it can use host-local sec, internal network, credentials, and runtime state. This is process capability, not write permission: TraeCLI remains a read-only observer/researcher and must not execute real requests, send MQ messages, update config or data, change offsets, deploy, restart services, edit files, clean resources, or make final pass/fail decisions. Always write the final response to a summary file and redirect stdout/stderr to a raw log so Codex reads only the summary by default:

```bash
traecli exec -m <model> --sandbox danger-full-access --ephemeral --allowed-tool 'Bash(bytedcli *:*)' -o /tmp/runtime-observer-summary.md '<observer prompt>' >/tmp/runtime-observer-raw.log 2>&1
```

Prefer a task-specific read-only `--allowed-tool` pattern for platform queries. Use `--allowed-tool 'Bash(bytedcli *:*)'` only when necessary, and then make the prompt explicitly allow only read-only subcommands. Broader shell access is allowed only for local processing of already-collected raw logs or command output. Do not use `--permission-mode bypass_permissions`, `-y`, or other yolo-style permission bypasses for runtime observation.

TraeCLI wait budgets are owned by the main agent:

- Short-window log or metric snapshot: wait up to 180 seconds for the summary file.
- Single task trace with known identifiers: wait up to 300 seconds.
- Internal research or best-practice lookup: wait up to 300 seconds.
- If the budget is exhausted, interrupt TraeCLI and inspect only the last 100 lines of the raw log to classify blocker or progress. Do not read the full raw log into context. If raw output contains enough evidence but no summary, run a narrow summary-only observer task or rerun with a narrower query.

Treat local TraeCLI health-check results explicitly:

- Local TraeCLI succeeds: use TraeCLI for bounded read-only observer tasks.
- Local TraeCLI fails with auth, SSO, token, model authorization, or permission errors: stop delegation and report the exact blocker.
- Local TraeCLI fails without diagnostics: report TraeCLI observer as unavailable and continue only with short bounded main-agent checks.

If TraeCLI fails with auth, token, keyring, SSO, sandbox, or permission errors, stop delegation and report the exact blocker. If the only blocker is model availability or authorization, retry once with the next model from the ordered model list. Do not silently bypass permissions or expand write capability.

Use the prompt templates in [references/observer-prompts.md](references/observer-prompts.md) when delegating:

- Runtime log search
- Runtime snapshot
- Internal research
- Bounded runtime monitoring

When delegating runtime observation to TraeCLI, use the observer prompt contract in [references/observer-prompts.md](references/observer-prompts.md). For BOE/PPE/online observation, do not accept local evidence unless the target is local runtime; TraeCLI must use named platform tools or report blocked.

## Token And Evidence Discipline

Runtime work can flood the context with logs and large platform responses. Keep every search bounded and reproducible.

- Search by strong identifiers first: `task_no`, `task_id`, `log_id`, `msg_id`, request path, metric name, config key, Redis key, or a unique test marker.
- Use narrow time windows by default, usually the exact case timestamp or latest 10-30 minutes.
- Limit output by match count, tail windows, resource name, page size, and selected fields.
- Summarize long JSON, SQL, payloads, and stack traces. Include at most 1-2 representative lines per pattern unless raw output is required for audit.
- Query named platform resources before broad listing. For TCC, prefer `get` for a known key and use `list` only with keyword, directory, region/env, and page limits.
- Retain only decision fields from large responses: resource name, effective/online version, latest version, status, timestamps, key values, identifiers, and errors.
- If full raw output is needed, save or reference its location and report an evidence index instead of pasting everything.

## Project Lessons

Use project-local runtime lessons to avoid repeating known project-specific failures. Detailed storage, templates, and git-ignore rules live in [references/project-lessons.md](references/project-lessons.md).

Before Phase 1, locate the project root with `git rev-parse --show-toplevel` when possible. If `.runtime-debug-test/index.md` exists at the project root, read it first, then load only relevant pitfall files by keyword, service, env, resource, or error. Fold matching lessons into the readiness summary.

During execution, mark a candidate lesson only when the issue is likely to recur and the cause or workaround is evidence-backed. Do not record secrets, tokens, cookies, full user payloads, broad raw logs, or unverified guesses.

At report time, write or update project lessons only after git-ignore protection is clear:

- Default storage is `.runtime-debug-test/` at the project root.
- Protect it with `.git/info/exclude`, not repo-tracked `.gitignore`.
- On first creation or when exclude is missing, show the proposed directory, exclude entry, and lesson content, then ask for user confirmation before writing.
- If the directory exists and exclude is already effective, update lessons directly and report the changed files plus ignore verification.
- In a non-git repo, read existing lessons if present, but do not create persistent lessons by default; report that git ignore protection is unavailable.

## Phase 1: Plan And Dependency Readiness

### 1. Understand The Feature

Read the relevant code before planning runtime calls. Use `rg` first for routes, handlers, config keys, request structs, status constants, repository methods, MQ topics, Redis keys, and metrics.

Summarize:

- Behavior changed: user-visible or system-visible behavior.
- Entry points: HTTP, MQ, cron, callback, CLI, scheduled job, or worker.
- Control branches: feature flags, gray rules, config switches, fallback paths.
- State transitions: DB status, Redis keys, MQ ack/nack, external job status.
- Terminal signals: callback, DB terminal state, artifact, comment, metric, alert, or log.

Do not invent request fields or resource names. If code and config disagree, call out the mismatch.

### 2. Classify Runtime Risk

Classify each planned case before proposing live actions:

| Risk | Examples | Rule |
| --- | --- | --- |
| Read-only | Health checks, config reads, log queries, dry validation | Proceed with bounded evidence. |
| Local write | Local files, local cache, local DB only | Proceed if cleanup is clear. |
| Shared write | BOE/PPE DB rows, Redis keys, MQ messages, TCC changes | Tell the user what will be touched and why. |
| External side effect | Sandbox/job creation, callbacks, comments, alerts, model calls, user-visible output | Ask before broad, costly, user-visible, or hard-to-clean actions. |

Ask before destructive cleanup, broad config changes, offset changes, DLQ consumption, deploys, or any action that could affect other users.

### 3. Confirm Config Dependencies

Identify dynamic config, local config, env vars, boot flags, runtime env, region, namespace, and config directory/path.

Inspect available config before finalizing test data:

- For TCC, use `bytedcli tcc config get/list` where available.
- Distinguish latest version from online/effective version.
- Preserve unrelated fields when asking to update config.
- Delegate high-volume read-only config discovery to TraeCLI only with explicit resource names, env, questions, and max output.

If config cannot be confirmed, stop and ask a targeted question. Include the proposed TCC/local JSON/YAML needed to unblock.

### 4. Confirm Resource Dependencies

Identify all runtime resources:

- MQ topics, producer/consumer groups, clusters, retry behavior, DLQ behavior.
- MySQL/RDS tables, columns, indexes, seed rows, and terminal states.
- Redis keys, TTLs, locks, counters, semaphores, and idempotency keys.
- TOS/object storage buckets, paths, credentials, and callback URLs.
- Downstream services, sandbox/job systems, model providers, auth tokens, IAM.

Use local code and available read-only tools to confirm resource names and schemas. If a dependency cannot be confirmed, ask for the concrete artifact needed:

- Config: proposed TCC/local config JSON/YAML.
- DB: `CREATE TABLE`, `ALTER TABLE`, `INSERT`, or `UPDATE` SQL.
- MQ: topic/group/cluster and sample message schema.
- Redis: key pattern, value shape, TTL, and cleanup command.

### 5. End-To-End Compile And Startup Readiness

After dependencies are clear, validate the whole runnable service, not only the packages touched by the change.

- Run focused package tests for changed code, but treat them as additive evidence only.
- Always run an entrypoint/root compile check that covers startup wiring. For Go services, prefer `go test .` or the repo's equivalent root-package compile command before package-scoped tests.
- Run the repo-native build command when available, such as `bash build.sh`, `make build`, or the documented package build. Do this before runtime execution unless the user explicitly accepts an environment blocker.
- Build or start the service using repo-native commands and verify the startup path can reach the changed wiring.
- If startup requires external resources, verify the missing config/resource error before asking the user.
- Do not treat package-scoped tests as startup readiness. Do not proceed to Phase 2 until the root compile/build/start check passes, or the blocker is explicitly accepted as the test boundary.

End Phase 1 with:

- Feature under test.
- Risk classification for planned cases.
- Confirmed config and effective versions.
- Confirmed MQ/MySQL/Redis/downstream dependencies.
- Startup command, URL, and log location.
- Known risks and unresolved dependencies.

If the user asks for a plan only, stop after Phase 1 plus the Phase 2 matrix.

## Phase 2: Runtime Execution And Observation

### 1. Maintain A Test Matrix

Create and update a matrix while executing:

| Field | Requirement |
| --- | --- |
| Purpose | Behavior or branch covered. |
| Preconditions | Config/resource state. |
| Test data | Request body, MQ payload, DB row, Redis state, or marker. |
| Execution | Exact command or call. |
| Observation | Logs, SQL, Redis, metrics, downstream console. |
| Expected result | Status transition and side effects. |
| Cleanup | Config reset, Redis delete, terminal callback, stop service, test-row cleanup. |
| Status | pending, running, passed, failed, blocked, or skipped. |

Cover when applicable:

- Happy path.
- Config disabled or gray miss.
- Invalid or missing dependency.
- Concurrency and rate limiting.
- Idempotency and duplicate delivery.
- Worker/downstream failure and retry.
- Timeout, orphan, or cron recovery.
- Callback terminal-state sync.

### 2. Execute Cases

For each case:

1. Confirm preconditions.
2. Start or confirm log tracing.
3. Execute the exact request/message yourself.
4. Capture response, timestamp, and identifiers.
5. Query logs, DB, Redis, metrics, or downstream state.
6. Compare actual behavior with expected behavior.
7. Update the matrix and cleanup state.

For BOE/PPE/online short-window log or metric observation, delegate a TraeCLI snapshot before querying directly. If TraeCLI fails, times out, or returns evidence without identifiers, record the failed delegation and run at most one narrow main-agent fallback query for that snapshot.

When observation is long-running or noisy, do not delegate an internal loop to TraeCLI. The main agent should schedule bounded TraeCLI snapshot tasks with explicit windows, identifiers, success/failure signals, and stop conditions, then decide whether another snapshot is needed. If TraeCLI snapshots cannot perform the observation, mark the long-running tracing item blocked or unavailable and report the missing evidence; do not replace it with main-agent long-cycle tracing.

If behavior differs from expected, diagnose before moving on unless the user asked only for test data construction. If two diagnosis iterations still do not identify the root cause, stop execution and report current evidence, excluded hypotheses, and the blocker.

Do not leave required long-running sessions active when finalizing. Stop dev servers, local services, consumers, and ports unless the user explicitly asks to leave them running.

## Runtime Test Report

Report with enough identifiers for another engineer to reproduce the evidence:

```markdown
## Runtime Test Report

Environment:
- Service:
- Config source:
- Startup command:
- Log location:

Dependency Readiness:
- Config:
- MQ:
- MySQL:
- Redis:
- Downstream:

Observer Usage:
- TraeCLI delegated tasks:
- Evidence accepted:
- Evidence rejected or incomplete:

Test Results:
| Case | Coverage | Input | Expected | Actual | Result |
| --- | --- | --- | --- | --- | --- |

Findings:
- ...

Unverified Items:
- Case X: not verified, reason: [environment/permission/time]

Cleanup:
- ...

Artifacts And Identifiers:
- task_no / task_id / log_id / msg_id / config version / job id

Residual Risk:
- ...

Follow-up Docs:
- Project lessons read or updated, plus ignore verification
- Other files updated with new runtime knowledge, if any
```

Keep the report factual. Include failed commands, missing resources, blockers, and unverified items explicitly. If testing reveals reusable runtime knowledge, update project lessons or current plan/tasks so the next run does not rediscover it.

## Interaction Rules

- If the user asks for a plan only, do not execute live cases.
- If the user asks to execute, proceed through both phases.
- If live config or external resources must be changed, ask for approval and show the exact change.
- If a dependency cannot be verified, ask a targeted question with the proposed artifact.
- If the service cannot start, report the blocker and evidence; do not fabricate runtime results.
- Keep final answers concise, but include enough evidence identifiers to verify the conclusion.
