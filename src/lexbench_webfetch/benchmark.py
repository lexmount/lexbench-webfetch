"""Verify public definitions and materialize independently acquired frozen inputs."""
from __future__ import annotations

import hashlib
from copy import deepcopy
import json
import os
import re
import shutil
import tempfile
from pathlib import Path
from .paths import contained_path, safe_identifier
from .inputs import digest, load_manifest, verify_catalog

SUITES = Path(__file__).parent / "definitions"

# Full reference bodies and source-capture/review payloads stay in frozen inputs.
PUBLIC_TASK_FIELDS = (
    "id", "name", "url", "category", "track", "task_kind", "description", "task_prompt",
    "expected_any", "required_facts", "forbidden_any", "diagnostic_any", "min_content_chars",
    "fact_coverage_threshold", "expected_resources", "resource_output_contract",
    "content_score_applicable", "required_patterns", "acceptance_contract",
    "composite_acceptance", "mutable_body_policy", "body_requirements", "retrieval_hints",
    "source_review_url", "evaluation_url", "expected_final_url", "page_identity_required",
    "expected_document_language", "document_language_match",
    "expected_document_language_present", "target_language", "target_region",
)


def reference_bindings(value):
    """Keep body-rule structure while binding external reference payloads."""
    if isinstance(value, list):
        return [reference_bindings(item) for item in value]
    if not isinstance(value, dict):
        return value
    result = {}
    for key, item in value.items():
        if key in {"text", "source_text"}:
            if not isinstance(item, str):
                raise ValueError("Body reference text must be a string")
            result[key + "_binding"] = {
                "sha256": hashlib.sha256(item.encode()).hexdigest(), "chars": len(item)}
        else:
            result[key] = reference_bindings(item)
    return result


def public_task(case: dict) -> dict:
    task = {key: case[key] for key in PUBLIC_TASK_FIELDS if key in case}
    if "body_requirements" in task:
        task["body_requirements"] = reference_bindings(task["body_requirements"])
    benchmark = case.get("source_benchmark", {})
    routing = {key: benchmark[key] for key in
               ("mode", "hosts", "entry_path", "minimum_entries", "verification_scope")
               if key in benchmark}
    navigation = benchmark.get("risk_control", {}).get("navigation_contract")
    if navigation is not None:
        routing["risk_control"] = {"navigation_contract": navigation}
    if routing:
        task["source_benchmark"] = routing
    verification = {key: case.get("source_verification", {})[key]
                    for key in ("mime", "file_sha256") if key in case.get("source_verification", {})}
    if verification:
        task["source_verification"] = verification
    review = case.get("rule_review", {})
    if review:
        task["rule_review"] = {key: review[key] for key in ("status", "reason") if key in review}
    return task






def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def registry() -> dict:
    document = read(SUITES / "registry.json")
    if document.get("schema_version") != 1:
        raise ValueError("Unsupported suite registry")
    ids = [row["id"] for row in document["suites"]]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate suite ID")
    return document


def suite(identifier: str) -> tuple[dict, Path]:
    matches = [row for row in registry()["suites"] if row["id"] == identifier]
    if len(matches) != 1:
        raise ValueError(f"Unknown suite: {identifier}")
    entry = matches[0]
    root = contained_path(SUITES, entry.get("directory", identifier), reject_symlinks=True)
    for relative, expected in entry["files"].items():
        if not re.fullmatch(r"[0-9a-f]{64}", expected):
            raise ValueError(f"Invalid SHA-256: {relative}")
        if digest(contained_path(root, relative, reject_symlinks=True)) != expected:
            raise ValueError(f"Changed suite file: {identifier}/{relative}")
    return entry, root


def validate(identifier: str) -> dict:
    entry, root = suite(identifier)
    catalog = read(root / "dataset-catalog.json")
    tasks = read(root / "tasks.json")
    manifest = load_manifest(root / "source-inputs.json")
    if manifest['catalog'] != 'dataset-catalog.json':
        raise ValueError('Manifest must select the registry-bound task catalog')
    if not (entry["dataset_id"] == catalog["id"] == tasks["id"]):
        raise ValueError("Inconsistent dataset identity")
    declared = catalog["cases"]
    cases = tasks["cases"]
    ids = [case["id"] for case in cases]
    if (len(ids) != len(set(ids)) or ids != [case["id"] for case in declared]
            or len(ids) != entry["case_count"] or len(ids) != catalog["case_count"]):
        raise ValueError("Inconsistent task inventory")
    for task, row in zip(cases, declared):
        for key in ("id", "name", "url", "category", "track", "task_prompt"):
            if key in row and row[key] != task.get(key):
                raise ValueError(f"Task catalog mismatch: {task['id']}/{key}")
    for relative, expected in input_files(manifest).items():
        contained_path(root, relative, reject_symlinks=True)
        if not re.fullmatch(r"[0-9a-f]{64}", expected):
            raise ValueError(f"Invalid input SHA-256: {relative}")
    for path in sorted((SUITES/'annotation-revisions').glob('*.json')):
        revision = read(path)
        if identifier in revision.get('parents', {}):
            apply_annotation_revision(identifier, tasks, revision['id'])
    return {"suite": identifier, "case_count": len(ids), "dataset_sha256": catalog["dataset_sha256"]}


