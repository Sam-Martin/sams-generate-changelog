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
            'new_version': '447093540a6ca4719add4d738a85fcb7f50d88be',
            'git_path': '..'
            # 'custom_attributes': {
            #     'jira_id': {
            #         'derived_from': 'message',
            #         'pattern': r'^\w+-\d+'
            #     }
            # }
        }

    def test_render_markdown_change_type_template(self):
        generate_changelog = GenerateChangelog(
            template_name='change_type', **self.default_args)

        result = generate_changelog.render_markdown()

        with open(f'{TEST_FOLDER}/fixtures/change_type_template.md') as reader:
            print(result)
            assert result == reader.read()

    def test_render_markdown_author_template(self):
        generate_changelog = GenerateChangelog(
            template_name='author', group_by='author', **self.default_args)

        result = generate_changelog.render_markdown()

        with open(f'{TEST_FOLDER}/fixtures/author_template.md') as reader:
            print(result)
            assert result == reader.read()

    def test_render_markdown_author_single_file_entry_template(self):
        generate_changelog = GenerateChangelog(
            template_name='author_single_file_entry', group_by='author', **self.default_args
        )

        result = generate_changelog.render_markdown()

        with open(f'{TEST_FOLDER}/fixtures/author_single_file_entry_template.md') as reader:
            print(result)
            assert result == reader.read()


if __name__ == '__main__':
    pytest.main([os.path.realpath(__file__)])
