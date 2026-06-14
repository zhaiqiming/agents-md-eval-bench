## Engineering Behavior

- Prefer the smallest change that fully solves the user's request.
- Every meaningful code change should trace back to the current task. Do not make opportunistic refactors or unrelated cleanup.
- Do not add abstractions, configuration, dependencies, or extensibility unless they remove real current complexity or are explicitly requested.
- Preserve existing behavior, public APIs, data formats, and ownership boundaries unless the task clearly asks to change them.
- When requirements are ambiguous but the risk is low, state the assumption and proceed. When ambiguity affects architecture, data, security, compatibility, or large amounts of code, ask before changing.
- Work with the repository's existing style and conventions instead of introducing a new preferred style.
- Remove only dead code, unused symbols, or cleanup directly caused by your own change unless the user asks for broader cleanup.
- Keep changes narrow enough that they are easy to review, test, and revert.

## Plan Mode Recommendations

- When presenting a recommended option in Plan mode, explain why it is recommended, how it would be carried out, and what benefit it gives the user.
- Keep the explanation concise but educational, so the user can learn the reasoning and grow their own judgment alongside Codex and GPT.
- Make tradeoffs explicit when useful: what the recommendation optimizes for, and what it does not prioritize.

## Validation Automation

- For complex validation tasks, prefer a reusable project-local script over ad hoc manual steps or long one-off shell pipelines.
- Create or update validation scripts when the workflow is likely to be repeated, has multiple steps, needs assertions, or is easy to perform incorrectly by hand.
- Follow the repository's existing script locations and conventions, such as `scripts/`, `tools/`, `hack/`, `Makefile`, package scripts, or test utilities.
- Keep validation scripts parameterized and reproducible. Avoid hardcoded local paths, secrets, personal environment assumptions, or one-off timestamps.
- Scripts should produce clear pass/fail output and exit non-zero on failure.
- After using a validation script, report the command, result, and any remaining manual or environment-dependent checks.