def input_files(manifest: dict) -> dict[str, str]:
    files = dict(manifest["files"])
    for tree, items in manifest["trees"].items():
        for relative, expected in items.items():
            name = f"{tree}/{relative}"
            if name in files:
                raise ValueError(f"Duplicate input: {name}")
            files[name] = expected
    return files


def verify_inputs(identifier: str, source: Path) -> dict:
    result = validate(identifier)
    _, root = suite(identifier)
    manifest = read(root / "source-inputs.json")
    for relative, expected in input_files(manifest).items():
        if digest(contained_path(source, relative, reject_symlinks=True)) != expected:
            raise ValueError(f"Changed frozen input: {relative}")
    raw = contained_path(source, manifest['dataset'], reject_symlinks=True).read_bytes()
    verify_catalog(root/'source-inputs.json', manifest, raw)
    dataset = json.loads(raw)
    tasks = read(root/'tasks.json')['cases']
    for case, task in zip(dataset['cases'], tasks):
        if public_task(case) != task:
            raise ValueError(f"Public task differs from frozen input: {case['id']}")
    return result


def apply_annotation_revision(identifier: str, dataset: dict, revision: str) -> dict:
    """Apply an explicit score-only version; keep its frozen parent unchanged."""
    safe_identifier(revision)
    path = contained_path(SUITES, f'annotation-revisions/{revision}.json', reject_symlinks=True)
    definition = read(path)
    if (definition.get('schema_version') != 1
            or definition.get('kind') != 'score_only_annotation_revision'
            or definition.get('id') != revision):
        raise ValueError('Unsupported annotation revision')
    from .scoring_regressions import load_scoring_regressions
    controls = definition.get('regression_ids', [])
    if not controls or set(controls) - load_scoring_regressions().keys():
        raise ValueError('Annotation revision requires registered regression controls')
    entry, root = suite(identifier)
    parent = definition.get('parents', {}).get(identifier)
    if parent != {'tasks_sha256': digest(root/'tasks.json'),
                  'source_inputs_sha256': digest(root/'source-inputs.json')}:
        raise ValueError('Annotation revision has a different frozen parent')
    if dataset.get('id') != entry['dataset_id']:
        raise ValueError('Annotation revision dataset identity differs')
    result = deepcopy(dataset)
    cases = {case['id']: case for case in result['cases']}
    allowed = {'expected_resources', 'required_facts', 'forbidden_any', 'diagnostic_any',
               'composite_acceptance', 'acceptance_contract', 'required_patterns'}
    changes = [row for row in definition['changes'] if row['suite'] == identifier]
    if not changes or len({row['case_id'] for row in changes}) != len(changes):
        raise ValueError('Annotation revision has an invalid task inventory')
    for change in changes:
        case = cases.get(change['case_id'])
        public = public_task(case) if case is not None else None
        encoded = json.dumps(public, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
        if hashlib.sha256(encoded).hexdigest() != change['before_sha256']:
            raise ValueError('Annotation revision task differs from frozen parent')
        if (set(change['set']) | set(change['remove'])) - allowed:
            raise ValueError('Annotation revision cannot change collection inputs')
        case.update(deepcopy(change['set']))
        for field in change['remove']:
            case.pop(field, None)
    result['id'] = dataset['id'] + '--' + revision
    result['definition_revision'] = {
        'id': revision, 'sha256': digest(path), 'parent_dataset_id': dataset['id'],
        'parent_tasks_sha256': parent['tasks_sha256'], 'provider_calls_added': 0,
    }
    return result


def export(identifier: str, source: Path, output: Path, *, revision: str | None = None) -> Path:
    """Copy only declared inputs after verification; never overwrite a run or input tree."""
    verify_inputs(identifier, source)
    if output.exists() or output.is_symlink():
        raise ValueError("Output must be a new directory")
    if not output.parent.is_dir():
        raise ValueError("Output parent must exist")
    _, root = suite(identifier)
    manifest = read(root / "source-inputs.json")
    stage = Path(tempfile.mkdtemp(prefix=".lexbench-", dir=output.parent))
    try:
        for relative in input_files(manifest):
            target = contained_path(stage, relative, reject_symlinks=True)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(contained_path(source, relative, reject_symlinks=True), target)
        verify_inputs(identifier, stage)
        if revision is not None:
            dataset_path = stage / manifest['dataset']
            revised = apply_annotation_revision(identifier, read(dataset_path), revision)
            dataset_path.write_text(json.dumps(revised, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        # A materialized dataset is intentionally independent of the historical
        # Browser Eval external-input resolver; do not copy source-inputs.json.
        os.rename(stage, output)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    return output / manifest["dataset"]
