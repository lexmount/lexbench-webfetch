# Contributing

Task definitions and acceptance requirements belong here. Task models, acceptance scoring, file checks and compilation also belong here. Browser adapters, scheduling, reference-capture orchestration and report rendering belong in the selected execution harness. Include a task ID and a reproducible accepted/rejected example when reporting a rule problem.

Use Python 3.11 or newer and [uv](https://docs.astral.sh/uv/). Run `uv sync --frozen`, then `make check`. Run `uv sync --frozen --extra test` to install the test tools. Tests use synthetic inputs and need no browser, network access or historical source bundle. Keep the English and Chinese READMEs aligned; other guides use English.

A task revision must explain the intended requirement, preserve the prior input version, and include scenarios that should pass and fail. Update the original dataset, catalog, public task definitions, input manifest and registry together after independent source verification. Do not regenerate old hashes to disguise an input correction. Frozen quotes retain their original language.

Keep measured outputs, captures, credentials and internal review notes outside Git. A result proposal must supply the evidence listed in the [protocol](docs/protocol.md); opening a PR does not add it to a leaderboard. See [THIRD_PARTY](THIRD_PARTY.md) before sharing source material.

## PR and commit titles

Use `<type>(<scope>): <summary>` for PR titles and new commit subjects. The scope is optional; use the module or feature affected, such as `scoring` or `webfetch`.

Choose the type that describes the change:

| Type | Change |
| --- | --- |
| `fix` | Correct existing behavior |
| `feat` | Add supported behavior |
| `docs` | Change documentation |
| `refactor` | Restructure code without changing behavior |
| `test` | Add or correct tests |
| `perf` | Improve performance |
| `build` / `ci` | Change packaging, dependencies or automation |
| `chore` | Other maintenance |

Write the summary in English, start with an imperative verb, and describe the concrete change. Aim for 72 characters or fewer, including the prefix; omit a trailing period. Use `!` before the colon for a breaking change and explain the migration in the description.

Examples:

- `fix(scoring): require facts in the returned body`
- `fix(webfetch): reject mixed executable versions before release`
- `docs(contributing): define PR and commit title conventions`

Avoid titles such as `Fix review feedback`, `Update code` or `Misc improvements`; name the behavior or document that changes. A PR title describes the complete diff; each commit subject describes that commit. Update the PR title when its scope changes. If squash merging is used, use a subject that follows the same format. Apply this convention to new work; do not rewrite shared commits solely to rename them.
