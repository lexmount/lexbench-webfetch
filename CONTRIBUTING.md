# Contributing

Task, reference and scoring releases follow [benchmark versions](docs/versions.md).
Keep package releases separate from benchmark editions; a new package commit
must not silently replace a report's frozen inputs.

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
- `fix(webfetch): disclose build provenance for partial reruns`
- `docs(contributing): define PR and commit title conventions`

Avoid titles such as `Fix review feedback`, `Update code` or `Misc improvements`; name the behavior or document that changes. A PR title describes the complete diff; each commit subject describes that commit. Update the PR title when its scope changes. If squash merging is used, use a subject that follows the same format. Apply this convention to new work; do not rewrite shared commits solely to rename them.

## Score-only annotation revisions

Keep an existing revision's bytes unchanged. Bind each new correction in
`definitions/annotation-revisions/reviews.json` to its revision hash, exact field
difference, frozen source inputs, reason, and accepted/rejected regression controls.
These controls run before a revision is applied. Changing another field requires
updating its review binding; a registered control ID alone is insufficient.

Inspect a revision without private measured outputs:

```sh
uv run --frozen lexbench-webfetch inspect-revision \
  --suite dynamic-content --revision serialization-20261021
```

`export --revision` writes `annotation-review.json` beside the dataset, including
the field differences, source hashes and executed controls. It preserves the
original input files and the revision's existing dataset identity.

## License

Contributions use the [Apache License 2.0](LICENSE). Preserve third-party licenses, copyright notices and source attributions described in [THIRD_PARTY](THIRD_PARTY.md).
