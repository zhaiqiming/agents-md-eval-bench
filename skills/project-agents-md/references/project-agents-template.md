# Project AGENTS.md Template

Use this as a skeleton. Replace bracketed text with verified repository facts. Delete sections that are not useful for the repository.

````md
# AGENTS.md

## Project Overview

[One concise paragraph: what this repository is, the main languages/frameworks, and the main runtime or package shape. Use only facts verified from the repo.]

## Repository Map

<!-- AGENTS-MAINTAIN:BEGIN repository-map -->
```text
.
├── [path]/              # [Decision-useful responsibility]
├── [path]/              # [Generated code, API definitions, migrations, scripts, tests, or config when relevant]
└── [path]/              # [Keep this tree concise, usually no deeper than 2-3 levels]
```
<!-- AGENTS-MAINTAIN:END repository-map -->

## Architecture / Runtime Facts

<!-- AGENTS-MAINTAIN:BEGIN architecture-runtime -->
[Optional. Delete this section when the repository does not prove useful runtime facts.]

| Surface | Verified fact | Source |
| --- | --- | --- |
| Entry point | `[command, package, service, job, or binary]` | `[tracked file or script]` |
| API / route / task | `[route, handler, queue, cron, CLI command, or package boundary]` | `[tracked file or script]` |
<!-- AGENTS-MAINTAIN:END architecture-runtime -->

## Build & Commands

<!-- AGENTS-MAINTAIN:BEGIN build-commands -->
| Purpose | Command | Source |
| --- | --- | --- |
| Build | `[project-provided build command]` | `[Makefile/package script/CI/docs]` |
| Run locally | `[project-provided run command]` | `[Makefile/package script/CI/docs]` |
| Generate code | `[project-provided generation command, if any]` | `[Makefile/package script/CI/docs]` |
<!-- AGENTS-MAINTAIN:END build-commands -->

## Development Standards

- [MUST] Follow the repository's existing style, ownership boundaries, and project-level conventions.
- [MUST] Do not hand-edit generated code. Regenerate it through the documented command when the repository provides one.
- [MUST] Keep public APIs, schemas, data formats, migrations, and compatibility behavior stable unless the task explicitly changes them.
- [RECOMMENDED] Point complex project-specific procedures to existing scripts, docs, or skills instead of embedding long SOPs here.

## Testing

<!-- AGENTS-MAINTAIN:BEGIN testing -->
- [MUST] Prefer project-provided test commands from Makefiles, package scripts, CI scripts, or documented commands.
- [MUST] Keep tests aligned with the repository's existing layout, fixtures, mocks, and naming conventions.
- [RECOMMENDED] If the repository has no verified test entrypoint, state that the test command is not confirmed instead of inventing one.
<!-- AGENTS-MAINTAIN:END testing -->

## Branch Naming

- [MUST] When creating a new branch, use `feat/<short-description>` for feature or requirement work and `fix/<short-description>` for issue or bug-fix work.
- [MUST] Do not create, switch, or rename branches unless the user asks for branch management or the current task explicitly requires it.
- [RECOMMENDED] If the current branch is unsuitable, recommend a compliant branch name instead of switching automatically.

## Static Checks

<!-- AGENTS-MAINTAIN:BEGIN static-checks -->
- [MUST] Keep this section separate from `Testing` and `Build & Commands`; tests and builds do not replace static analysis.
- [MUST] Prefer project-defined local checks from Makefiles, package scripts, CI scripts, or documented commands.
- [MUST] If no project command exists, use the language-appropriate baseline:
  - Go: `golangci-lint run ./...` when `golangci-lint` is available; fall back to `go vet ./...` only when `golangci-lint` is unavailable. If the repo has `.golangci.yml`, `.golangci.yaml`, or a project lint command, use that project configuration. Do not omit `golangci-lint` merely because `go test` or `go vet` is present. Do not create a new golangci-lint config unless requested or already expected by the repo. If sandboxing blocks Go or golangci-lint cache writes, rerun with `GOCACHE` and `GOLANGCI_LINT_CACHE` set to writable temp or project-local cache directories before treating the check as failed.
  - Python: project `ruff`/`mypy`/`pytest` first; otherwise `python -m compileall`.
  - JavaScript/TypeScript: package-manager `lint`, `test`, or `tsc --noEmit`.
  - Java/Kotlin: Gradle or Maven `check`/`test`.
  - Rust: `cargo check`; `cargo clippy` when available.
  - Other languages: discover existing lint/check commands before choosing.
- [MUST] If static checks cannot run, report the blocker and residual risk.
<!-- AGENTS-MAINTAIN:END static-checks -->

## Validation Scripts

<!-- AGENTS-MAINTAIN:BEGIN validation-scripts -->
- [SHOULD] For complex, repeatable, multi-step, or easy-to-misread validation, prefer creating or updating a reusable project-local script instead of relying on long one-off command chains.
- [MUST] If the change introduces or modifies a public validation surface, keep the matching verifier, smoke test, SDK test, or validation script up to date.
- [MUST] Keep validation scripts parameterized, reproducible, and clear about pass/fail; they should exit non-zero on failure.
<!-- AGENTS-MAINTAIN:END validation-scripts -->

