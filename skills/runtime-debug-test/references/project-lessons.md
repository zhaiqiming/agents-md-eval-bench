# Project Lessons

Use project lessons for runtime-debug knowledge that is specific to the current repository and likely to prevent repeated failures in later runs.

## Storage

Store lessons under the git project root:

```text
.runtime-debug-test/
  index.md
  pitfalls/
    <stable-slug>.md
```

Use stable lowercase slugs such as `sandbox-auth-failed-use-local.md` or `tcc-cli-wrong-env-param.md`.

Protect the directory with the local git exclude file:

```gitignore
.runtime-debug-test/
```

Add that entry to `.git/info/exclude`, not `.gitignore`. Verify protection with `git check-ignore .runtime-debug-test/index.md` or an equivalent git ignore check before writing lessons. This prevents normal `git add` and `git status` from including the directory, but it cannot prevent an explicit `git add -f`.

If the current directory is not a git repo, read existing `.runtime-debug-test/` files if present, but do not create new persistent lessons by default. Report that git ignore protection is unavailable.

## Preflight

Before Phase 1:

1. Run `git rev-parse --show-toplevel` when available.
2. If `<root>/.runtime-debug-test/index.md` exists, read it.
3. Load only relevant files under `<root>/.runtime-debug-test/pitfalls/` by matching service, env, resource, error text, command, or feature keywords.
4. Include matching lessons in the Phase 1 readiness summary.

Do not scan large lesson trees broadly. Prefer `rg` on `.runtime-debug-test/` with the current service, env, config key, topic, table, error, or command.

## When To Write

Write a lesson only when all are true:

- The failure or workaround is likely to recur in this project.
- The trigger is specific enough to recognize next time.
- Evidence exists: command, error summary, resource name, config key, log id, task id, or timestamp.
- The resolution or next diagnostic step is known.

Good candidates:

- Sandbox authorization failure that requires local validation instead.
- TCC CLI environment, site, region, namespace, or version selection mistakes.
- Project-specific startup blockers and accepted fallback validation.
- Required local env vars, ports, log paths, or bootstrap order.
- MQ/RDS/Redis resource naming or read-only query pitfalls.

Do not write:

- Secrets, tokens, cookies, passwords, private keys, or full credentials.
- Full user payloads or sensitive request/response bodies.
- Large raw logs, full stack traces, broad SQL dumps, or platform response dumps.
- One-off transient network failures without a stable workaround.
- Guesses where the cause or workaround is not evidence-backed.

## First-Write Confirmation

Before the first creation of `.runtime-debug-test/`, or before writing when `.git/info/exclude` does not protect it, show the user:

- Directory to create.
- Exact `.git/info/exclude` entry.
- Lesson file path.
- Lesson content summary.

Ask for confirmation before writing. After confirmation, create the directory, update `.git/info/exclude`, write the lesson, update `index.md`, and verify ignore behavior.

If `.runtime-debug-test/` exists and ignore protection is already effective, update lessons directly when the candidate passes the write rules. Report changed files and ignore verification in the runtime test report.

## Index Format

Keep `index.md` short and searchable:

```markdown
# Runtime Debug/Test Lessons

| Lesson | Env | Resource | Last Seen | Status |
| --- | --- | --- | --- | --- |
| [TCC CLI wrong env param](pitfalls/tcc-cli-wrong-env-param.md) | boe | TCC | 2026-06-14 | active |
```

## Pitfall Template

```markdown
---
title: Short reusable title
scope: runtime-debug
env: boe/ppe/prod/local
resource: TCC/MQ/RDS/Redis/sandbox/startup/etc.
status: active
last_seen: YYYY-MM-DD
---

## Symptom
What failed and how it appeared.

## Trigger
The condition, command, env, resource, or project setup that caused it.

## Evidence
- command:
- error summary:
- identifier:

## Resolution
The confirmed workaround, fix, or next diagnostic step.

## Next Time Checklist
- Concrete check to run before repeating the test.
```

Prefer summaries over raw output. Redact sensitive values before writing.
