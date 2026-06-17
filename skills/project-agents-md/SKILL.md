---
name: project-agents-md
description: Create, update, rewrite, or plan a concrete repository-level AGENTS.md for Codex. Use when the user asks for project AGENTS.md, repo AGENTS.md, workspace/project guidance that should be based on actual repository facts, or a project-level Codex instruction file for Go, Python, JavaScript/TypeScript, Java/Kotlin, Rust, or other codebases. Do not use for global ~/.codex/AGENTS.md personal preference design unless the user explicitly asks for global guidance.
---

# Project AGENTS.md

Use this skill to produce project-level Codex guidance from verified repository facts. The output should help future Codex agents edit, test, review, and avoid mistakes in this specific repository. Do not turn `AGENTS.md` into a README, and do not invent project knowledge.

## Workflow

1. Confirm scope and discovery.
   - Identify the target directory and Git root with non-mutating inspection.
   - Explain in chat or the final report whether the target `AGENTS.md` will be auto-read by Codex. Do not write this discovery note into the generated file. Codex usually reads files from the Git root toward the current directory; a workspace parent outside the Git root may not be loaded for child repositories.
   - If the user asks for a global personal file, stop using this skill unless they explicitly want global guidance.

2. Inspect existing guidance.
   - Read any existing `AGENTS.md`, `AGENTS.override.md`, `.github/copilot-instructions.md`, `.cursor/rules`, README, build files, CI files, and local scripts relevant to agent behavior.
   - If `AGENTS.md` already exists, merge or revise it. Do not overwrite it blindly.

3. Gather repository facts.
   - Prefer tracked sources: README files, language manifests, Makefiles, package scripts, CI configs, `scripts/`, source entrypoints, API or IDL definitions, migrations, config samples, and deployment or packaging files.
   - Treat `.git/`, local hooks, editor settings, personal config, and untracked files as clues only. Do not write them as project rules unless tracked documentation or configuration confirms they are part of the repository workflow.
   - Identify language stack, frameworks, build systems, runnable commands, test entrypoints, static checks, local CI gates, generated-code boundaries, configuration sources, migration paths, high-risk change areas, and key repository structure.
   - Separate facts into repository facts, executable commands, project constraints, and TODOs or questions before drafting.
   - Include only verified facts that change how an agent should work in the repo.
   - Omit unconfirmed guesses. If a fact matters but cannot be verified, mark it as a short TODO or ask the user before writing.

4. Generate project-level guidance.
   - Prefer the structure in `references/project-agents-template.md`.
   - Start the file directly with `# AGENTS.md` or the first useful project heading. Do not add generated-by, verified-at-revision, filesystem path, auto-read, or audit-note prefaces.
   - Use rule labels when helpful:
     - `[MUST]` for required behavior.
     - `[FORBIDDEN]` for prohibited behavior.
     - `[RECOMMENDED]` for preferred but context-dependent behavior.
   - Point long SOPs to existing project skills, scripts, or docs instead of copying lengthy procedures into `AGENTS.md`.
   - Prefer a compact tree for `Repository Map` or `Architecture` sections when it improves scanability. Keep it decision-useful, usually no deeper than 2-3 levels.
   - Use `AGENTS-MAINTAIN` blocks for derived or likely-changing repository facts so future agents can update them without rewriting stable policy sections.
   - Put stable policy sections outside `AGENTS-MAINTAIN` blocks. Use managed blocks for derived sections such as repository map, architecture/runtime facts, build commands, testing, static checks, configuration, security, and validation scripts.

5. Validate the result.
   - Check that project structure and workflows are concise, verified, and decision-useful.
   - Check that no secrets, transient local state, or overly detailed file inventories were added.
   - Check that static checks are language-appropriate and prefer project-defined commands.
   - Check that Codex `/review`, reviewer subagents, and TraeCLI review are in a language-independent Agent Review section.
   - Check that maintainable facts are inside marked `AGENTS-MAINTAIN` blocks when future updates are expected.

## Content Guidelines

### Project Overview

Include a one-paragraph summary only when verified from the repository. Mention major languages and frameworks. Avoid marketing copy and unverified product claims.

Do not begin the file with blockquotes or metadata such as local filesystem paths, Git revisions, generation timestamps, or Codex discovery status. Put that information in the assistant's final response when useful.

### Repository Map

Include only directories that affect future code changes. Useful entries include source roots, API definitions, generated code, migrations, scripts, tests, config, and deployment or packaging folders. Prefer a compact tree when it is easier to scan than bullets. Avoid exhaustive file lists.

### Architecture / Runtime Facts

Include this section only when the repository proves useful runtime facts such as service entrypoints, CLI commands, jobs, routes, API surfaces, queues, scheduled tasks, or package boundaries. Tables are useful for commands, routes, and jobs. Do not infer behavior from filenames alone.

### Build & Commands

List project-provided build, run, test, lint, generation, and local CI commands when they are documented or discoverable from tracked scripts and manifests. Prefer a compact table with purpose, command, and source. Do not include personal shell aliases or commands that depend on untracked local state.

