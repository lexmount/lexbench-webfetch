"""Declared requirements compose independently of a task's reporting family."""
import pytest
from lexbench_webfetch.scoring import score_attempt
from lexbench_webfetch.metrics import task_passed


CONTRACT = {'version': 1, 'schema': 'named_link', 'minimum_records': 1,
            'hosts': ['example.test'], 'entry_path': r'/item/\d+',
            'stable_text_anchors': []}


@pytest.mark.parametrize('kind', ['body', 'structure', 'resource'])
@pytest.mark.parametrize('missing', [None, 'fact', 'resource', 'record'])
def test_every_declared_requirement_contributes_to_acceptance(kind, missing):
    case = {'url': 'https://example.test/', 'task_kind': kind,
            'acceptance_contract': CONTRACT,
            'required_facts': [{'id': 'description', 'alternatives': ['Battery lasts twelve hours']}],
            'expected_resources': [{'id': 'manual', 'urls': ['/manual.pdf']}]}
    parts = {'fact': 'Battery lasts twelve hours', 'record': '[Portable speaker](/item/1)',
             'resource': '[Manual](/manual.pdf)'}
    answer = '\n'.join(text for key, text in parts.items() if key != missing)
    metrics = score_attempt(case, answer.encode(), ok=True)
    assert task_passed(True, metrics) is (missing is None)


@pytest.mark.parametrize('answer,passed', [
    ('Home\n[Item](/item/1)\nBattery lasts twelve hours', True),
    ('Home\n[Item](/item/1)', False)])
def test_required_facts_remain_required_next_to_a_stable_contract(answer, passed):
    case = {'url': 'https://example.test/', 'acceptance_contract': CONTRACT,
            'required_facts': [{'id': 'detail', 'alternatives': ['Battery lasts twelve hours']}]}
    assert task_passed(True, score_attempt(case, answer.encode(), ok=True)) is passed


@pytest.mark.parametrize('kind', ['body', 'structure', 'resource', 'file'])
@pytest.mark.parametrize('missing', [None, 'fact', 'resource', 'record', 'file'])
def test_file_and_text_requirements_use_the_same_combination(kind, missing):
    from lexbench_webfetch.evaluation import evaluate_response
    case = {'url': 'https://example.test/', 'task_kind': kind,
            'acceptance_contract': CONTRACT,
            'required_facts': [{'id': 'description', 'alternatives': ['Battery lasts twelve hours']}],
            'expected_resources': [{'id': 'manual', 'urls': ['/manual.pdf']}]}
    parts = {'fact': 'Battery lasts twelve hours', 'record': '[Portable speaker](/item/1)',
             'resource': '[Manual](/manual.pdf)'}
    answer = '\n'.join(text for key, text in parts.items() if key != missing).encode()
    files = [] if missing == 'file' else [b'\x89PNG\r\n\x1a\n' + b'x' * 32]
    result = evaluate_response(case, answer, files=files)
    assert result['passed'] is (missing is None or (missing == 'file' and kind != 'file'))


def test_absent_requirements_are_skipped_but_missing_required_evidence_is_not():
    from lexbench_webfetch.evaluation import evaluate_response
    task = {'url': 'https://example.test/', 'task_kind': 'resource'}
    unavailable = evaluate_response(task, b'No reference or resource returned')
    assert not unavailable['passed']
    assert not unavailable['measured']
    assert unavailable['metrics']['acceptance_checks'] == {'resources': None}
    task = {'url': 'https://example.test/', 'required_facts': [
        {'id': 'body', 'alternatives': ['Article body']} ]}
    accepted = evaluate_response(task, b'Article body')
    assert accepted['passed']
    assert set(accepted['metrics']['acceptance_checks']) == {'content', 'facts'}


def test_perfect_tree_does_not_override_a_missing_content_requirement():
    import json
    case = {'url': 'https://example.test/', 'ordered_tree_reference': {'tag': 'table'},
            'ordered_tree_min_similarity': 1.0,
            'required_facts': [{'id': 'value', 'alternatives': ['Quarterly revenue']} ]}
    metrics = score_attempt(case, json.dumps(case['ordered_tree_reference']).encode(), ok=True)
    assert metrics['ordered_tree_similarity'] == 1.0
    assert not task_passed(True, metrics)


@pytest.mark.parametrize('field,value,short_answer', [
    ('expected_any', ['Required introduction'], '[Item](/item/1)'),
    ('min_content_chars', 80, '[Item](/item/1)')])
def test_declared_literal_and_length_requirements_survive_a_record_contract(field, value, short_answer):
    case = {'url': 'https://example.test/', 'acceptance_contract': CONTRACT, field: value}
    assert not task_passed(True, score_attempt(case, short_answer.encode(), ok=True))
    full = 'Required introduction with a full substantive explanation of the portable device.\n[Item](/item/1)'
    assert task_passed(True, score_attempt(case, full.encode(), ok=True))


@pytest.mark.parametrize('track', ['web', 'dynamic', 'challenge', 'risk_control', 'document', 'image', 'video'])
@pytest.mark.parametrize('language,passed', [('en', True), ('fr', False), (None, False)])
def test_declared_document_language_check_does_not_depend_on_track(track, language, passed):
    case = {'url': 'https://example.test/', 'track': track,
            'expected_final_url': 'https://example.test/',
            'expected_document_language': 'en', 'page_identity_required': True}
    metrics = score_attempt(case, b'Article body', ok=True, final_url=case['url'],
                            metadata={'document_language': language})
    assert task_passed(True, metrics) is passed


@pytest.mark.parametrize('kind', ['body', 'structure', 'resource', 'file'])
@pytest.mark.parametrize('complete', [True, False])
def test_declared_body_scope_keeps_truncation_protection_across_output_types(kind, complete):
    from lexbench_webfetch.evaluation import evaluate_response
    task = {'url': 'https://example.test/', 'task_kind': kind,
            'acceptance_contract': CONTRACT,
            'expected_resources': [{'id': 'image', 'urls': ['/image.png']}],
            'body_requirements': {'version': 1, 'unit': 'region_token_recall', 'minimum_coverage': 0.8,
                'regions': [{'id': 'body', 'text': 'alpha beta gamma delta epsilon zeta eta theta iota kappa'}]}}
    answer = ('alpha beta gamma delta epsilon zeta eta theta iota\n'
              '[Item](/item/1)\n![Image](/image.png)\n'
              '(Content truncated. Fetch a more specific URL or section for the full text.)')
    if complete:
        answer = answer.replace('theta iota\n', 'theta iota kappa\n')
    result = evaluate_response(task, answer.encode(), files=[b'\x89PNG\r\n\x1a\n'+b'x'*32])
    assert result['passed'] is complete
