<div align="center">

<img src="docs/assets/overview.png" alt="LexBench Web Fetch — Measure what comes back." width="100%">

**English** · [简体中文](docs/README.zh-CN.md)

[![CI](https://github.com/lexmount/lexbench-webfetch/actions/workflows/ci.yml/badge.svg)](https://github.com/lexmount/lexbench-webfetch/actions/workflows/ci.yml)
[![License: Apache 2.0](https://img.shields.io/badge/code-Apache--2.0-51735b)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-356a91)](pyproject.toml)

[Tasks](#task-suites) · [Quickstart](#quickstart) · [Scoring](#score-an-answer) · [Contributing](CONTRIBUTING.md)

</div>

LexBench Web Fetch provides tasks and scoring tools for web retrieval: page text, records with usable links, resources and files. Use it with your own runner or [Browser Eval](https://github.com/lexmount/browser-eval).

## Task suites

| Suite | Tasks | Scope |
| --- | ---: | --- |
| `webfetch` | 150 | Web pages, documents, images, video and challenge pages |
| `dynamic-content` | 100 | Content and records loaded after the initial response |
| `popular-sites` | 100 | Content on widely used websites |
| `access-restrictions` | 100 | URLs with previously observed access restrictions |
| `articles` | 100 | Article bodies, initial comments and post collections |

The catalog contains 550 task entries across five suites. Public definitions include task instructions and acceptance rules; complete frozen reference inputs must be obtained separately. See [data and access](docs/data.md) and [article requirements](src/lexbench_webfetch/definitions/evaluation/articles/README.md).

## Quickstart

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then:

```sh
git clone https://github.com/lexmount/lexbench-webfetch.git
cd lexbench-webfetch
uv sync --frozen
uv run --frozen lexbench-webfetch list
uv run --frozen lexbench-webfetch validate
```

These commands check the bundled definitions offline, without a browser or API key.

To export a suite, obtain the frozen files listed in its input manifest and run:

```sh
uv run --frozen lexbench-webfetch export \
  --suite webfetch --source /absolute/path/approved-inputs \
  --output /absolute/path/new-input-directory
```

Export verifies the input hashes and writes the declared files to a new directory. Full reference captures are not distributed in this repository; there is currently no public input bundle. The [data guide](docs/data.md) describes required files and access.

## Score an answer

Try an accepted and a rejected saved response:

```sh
uv run --frozen lexbench-webfetch score --task examples/task.json --response examples/answer.txt
uv run --frozen lexbench-webfetch score --task examples/task.json --response examples/missing.txt
```

For real evaluations, use the complete task from a verified dataset. Add `--metadata metadata.json` for structured response fields, or `--file /absolute/path/file` for delivered files. Scoring requirements and result reporting are described in the [evaluation protocol](docs/protocol.md).

## Versions and execution

Run `uv run --frozen lexbench-webfetch version` to inspect the installed catalog. Tags use `bench-vMAJOR.MINOR.PATCH`. Each report freezes the selected tasks and scoring source in `benchmark-release.json`; a package upgrade leaves that selection unchanged.

Use `release` to freeze an edition and `compare-releases` to check comparability. See [versioning](docs/versions.md) for commands and major/minor/patch rules.

To execute browser or service calls and build reports, follow the [Browser Eval integration guide](https://github.com/lexmount/browser-eval/blob/main/docs/benchmarks.md).

## Contribute

Read [CONTRIBUTING](CONTRIBUTING.md) before changing task requirements or scoring. Run `make check` to validate definitions and tests.

[Security](SECURITY.md) · [Third-party content](THIRD_PARTY.md) · [Apache 2.0](LICENSE)

## Cite LexBench Web Fetch

Use this citation or [CITATION.cff](CITATION.cff), and record the benchmark edition and suites used.

```bibtex
@software{lexbench_webfetch_2026,
  author = {{LexBench Web Fetch contributors}},
  title = {LexBench Web Fetch},
  year = {2026},
  version = {0.3.0},
  url = {https://github.com/lexmount/lexbench-webfetch}
}
```
