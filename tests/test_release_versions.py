"""Release compatibility follows workload and scoring, not labels alone."""
from copy import deepcopy
import json

import pytest

from lexbench_webfetch.versions import (
    compare_releases, create_release, freeze_release, verify_release,
)


def dataset(track="web"):
    return {"id": "sample", "cases": [{
        "id": "first", "url": "https://example.test/a", "track": track,
        "task_prompt": "Return the full article.",
        "required_facts": [{"id": "topic", "alternatives": ["complete body"]}],
        "ground_truth_main_content": "complete body",
    }]}


def release(data=None, version="1.0.0", **kwargs):
    return create_release(data or dataset(), benchmark="sample-benchmark",
                          version=version, **kwargs)


@pytest.mark.parametrize("track", ["web", "dynamic", "challenge", "risk_control", "articles", "document"])
def test_identical_measurement_remains_comparable_across_documentation_patch(track):
    before = dataset(track)
    first = release(before)
    after = deepcopy(before)
    after["name"] = "A clearer report name"
    after["cases"][0]["name"] = "A clearer task label"
    second = release(after, "1.0.1", previous=first)
    assert compare_releases(first, second)["mode"] == "direct"
    verify_release(second, after)


@pytest.mark.parametrize("change", ["add", "remove", "url", "prompt", "scope", "route"])
def test_workload_changes_require_a_major_release(change):
    before = dataset()
    before["cases"].append({**deepcopy(before["cases"][0]), "id": "second"})
    after = deepcopy(before)
    if change == "add":
        after["cases"].append({**deepcopy(after["cases"][0]), "id": "third"})
    elif change == "remove":
        after["cases"].pop()
    elif change == "url":
        after["cases"][0]["url"] += "/different"
    elif change == "prompt":
        after["cases"][0]["task_prompt"] = "Return only the heading."
    elif change == "scope":
        after["cases"][0]["task_kind"] = "file"
    else:
        after["cases"][0]["retrieval_hints"] = {"wait_until": "selector", "selector": ".body"}
    first = release(before)
    with pytest.raises(ValueError, match="major"):
        release(after, "1.1.0", previous=first, change_note="New task scope")
    second = release(after, "2.0.0", previous=first, change_note="New task scope")
    assert compare_releases(first, second)["mode"] == "separate"


@pytest.mark.parametrize("field,value", [
    ("required_facts", [{"id": "topic", "alternatives": ["complete body", "equivalent body"]}]),
    ("ground_truth_main_content", "corrected body"),
    ("body_requirements", {"regions": [{"id": "body", "text": "corrected body"}]}),
])
def test_scoring_corrections_require_minor_version_and_rescore(field, value):
    first = release()
    after = dataset()
    after["cases"][0][field] = value
    with pytest.raises(ValueError, match="minor"):
        release(after, "1.0.1", previous=first, change_note="Correct independently reviewed text")
    with pytest.raises(ValueError, match="change note"):
        release(after, "1.1.0", previous=first)
    second = release(after, "1.1.0", previous=first, change_note="Correct independently reviewed text")
    assert compare_releases(first, second)["mode"] == "rescore"


def test_scorer_changes_cannot_silently_relabel_old_scores():
    first = release(scoring_source_sha256="a" * 64)
    with pytest.raises(ValueError, match="minor"):
        release(version="1.0.1", previous=first, scoring_source_sha256="b" * 64)
    second = release(version="1.1.0", previous=first,
                     scoring_source_sha256="b" * 64, change_note="Fix serialization matching")
    assert compare_releases(first, second)["mode"] == "rescore"
    with pytest.raises(ValueError, match="scoring source"):
        verify_release(first, dataset(), scoring_source_sha256="b" * 64)


def test_same_version_cannot_name_different_contracts():
    first = release()
    after = dataset()
    after["cases"][0]["required_facts"] = []
    with pytest.raises(ValueError, match="reused"):
        compare_releases(first, release(after))


def test_different_benchmarks_and_majors_are_separate_even_when_inputs_match():
    first = release()
    other = create_release(dataset(), benchmark="another-benchmark", version="1.0.0")
    assert compare_releases(first, other)["mode"] == "separate"
    assert compare_releases(first, release(version="2.0.0"))["mode"] == "separate"


@pytest.mark.parametrize("version", ["latest", "1.0", "01.0.0", "1.0.0-dev", "1.0.-1"])
def test_mutable_or_ambiguous_version_labels_are_rejected(version):
    with pytest.raises(ValueError, match="version"):
        release(version=version)


def test_dataset_drift_and_duplicate_ids_are_rejected():
    first = release()
    after = dataset()
    after["cases"][0]["required_facts"] = []
    with pytest.raises(ValueError, match="dataset"):
        verify_release(first, after)
    after["cases"].append(deepcopy(after["cases"][0]))
    with pytest.raises(ValueError, match="unique"):
        release(after)


def test_freeze_is_exclusive_and_manifest_is_portable(tmp_path):
    source = tmp_path / "dataset.json"
    source.write_text(json.dumps(dataset()))
    target = tmp_path / "benchmark-release.json"
    freeze_release(source, target, benchmark="sample-benchmark", version="1.0.0")
    frozen = json.loads(target.read_text())
    verify_release(frozen, dataset())
    assert str(tmp_path) not in target.read_text()
    with pytest.raises(FileExistsError):
        freeze_release(source, target, benchmark="sample-benchmark", version="1.0.1")
    link = tmp_path / "link.json"
    link.symlink_to(source)
    with pytest.raises(ValueError, match="symlink"):
        freeze_release(link, tmp_path / "another.json", benchmark="sample-benchmark", version="1.0.0")


def test_public_cli_freezes_and_compares_real_files(tmp_path, capsys, monkeypatch):
    from lexbench_webfetch.cli import main
    source = tmp_path / "dataset.json"
    source.write_text(json.dumps(dataset()))
    frozen = tmp_path / "release.json"
    monkeypatch.setattr("sys.argv", ["lexbench-webfetch", "release", "--dataset", str(source),
                                    "--output", str(frozen), "--benchmark", "sample-benchmark",
                                    "--version", "1.0.0"])
    main()
    assert json.loads(capsys.readouterr().out)["version"] == "1.0.0"
    monkeypatch.setattr("sys.argv", ["lexbench-webfetch", "compare-releases", str(frozen), str(frozen)])
    main()
    assert json.loads(capsys.readouterr().out)["mode"] == "direct"
