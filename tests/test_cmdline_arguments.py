import os
import unittest
from unittest.mock import patch
import pytest
from .test_helper import TestMixin
from samsgeneratechangelog.__main__ import main

TEST_FOLDER = os.path.dirname(os.path.realpath(__file__))
GIT_FOLDER = os.path.join(TEST_FOLDER, '..')
DEFAULT_ARGS = [
    'test.py', 'print',
    '--git-path', GIT_FOLDER,
    '--start-ref', '0520826f8057485f8f86f7198149c7b4ea6b6aa2',
    '--end-ref', 'ac77514f027554af76506833825d418e5072a866',
    '--var', 'header_text', '1.0.0'
]
CUSTOM_TEMPLATE_ARGS = DEFAULT_ARGS.copy()
CUSTOM_TEMPLATE_ARGS.extend([
    '--template-file', os.path.join(TEST_FOLDER, 'fixtures/custom_template.j2'),
    '--custom-attributes', '{"jira_id": {"derived_from": "message", "pattern": "^\\\w+-\\\d+"}}'  # noqa: W605
])

SAVE_FILE_ARGS = DEFAULT_ARGS.copy()
SAVE_FILE_ARGS[1] = 'save'
SAVE_FILE_ARGS.extend([
    '--output-file', os.path.join(TEST_FOLDER, 'CHANGELOG.md'),
    '--entry-id', '1.0.0'
])

NO_VARS_ARGS = DEFAULT_ARGS.copy()
NO_VARS_ARGS = NO_VARS_ARGS[0:-3]


def mock_std_to_string(mock_stdout):
    """ Take a mock_stdout object and return a standardised string that will match our fixtures """
    return ''.join([str(x[0][0]) for x in mock_stdout.write.call_args_list[:-1]])


@patch('sys.stdout')
@patch.dict('os.environ', {'TZ': 'UTC'})
class TestConfig(unittest.TestCase, TestMixin):

    def setUp(self):
        self._delete_files()

    def tearDown(self):
        self._delete_files()

    @patch('argparse._sys.argv', DEFAULT_ARGS)
    def test_default_args(self, mock_stdout):
        main()
        result = mock_std_to_string(mock_stdout)
        with open(f'{TEST_FOLDER}/fixtures/author_by_change_type_template.md') as reader:
            assert result == reader.read()

    @patch('argparse._sys.argv', SAVE_FILE_ARGS)
    def test_custom_template(self, mock_stdout):
        main()

        self.assertFileContentsEqual(
            file_a='CHANGELOG.md',
            file_b=os.path.join('fixtures', 'new_file_output.md')
        )

    @patch('argparse._sys.argv', NO_VARS_ARGS)
    def test_no_vars(self, mock_stdout):
        main()

        # The first line of the default template expects an var of header_text which will not
        # be populated
        mock_std_to_string(mock_stdout)[0] == '# '


if __name__ == '__main__':
    pytest.main([os.path.realpath(__file__)])
