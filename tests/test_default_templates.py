import os
import time
import unittest
from unittest.mock import patch
import pytest
from .fixtures.defaults import DEFAULT_ARGS, TEST_FOLDER
from samsgeneratechangelog import GenerateChangelog


@patch.dict('os.environ', {'TZ': 'UTC'})
class TestGenerateChangelog(unittest.TestCase):

    def setUp(self):
        time.tzset()

    def test_render_markdown_change_type_all_commits_template(self):
        generate_changelog = GenerateChangelog(
            template_name='change_type_all_commits', **DEFAULT_ARGS)

        result = generate_changelog.render_markdown()

        with open(f'{TEST_FOLDER}/fixtures/change_type_all_commits_template.md') as reader:
            print(result)
            assert result == reader.read()

    def test_render_markdown_author_template(self):
        generate_changelog = GenerateChangelog(
            template_name='author_all_commits', **DEFAULT_ARGS)

        result = generate_changelog.render_markdown()

        with open(f'{TEST_FOLDER}/fixtures/author_all_commits_template.md') as reader:
            print(result)
            assert result == reader.read()

    def test_render_markdown_author_by_change_type_template(self):
        generate_changelog = GenerateChangelog(
            template_name='author_by_change_type', **DEFAULT_ARGS
        )

        result = generate_changelog.render_markdown()

        with open(f'{TEST_FOLDER}/fixtures/author_by_change_type_template.md') as reader:
            print(result)
            assert result == reader.read()

    def test_render_markdown_root_folder_all_commits_template(self):
        generate_changelog = GenerateChangelog(
            template_name='root_folder_all_commits',
            custom_attributes={
                'root_folder': {'derived_from': 'file_path', 'pattern': r'^([^/]+)/|'}
            },
            **DEFAULT_ARGS
        )

        result = generate_changelog.render_markdown()

        with open(f'{TEST_FOLDER}/fixtures/root_folder_all_commits_template.md') as reader:
            print(result)
            assert result == reader.read()

    def test_render_markdown_jira_id_all_commits_template(self):
        generate_changelog = GenerateChangelog(
            template_name='jira_id_all_commits',
            custom_attributes={
                'jira_id': {
                    'derived_from': 'message',
                    'pattern': r'^\w+-\d+'
                }
            },
            ** DEFAULT_ARGS
        )

        result = generate_changelog.render_markdown()

        with open(f'{TEST_FOLDER}/fixtures/jira_id_all_commits_template.md') as reader:
            print(result)
            assert result == reader.read()

    def test_render_markdown_jira_id_by_change_type_template(self):
        generate_changelog = GenerateChangelog(
            template_name='jira_id_by_change_type',
            custom_attributes={
                'jira_id': {
                    'derived_from': 'message',
                    'pattern': r'^\w+-\d+'
                }
            },
            ** DEFAULT_ARGS
        )

        result = generate_changelog.render_markdown()

        with open(f'{TEST_FOLDER}/fixtures/jira_id_by_change_type_template.md') as reader:
            print(result)
            assert result == reader.read()

    def test_render_markdown_jira_id_by_change_type_template_throws_without_custom_attribute(self):

        with self.assertRaises(ValueError) as cm:
            GenerateChangelog(
                template_name='jira_id_by_change_type',
                ** DEFAULT_ARGS
            )
        assert str(cm.exception) == ('jira_id_by_change_type requires a custom attribute specification'
                                     ' to be provided, please consult the documentation')

    def test_render_markdown_jira_id_all_commits_template_throws_without_custom_attribute(self):

        with self.assertRaises(ValueError) as cm:
            GenerateChangelog(
                template_name='jira_id_all_commits',
                ** DEFAULT_ARGS
            )
        assert str(cm.exception) == ('jira_id_all_commits requires a custom attribute specification'
                                     ' to be provided, please consult the documentation')

    def test_render_markdown_root_folder_all_commits_template_throws_without_custom_attribute(self):

        with self.assertRaises(ValueError) as cm:
            GenerateChangelog(
                template_name='root_folder_all_commits',
                ** DEFAULT_ARGS
            )
        assert str(cm.exception) == ('root_folder_all_commits requires a custom attribute specification'
                                     ' to be provided, please consult the documentation')

    def test_render_markdown_throws_with_unrecognised_template_name(self):

        with self.assertRaises(ValueError) as cm:
            GenerateChangelog(
                template_name='unrecognised_template',
                ** DEFAULT_ARGS
            )
        assert str(cm.exception) == ("unrecognised_template is not a template bundled with this "
                                     "version of Sam's Generate Changelog")


if __name__ == '__main__':
    pytest.main([os.path.realpath(__file__)])
