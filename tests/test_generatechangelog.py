import os
import logging
import json
import unittest
import pytest
from unittest.mock import patch, MagicMock, Mock
from .fixtures import MOCK_REPO
from samsgeneratechangelog import GenerateChangelog

# logging.basicConfig(level='DEBUG')
TEST_FOLDER = os.path.dirname(os.path.realpath(__file__))


class TestGenerateChangelog(unittest.TestCase):

    def setUp(self):
        self.default_args = {
            'old_version': '0520826f8057485f8f86f7198149c7b4ea6b6aa2',
            'new_version': 'ac77514f027554af76506833825d418e5072a866',
            'git_path': '..'
            # 'custom_attributes': {
            #     'jira_id': {
            #         'derived_from': 'message',
            #         'pattern': r'^\w+-\d+'
            #     }
            # }
        }

    def test_render_markdown_change_type_all_commits_template(self):
        generate_changelog = GenerateChangelog(
            template_name='change_type_all_commits', **self.default_args)

        result = generate_changelog.render_markdown()

        with open(f'{TEST_FOLDER}/fixtures/change_type_all_commits_template.md') as reader:
            print(result)
            assert result == reader.read()

    def test_render_markdown_author_template(self):
        generate_changelog = GenerateChangelog(
            template_name='author_all_commits', group_by='author', **self.default_args)

        result = generate_changelog.render_markdown()

        with open(f'{TEST_FOLDER}/fixtures/author_all_commits_template.md') as reader:
            print(result)
            assert result == reader.read()

    def test_render_markdown_author_by_change_type_template(self):
        generate_changelog = GenerateChangelog(
            template_name='author_by_change_type', group_by='author', **self.default_args
        )

        result = generate_changelog.render_markdown()

        with open(f'{TEST_FOLDER}/fixtures/author_by_change_type_template.md') as reader:
            print(result)
            assert result == reader.read()


if __name__ == '__main__':
    pytest.main([os.path.realpath(__file__)])
