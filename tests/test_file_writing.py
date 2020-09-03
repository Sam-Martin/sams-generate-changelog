import os
import unittest
from unittest.mock import patch
import logging
import pytest
from .test_helper import TestMixin
from samsgeneratechangelog import GenerateChangelog

logging.basicConfig(level='DEBUG')

TEST_FOLDER = os.path.dirname(os.path.realpath(__file__))
DEFAULT_ARGS = {
    'start_ref': '0520826f8057485f8f86f7198149c7b4ea6b6aa2',
    'end_ref': 'ac77514f027554af76506833825d418e5072a866',
    'header_text': '1.0.0',
    'git_path': os.path.join(TEST_FOLDER, '..')
}


@patch.dict('os.environ', {'TZ': 'UTC'})
class TestFileWriting(unittest.TestCase, TestMixin):

    def setUp(self):
        self._delete_files()

    def tearDown(self):
        self._delete_files()

    def test_render_markdown_to_new_file(self):
        gc = GenerateChangelog(**DEFAULT_ARGS)

        gc.render_markdown_to_file(
            file_path=os.path.join(TEST_FOLDER, 'CHANGELOG.md'),
            entry_id='1.0.0'
        )

        self.assertFileContentsEqual(
            file_a='CHANGELOG.md',
            file_b=os.path.join('fixtures', 'new_file_output.md')
        )

    def test_render_markdown_to_existing_file(self):
        gc = GenerateChangelog(**DEFAULT_ARGS)

        gc.render_markdown_to_file(
            file_path=os.path.join(TEST_FOLDER, 'CHANGELOG-existing.md'),
            entry_id='1.0.0'
        )
        gc.render_markdown_to_file(
            file_path=os.path.join(TEST_FOLDER, 'CHANGELOG-existing.md'),
            entry_id='2.0.0'
        )
        gc.render_markdown_to_file(
            file_path=os.path.join(TEST_FOLDER, 'CHANGELOG-existing.md'),
            entry_id='3.0.0'
        )
        gc.render_markdown_to_file(
            file_path=os.path.join(TEST_FOLDER, 'CHANGELOG-existing.md'),
            entry_id='1.0.0'
        )

        self.assertFileContentsEqual(
            file_a='CHANGELOG-existing.md',
            file_b=os.path.join('fixtures', 'existing_file_overwrite_output.md')
        )


if __name__ == '__main__':
    pytest.main([os.path.realpath(__file__)])
