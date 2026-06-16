# Project AGENTS.md Template

Use this as a skeleton. Replace bracketed text with verified repository facts. Delete sections that are not useful for the repository.

```md
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

## Development Standards

- [MUST] Follow the repository's existing style, ownership boundaries, and project-level conventions.
- [MUST] Do not hand-edit generated code. Regenerate it through the documented command when the repository provides one.
- [MUST] Keep public APIs, schemas, data formats, migrations, and compatibility behavior stable unless the task explicitly changes them.
- [RECOMMENDED] Point complex project-specific procedures to existing scripts, docs, or skills instead of embedding long SOPs here.

## Branch Naming

- [MUST] When creating a new branch, use `feat/<short-description>` for feature or requirement work and `fix/<short-description>` for issue or bug-fix work.
- [MUST] Do not create, switch, or rename branches unless the user asks for branch management or the current task explicitly requires it.
- [RECOMMENDED] If the current branch is unsuitable, recommend a compliant branch name instead of switching automatically.

## Static Checks

<!-- AGENTS-MAINTAIN:BEGIN static-checks -->
- [MUST] Prefer project-defined local checks from Makefiles, package scripts, CI scripts, or documented commands.
- [MUST] If no project command exists, use the language-appropriate baseline:
  - Go: `golangci-lint run ./...` when `golangci-lint` is available; fall back to `go vet ./...` only when `golangci-lint` is unavailable. If the repo has `.golangci.yml`, `.golangci.yaml`, or a project lint command, use that project configuration. Do not create a new golangci-lint config unless requested or already expected by the repo. If sandboxing blocks Go or golangci-lint cache writes, rerun with `GOCACHE` and `GOLANGCI_LINT_CACHE` set to writable temp or project-local cache directories before treating the check as failed.
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

## Agent Review

- [MUST] Keep `/review` and Coco separate from language static checks.
- [MUST] When both are available and not blocked, start `/review` and Coco review-only checks concurrently.
- [MUST] Use both checks to look for code logic errors, boundary errors, concurrency/error-handling issues, compatibility risks, incomplete implementation, and mismatch with the plan.
- [MUST] Keep Coco read-only: no file edits, no real request execution, and no yolo-style write permissions.
- [MUST] Report both results; if one check cannot run, explain why.

## AGENTS.md Maintenance

- [MUST] Update this file when repository structure, generated-code boundaries, static checks, validation scripts, CI/local gates, API/schema/route expectations, or high-risk workflows change.
- [MUST] Prefer editing marked `AGENTS-MAINTAIN` blocks for derived repository facts.
- [FORBIDDEN] Do not rewrite stable policy sections unless the user explicitly asks.

## Non-Goals

- [FORBIDDEN] Do not include secrets, tokens, personal credentials, or local-only private state.
- [FORBIDDEN] Do not include generated-by notes, local filesystem paths, Git revision audit notes, generation timestamps, or Codex auto-read/discovery status in the file body.
- [FORBIDDEN] Do not include unverified guesses about repository behavior.
- [FORBIDDEN] Do not turn this file into a full README, architecture document, deployment guide, or exhaustive file inventory.
```

## Authoring Notes

- Include repository structure in concrete project `AGENTS.md` files, but keep it concise and decision-useful.
- Start generated files directly with `# AGENTS.md` or the first useful project heading; put generation notes in the final chat response, not in the file.
- Do not include repository structure in generic workspace templates.
- Prefer a compact tree for repository structure when it improves scanability.
- Put likely-changing derived facts inside `AGENTS-MAINTAIN` blocks.
- Prefer `[MUST]`, `[FORBIDDEN]`, and `[RECOMMENDED]` labels when the strength of a rule matters.
- Let existing project instructions override this template when they are more specific.
