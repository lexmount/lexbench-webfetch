"""Input contracts: complete versions export; corrupt, partial or unsafe inputs fail."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from lexbench_webfetch import benchmark as bench


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')
    return bench.digest(path)


class PublicDefinitions(unittest.TestCase):
    def test_all_shipped_suites_are_consistent(self):
        rows = [bench.validate(row['id']) for row in bench.registry()['suites']]
        self.assertEqual(len(rows), 4)
        self.assertEqual(sum(row['case_count'] for row in rows), 450)

    def test_nested_reference_bodies_are_bound_without_being_distributed(self):
        body = 'Third-party reference paragraph. ' * 400
        source = 'Captured source lines. ' * 300
        case = {'id': 'article', 'body_requirements': {
            'regions': [{'id': 'main', 'text': body, 'source_text': source,
                         'min_coverage': 0.9}], 'min_region_coverage': 0.8}}
        public = bench.public_task(case)
        encoded = json.dumps(public)
        self.assertNotIn(body, encoded)
        self.assertNotIn(source, encoded)
        region = public['body_requirements']['regions'][0]
        self.assertEqual(region['text_binding'], {
            'sha256': hashlib.sha256(body.encode()).hexdigest(), 'chars': len(body)})
        self.assertEqual(region['min_coverage'], 0.9)
        self.assertEqual(public['body_requirements']['min_region_coverage'], 0.8)
        self.assertEqual(case['body_requirements']['regions'][0]['text'], body)

    def test_file_acceptance_metadata_is_public_without_capture_payloads(self):
        public = bench.public_task({'source_verification': {
            'mime': 'image/png', 'file_sha256': 'a'*64, 'capture_log': 'private source capture'}})
        self.assertEqual(public['source_verification'], {'mime': 'image/png', 'file_sha256': 'a'*64})
        self.assertNotIn('private source capture', json.dumps(public))

    def test_registered_revision_keeps_original_suites_and_has_new_dataset_ids(self):
        import copy
        revision = bench.read(bench.SUITES/'annotation-revisions/serialization-20261021.json')
        changed = 0
        for identifier in revision['parents']:
            _, root = bench.suite(identifier)
            data = bench.read(root/'tasks.json');before=copy.deepcopy(data)
            new = bench.apply_annotation_revision(identifier, data, revision['id'])
            self.assertEqual(data, before)
            self.assertNotEqual(new['id'], data['id'])
            self.assertEqual(len(new['cases']), len(data['cases']))
            changed += sum(a != b for a,b in zip(new['cases'],data['cases']))
        self.assertEqual(changed, len(revision['changes']))

    def test_unknown_suite_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Unknown suite'):
            bench.validate('not-a-suite')


class FrozenInputs(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.suites = self.root / 'suites'
        self.source = self.root / 'source'
        suite = self.suites / 'synthetic'
        case = {'id': 'article', 'name': 'Article', 'url': 'https://example.test',
                'category': 'web', 'task_prompt': 'Return the article',
                'expected_any': ['unique fact'], 'ground_truth_main_content': 'unique fact'}
        data = {'id': 'test', 'name': 'Test', 'cases': [case]}
        sha = write(self.source / 'dataset.json', data)
        ref_sha = write(self.source / 'sources/article.json', {'reference': 'unique fact'})
        definition = hashlib.sha256(json.dumps(case, ensure_ascii=False, sort_keys=True,
                                               separators=(',', ':')).encode()).hexdigest()
        catalog_sha = write(suite / 'dataset-catalog.json', {
            'kind': 'frozen_dataset_catalog', 'id': 'test', 'name': 'Test', 'case_count': 1, 'dataset_sha256': sha,
            'cases': [{'id': 'article', 'name': 'Article', 'url': 'https://example.test',
                       'definition_sha256': definition}]})
        write(suite / 'tasks.json', {'id': 'test', 'cases': [{k: v for k, v in case.items()
                                                          if k != 'ground_truth_main_content'}]})
        write(suite / 'source-inputs.json', {
            'schema_version': 2, 'kind': 'frozen_reference_inputs', 'id': 'synthetic-inputs',
            'catalog': 'dataset-catalog.json',
            'catalog_sha256': catalog_sha, 'dataset_sha256': sha, 'dataset': 'dataset.json',
            'files': {'dataset.json': sha}, 'trees': {'sources': {'article.json': ref_sha}}})
        self.bind_registry()
        self.patch = patch.object(bench, 'SUITES', self.suites)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def bind_registry(self):
        suite = self.suites / 'synthetic'
        write(self.suites / 'registry.json', {'schema_version': 1, 'suites': [{
            'id': 'synthetic', 'dataset_id': 'test', 'case_count': 1,
            'files': {p.name: bench.digest(p) for p in suite.iterdir()}}]})

    def test_complete_inputs_export_without_private_extras(self):
        (self.source / 'private.log').write_text('not public')
        output = self.root / 'export'
        result = bench.export('synthetic', self.source, output)
        self.assertEqual(result, output / 'dataset.json')
        self.assertEqual({p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file()},
                         {'dataset.json', 'sources/article.json'})
        self.assertEqual(bench.verify_inputs('synthetic', output)['case_count'], 1)

    def annotation_revision(self):
        from lexbench_webfetch.scoring_regressions import load_scoring_regressions
        task = bench.read(self.suites/'synthetic/tasks.json')['cases'][0]
        encoded = json.dumps(task, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
        data = {'schema_version': 1, 'kind': 'score_only_annotation_revision',
                'id': 'source-annotation-v2', 'parents': {'synthetic': {
                    'tasks_sha256': bench.digest(self.suites/'synthetic/tasks.json'),
                    'source_inputs_sha256': bench.digest(self.suites/'synthetic/source-inputs.json')}},
                'regression_ids': [next(iter(load_scoring_regressions()))],
                'changes': [{'suite': 'synthetic', 'case_id': 'article',
                             'before_sha256': hashlib.sha256(encoded).hexdigest(),
                             'set': {'required_facts': [{'id': 'main', 'alternatives': ['unique fact']}]},
                             'remove': []}]}
        write(self.suites/'annotation-revisions/source-annotation-v2.json', data)
        return data

    def test_revised_export_has_a_distinct_identity_and_preserves_frozen_inputs(self):
        self.annotation_revision()
        before = (self.source/'dataset.json').read_bytes()
        path = bench.export('synthetic', self.source, self.root/'revised', revision='source-annotation-v2')
        revised = bench.read(path)
        self.assertEqual(revised['id'], 'test--source-annotation-v2')
        self.assertEqual(revised['definition_revision']['parent_dataset_id'], 'test')
        self.assertEqual(revised['cases'][0]['required_facts'][0]['alternatives'], ['unique fact'])
        self.assertEqual((self.source/'dataset.json').read_bytes(), before)
        self.assertEqual(bench.verify_inputs('synthetic', self.source)['case_count'], 1)
        old = bench.export('synthetic', self.source, self.root/'unchanged')
        self.assertEqual(old.read_bytes(), before)

    def test_revised_export_rejects_wrong_parent_unknown_controls_and_collection_changes(self):
        import copy
        definition = self.annotation_revision()
        for defect in ['parent', 'task', 'controls', 'collection']:
            with self.subTest(defect=defect):
                bad = copy.deepcopy(definition)
                if defect == 'parent': bad['parents']['synthetic']['tasks_sha256'] = '0'*64
                elif defect == 'task': bad['changes'][0]['before_sha256'] = '0'*64
                elif defect == 'controls': bad['regression_ids'] = ['unknown']
                else: bad['changes'][0]['set']['url'] = 'https://other.test/'
                write(self.suites/'annotation-revisions/source-annotation-v2.json', bad)
                output = self.root/defect
                with self.assertRaises(ValueError):
                    bench.export('synthetic', self.source, output, revision='source-annotation-v2')
                self.assertFalse(output.exists())

    def test_existing_output_is_preserved(self):
        output = self.root / 'existing'
        output.mkdir()
        marker = output / 'saved'
        marker.write_text('evidence')
        with self.assertRaisesRegex(ValueError, 'new directory'):
            bench.export('synthetic', self.source, output)
        self.assertEqual(marker.read_text(), 'evidence')

    def test_missing_and_changed_inputs_fail_without_export(self):
        target = self.source / 'sources/article.json'
        original = target.read_bytes()
        for replacement in (None, b'changed'):
            with self.subTest(replacement=replacement):
                if replacement is None:
                    target.unlink()
                else:
                    target.write_bytes(replacement)
                with self.assertRaises((OSError, ValueError)):
                    bench.export('synthetic', self.source, self.root / 'output')
                self.assertFalse((self.root / 'output').exists())
                target.write_bytes(original)

    def test_symlinked_input_is_rejected(self):
        target = self.source / 'sources/article.json'
        outside = self.root / 'outside.json'
        target.rename(outside)
        target.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, 'Symlinked'):
            bench.verify_inputs('synthetic', self.source)

    def test_public_acceptance_cannot_differ_from_frozen_task(self):
        path = self.suites / 'synthetic/tasks.json'
        data = bench.read(path)
        data['cases'][0]['expected_any'] = ['easier requirement']
        write(path, data)
        self.bind_registry()
        with self.assertRaisesRegex(ValueError, 'Public task differs'):
            bench.verify_inputs('synthetic', self.source)

    def test_omitting_an_acceptance_requirement_is_rejected(self):
        path = self.suites / 'synthetic/tasks.json'
        data = bench.read(path)
        del data['cases'][0]['expected_any']
        write(path, data)
        self.bind_registry()
        with self.assertRaisesRegex(ValueError, 'Public task differs'):
            bench.verify_inputs('synthetic', self.source)

    def test_task_removal_and_reordering_are_rejected(self):
        path = self.suites / 'synthetic/tasks.json'
        write(path, {'id': 'test', 'cases': []})
        self.bind_registry()
        with self.assertRaisesRegex(ValueError, 'inventory'):
            bench.validate('synthetic')

    def test_public_validation_rejects_escaping_catalog(self):
        path = self.suites / 'synthetic/source-inputs.json'
        data = bench.read(path)
        data['catalog'] = '../escape.json'
        write(path, data)
        self.bind_registry()
        with self.assertRaises(ValueError):
            bench.validate('synthetic')

    def test_public_validation_rejects_missing_manifest_identity(self):
        path = self.suites / 'synthetic/source-inputs.json'
        data = bench.read(path)
        del data['id']
        write(path, data)
        self.bind_registry()
        with self.assertRaises((ValueError, KeyError)):
            bench.validate('synthetic')

    def test_changed_shipped_file_fails(self):
        (self.suites / 'synthetic/tasks.json').write_text('{}')
        with self.assertRaisesRegex(ValueError, 'Changed suite file'):
            bench.validate('synthetic')

    def test_escaping_paths_are_rejected(self):
        for value in ('../secret', '/absolute', 'sources/../../secret', 'sources\\secret'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                bench.contained_path(self.source, value, reject_symlinks=True)


if __name__ == '__main__':
    unittest.main()