## Security

<!-- AGENTS-MAINTAIN:BEGIN security -->
- [MUST] Do not commit secrets, tokens, personal credentials, or local private config.
- [MUST] Preserve verified authentication, authorization, input validation, and sensitive logging boundaries.
- [RECOMMENDED] Add project-specific security rules only when they are verified from repository code or docs.
<!-- AGENTS-MAINTAIN:END security -->

## Configuration

<!-- AGENTS-MAINTAIN:BEGIN configuration -->
- [MUST] Follow verified configuration sources such as tracked config files, config samples, environment variable docs, feature flag definitions, or deployment manifests.
- [MUST] Do not hardcode local paths, secrets, personal environment values, or deployment-specific values unless the repository already defines them as fixtures.
- [RECOMMENDED] Mark required-but-unconfirmed config as TODO instead of guessing values.
<!-- AGENTS-MAINTAIN:END configuration -->

## Agent Review

- [MUST] Keep Codex `/review`, reviewer subagents, and TraeCLI review separate from language static checks.
- [MUST] Do not treat Codex `/review` as a shell command, MCP tool, or directly callable agent tool. When the current Codex surface supports it, `/review` is user-triggered; use its returned comments as review guidance.
- [RECOMMENDED] When the user explicitly authorizes agent review or parallel review and subagent tooling is available, spawn a read-only reviewer subagent.
- [MUST] Use TraeCLI as the default external review second perspective when `traecli` is available and not blocked. Run TraeCLI locally outside the Codex sandbox when host-local security context is required.
- [MUST] Choose an explicit TraeCLI review model from this ordered list: `Test-O-New-Thinking`, `DeepSeek-V4-Pro`, `MiniMax-M2.7`, `GLM-5.1`. If a model is unavailable, unauthorized, or unsupported, try the next model and report the fallback reason.
- [MUST] Prefer `traecli exec review` with TraeCLI's read-only sandbox, read-only network enabled, `-o <summary-file>`, and shell stdout/stderr redirection to a raw log so Codex reads only the final summary by default. Example shape: `traecli exec review -m <model> --sandbox read-only -c "sandbox_read_only.network_access=true" --uncommitted -o /tmp/trae-review-summary.md '<prompt>' >/tmp/trae-review-raw.log 2>&1`.
- [MUST] Use `--uncommitted` for working-tree changes, `--base <branch>` for branch comparisons, or `--commit <sha> --title <title>` for a single commit.
- [MUST] Keep TraeCLI review-only: do not ask it to modify files, do not use `--permission-mode bypass_permissions`, `--sandbox danger-full-access`, `-y`, or yolo-style write permissions for review.
- [MUST] Review focus: code logic errors, boundary errors, concurrency/error-handling issues, compatibility risks, incomplete implementation, mismatch with the plan, and missing tests.
- [MUST] If reviewer subagent and TraeCLI are both available and authorized, start them concurrently. Report both results; if one check cannot run, explain why.

## AGENTS.md Maintenance

- [MUST] Update this file when repository structure, generated-code boundaries, static checks, validation scripts, CI/local gates, API/schema/route expectations, or high-risk workflows change.
- [MUST] Prefer editing marked `AGENTS-MAINTAIN` blocks for derived repository facts.
- [FORBIDDEN] Do not rewrite stable policy sections unless the user explicitly asks.

## Non-Goals

- [FORBIDDEN] Do not include secrets, tokens, personal credentials, or local-only private state.
- [FORBIDDEN] Do not include generated-by notes, local filesystem paths, Git revision audit notes, generation timestamps, or Codex auto-read/discovery status in the file body.
- [FORBIDDEN] Do not include unverified guesses about repository behavior.
- [FORBIDDEN] Do not turn this file into a full README, architecture document, deployment guide, or exhaustive file inventory.
````

## Authoring Notes

- Include repository structure in concrete project `AGENTS.md` files, but keep it concise and decision-useful.
- Start generated files directly with `# AGENTS.md` or the first useful project heading; put generation notes in the final chat response, not in the file.
- Do not include repository structure in generic workspace templates.
- Prefer a compact tree for repository structure when it improves scanability.
- Put likely-changing derived facts inside `AGENTS-MAINTAIN` blocks, especially repository map, architecture/runtime facts, build commands, testing, static checks, configuration, security, and validation scripts.
- Keep stable policy sections outside managed blocks unless the project already owns them as drift-prone facts.
- Prefer tracked sources over local state. `.git/`, local hooks, editor settings, personal config, and untracked files may guide investigation, but do not write them as project rules unless tracked docs or configuration confirm them.
- Prefer `[MUST]`, `[FORBIDDEN]`, and `[RECOMMENDED]` labels when the strength of a rule matters.
- Let existing project instructions override this template when they are more specific.
