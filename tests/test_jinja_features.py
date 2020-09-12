import os
import unittest
from unittest.mock import patch
from .fixtures.defaults import DEFAULT_ARGS, TEST_FOLDER
from .test_helper import TestMixin
from samsgeneratechangelog import GenerateChangelog


@patch.dict('os.environ', {'TZ': 'UTC'})
class TestJinjaFeatures(unittest.TestCase, TestMixin):

    def setUp(self):
        self._delete_files()

    def tearDown(self):
        self._delete_files()

    def test_template_includes(self):
        gc = GenerateChangelog(**DEFAULT_ARGS, **{
            'template_file': os.path.join(TEST_FOLDER, 'fixtures', 'template_with_includes.j2')
        })

        result = gc.render_markdown()

        assert result == "# I AM INCLUSIVE\n## I AM INCLUDED"

    def test_expression_statements(self):
        gc = GenerateChangelog(**DEFAULT_ARGS, **{
            'template_file': os.path.join(TEST_FOLDER, 'fixtures', 'template_expression_statement.j2')
        })

        result = gc.render_markdown()

        assert result == "I appended successfully"