### Development Standards

Capture project-specific conventions: formatting, error handling, dependency boundaries, generated-code rules, config ownership, migration expectations, API compatibility, and areas needing extra care.

### Testing

Capture the repository's test commands, test layout, fixture or mock conventions, and any required environment assumptions. Prefer project scripts over language defaults. If the repository has no tests or the test entrypoint is unclear, say so briefly rather than inventing a command.

### Branch Naming

Use these defaults unless the repo already has stricter rules:

- When creating a new branch, use `feat/<short-description>` for feature or requirement work and `fix/<short-description>` for issue or bug-fix work.
- Do not create, switch, or rename branches unless the user asks for branch management or the current task explicitly requires it.
- If the current branch is unsuitable, recommend a compliant branch name instead of switching automatically.

### Static Checks

Prefer project-provided checks from Makefiles, package scripts, CI scripts, or documented local gates. If no project command exists, use a language default:

- Go: use `golangci-lint run ./...` when `golangci-lint` is available; fall back to `go vet ./...` only when `golangci-lint` is unavailable. If the repo already has `.golangci.yml`, `.golangci.yaml`, or a project lint command, prefer that project configuration. Do not create a new golangci-lint config unless the user asks or the repo already expects one. If Codex sandboxing blocks Go or golangci-lint cache writes, rerun with `GOCACHE` and `GOLANGCI_LINT_CACHE` set to writable temp or project-local cache directories before treating the check as failed.
- Python: prefer `ruff`, `mypy`, `pytest`, or project scripts; otherwise at least `python -m compileall`.
- JavaScript/TypeScript: prefer package-manager `lint`, `test`, or `tsc --noEmit`.
- Java/Kotlin: prefer Gradle or Maven `check`/`test`.
- Rust: prefer `cargo check`; use `cargo clippy` when available.
- Other languages: do not invent tooling. Discover existing lint/check commands first.

If a change modifies APIs, routes, protocols, schemas, data models, or validation surfaces, add guidance to update the matching verifier, smoke test, or reusable validation script in the same change.

### Validation Scripts

For complex or repeatable validation, prefer reusable project-local scripts over long manual command chains. Scripts should be parameterized, reproducible, clear about pass/fail, and exit non-zero on failure. Do not create repository scripts for one-off checks unless they are likely to be reused or protect a public validation surface.

### Security

Include security guidance only when verified from repository code or docs, such as secret handling, authentication boundaries, sensitive logging rules, input validation, sandboxing, or permission checks. Do not add generic security advice.

### Configuration

Include configuration guidance only when verified from repository code or docs, such as config files, environment variables, config samples, feature flags, or deployment-specific overrides. Mark unknown required config as TODO instead of guessing values.

### Agent Review

Keep agent review separate from language static checks.

- [MUST] Do not treat Codex `/review` as a shell command, MCP tool, or directly callable agent tool. It is a user-facing Codex slash command when the current surface supports it.
- [RECOMMENDED] If the user wants Codex's built-in review pass and the current surface supports `/review`, ask the user to run `/review`, then use the returned comments as review guidance.
- [RECOMMENDED] When the user explicitly authorizes agent review or parallel review and subagent tooling is available, spawn a read-only reviewer subagent.
- [MUST] Use TraeCLI as the default external review second perspective when `traecli` is available and not blocked.
- [MUST] Prefer `traecli review --uncommitted <prompt>` for working-tree changes, `traecli review --base <branch> <prompt>` for branch comparisons, or `traecli review --commit <sha> --title <title> <prompt>` for a single commit.
- [MUST] Keep TraeCLI review-only: do not run `traecli exec` to modify files, do not use `--permission-mode bypass_permissions`, `--sandbox danger-full-access`, `-y`, or yolo-style write permissions for review.
- [RECOMMENDED] For stricter isolation, use `traecli exec --sandbox read-only --ephemeral review ...` when that form works in the current TraeCLI version.
- [MUST] Review focus: logic errors, boundary errors, incomplete implementation, divergence from the plan, error-handling issues, concurrency issues, compatibility risks, and missing tests.
- [MUST] If reviewer subagent and TraeCLI are both available and authorized, start them concurrently. Report both results; if one cannot run, explain the blocker and residual risk.

### AGENTS.md Maintenance

Add maintenance rules when the file contains repository facts that will drift.

- [MUST] Update `AGENTS.md` only when a change affects future agent behavior, such as repository structure, generated-code boundaries, static checks, validation scripts, CI/local gates, API/schema/route expectations, or high-risk workflows.
- [MUST] Prefer editing marked `AGENTS-MAINTAIN` blocks for derived repository facts.
- [FORBIDDEN] Do not rewrite stable policy sections unless the user explicitly asks.

### Non-Goals

Do not include secrets, tokens, personal credentials, temporary local state, local filesystem paths, Git revision audit notes, generated-by notes, Codex auto-read notes, long business explanations, overly detailed file lists, or unverified guesses. Do not duplicate extensive README content.

## Reference

Read `references/project-agents-template.md` when drafting or updating an `AGENTS.md`.
