# Benchmark versions

A benchmark edition fixes the task population, request contract, acceptance
rules, frozen references and scoring source. Its version is independent of
the Python package version. A package upgrade does not upgrade a report.

Use a readable `MAJOR.MINOR.PATCH` together with immutable SHA-256 bindings.
Keep the exact repository commit in the harness dependency lock. A Git tag
such as `bench-v2.0.1` gives a released commit a durable name; never move
or overwrite a published release tag. A tag alone does not identify external
reference bytes or a report's selected task population.

Create `bench-vMAJOR.MINOR.PATCH` tags only in this benchmark repository.
Browser Eval publishes software versions as `vMAJOR.MINOR.PATCH` and records the
full Git commit for execution and report-building code.
A report names the benchmark edition it uses, and the hosting platform's
immutable version ID identifies each published build. Retain benchmark tags
needed by published reports; do not create report, date or review-checkpoint tags.

| Change | Version | Comparing results |
| --- | --- | --- |
| Documentation or presentation; measurement contracts and scorer unchanged | Patch | Direct, with the same execution controls |
| Reviewed scoring/reference correction; original tasks and requests retained | Minor | Recompute both saved cohorts under one edition before comparison |
| Added/removed tasks, different URLs, requests, output scope or retrieval route | Major | Start a separate benchmark series of results |

A minor version is for correcting the existing measurement, not adding a new
scoring dimension under the same name. Expanding stable-label checks into a
main-content benchmark is a major change. The release tool checks concrete
population and request differences; maintainers still review whether a rule
change preserves the intended task. Existing annotation revisions retain
their independent source evidence and executable correction controls.

## Freeze an edition

`lexbench-webfetch version` verifies the installed catalog's complete suite list,
task definitions, frozen reference bindings and scorer against
`definitions/benchmark-release.json`. The published `bench-vMAJOR.MINOR.PATCH`
tag fixes that catalog. Full reference inputs remain separately hash-bound;
the catalog does not replace the executable datasets or distribute their source
captures. A report binds its actual selected population with the sidecar below;
installing a newer catalog never expands that population.

Compile or export the inputs through their existing owner first, including any
registered annotation revision. Freeze the complete selected population before
provider calls:

```sh
uv run --frozen lexbench-webfetch release \
  --dataset /absolute/inputs/dataset.json \
  --output /absolute/inputs/benchmark-release.json \
  --benchmark lexbench-webfetch --version 2.0.1 \
  --scorer-revision <full-40-character-scorer-commit>
```

For a successor, add `--previous /absolute/previous/benchmark-release.json`.
The scorer commit locates the code; the independently computed scoring-source
hash fixes the actual evaluator bytes. Scoring corrections also require a
concrete `--change-note`. The tool rejects
an insufficient version bump and an existing output path. Keep the sidecar
alongside frozen inputs, outside Git. It contains no provider measurements or
local paths. Commit reusable definitions and publish the code through the
normal feature-branch and release process.

```sh
uv run --frozen lexbench-webfetch compare-releases \
  /absolute/old/benchmark-release.json /absolute/new/benchmark-release.json
```

The result is `direct`, `rescore` or `separate`. It checks actual contract
fingerprints in addition to version numbers. Reusing the same version for a
different measurement is an error. A different major edition stays separate
even if some task IDs overlap. An overlap analysis may be diagnostic, but it
does not make the two full-population percentages comparable.

## Reports and retained calls

Report builds retain the selected edition, dataset digest and per-result
scoring-source identities. Rebuilding presentation preserves that edition.
Scoring corrections create a new edition and result revision, retaining the
previous report. Do not replace task inputs from an installed package merely
because it is newer.

For a minor correction, reuse successful and failed saved outputs wherever
the original request contract still applies, and recompute their scores under
one scorer. Changed requests need new calls for the affected scope. Preserve
all physical attempts and use the existing final-attempt selection policy.
Execution budgets, method configurations and timing comparability remain
owned by the harness; a matching dataset edition does not establish those.

Historical reports without a readable edition keep their existing exact hash
bindings. Naming one does not change its task snapshot, results, permissions
or original scoring source. Never label a historical subset as the latest
full dataset.
