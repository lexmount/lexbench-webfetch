# Data layout and rights

The suite registry is `src/lexbench_webfetch/definitions/registry.json`. Its suite directories contain the current inputs. It binds every shipped suite file by SHA-256 and records each population's ID and size.

| File within a suite | Role |
| --- | --- |
| `tasks.json` | Public task instructions and acceptance requirements, with body-reference text replaced by SHA-256/character-count bindings, and no full reference bodies or capture logs |
| `dataset-catalog.json` | Original ordered task inventory, source URLs and complete task-definition hashes |
| `source-inputs.json` | Exact executable dataset and external reference-file hashes |

The initial versions were imported from Browser Eval commit `894b38f8`. The current access-restriction suite selects the later frozen version declared in the registry. Source commits and per-file hashes are in `provenance.json`. Original catalog and manifest bytes are retained, including original dataset IDs and task languages. Their names may contain historical method labels; those labels identify frozen input versions and confer no method-specific acceptance exception.

Public task requirements are maintained in this repository. Frozen historical catalogs and manifests also live under `definitions/evaluation/` with their original relative paths and bytes. Browser Eval resolves its historical logical paths through this installed package. It retains experiment profiles and compact hash bindings, rather than duplicate definition files.

## External inputs

An approved input directory contains the exact `dataset.json` and, when listed by the manifest, `sources/` and `list-references/` files. `verify-inputs` checks every declared file, the full dataset hash, ordered complete task-definition hashes and public requirements. `export` verifies the source, copies only declared files into a new directory and verifies the copy. Unlisted files are ignored and never exported. No provider calls or downloads occur.

The exported directory intentionally has no `source-inputs.json`: it is a directly materialized, verified input tree. Browser Eval can consume its dataset through `--dataset` without relying on Browser Eval's historical storage paths. Keep the suite manifest and benchmark revision with your experiment metadata.

Complete third-party text, PDFs, media, rendered pages and provider outputs are excluded from this repository. Obtain required inputs under their original terms. There is currently no hosted public input bundle; the public definitions can be inspected independently, while exact historical runs require separately acquired matching inputs. A new capture is a new version and must not be presented as the old frozen suite.

## Score-only annotation versions

Frozen `tasks.json`, catalogs and input manifests retain their original bytes.
Corrections live in `definitions/annotation-revisions/` with a distinct revision
ID, parent task and source-manifest hashes, per-task predecessor hashes and
registered scoring controls. They change acceptance annotations, not collection
URLs, prompts or saved provider outputs.

To export a corrected definition, select its version explicitly:

```sh
uv run --frozen lexbench-webfetch export --suite webfetch --source /path/to/frozen-inputs --output /path/to/new-inputs --revision serialization-20261021
```

The exported dataset receives a new ID and a `definition_revision` binding.
Without `--revision`, export reproduces the original frozen dataset exactly.
A score recomputed with revised annotations must retain both definition hashes
and its original call identities; it is not a new browser run.
