import os
import unittest
from unittest.mock import patch
import pytest
from samsgeneratechangelog.__main__ import main

TEST_FOLDER = os.path.dirname(os.path.realpath(__file__))
DEFAULT_ARGS = [
    'test.py', 'print',
    '--git-path', '..',
    '--start-ref', '0520826f8057485f8f86f7198149c7b4ea6b6aa2',
    '--end-ref', 'ac77514f027554af76506833825d418e5072a866',
    '--header-text', '1.0.0'
]
CUSTOM_TEMPLATE_ARGS = DEFAULT_ARGS.copy()
CUSTOM_TEMPLATE_ARGS.extend([
    '--template-file', 'fixtures/custom_template.j2',
    '--custom-attributes', '{"jira_id": {"derived_from": "message", "pattern": "^\\\w+-\\\d+"}}'  # noqa: W605
])


def mock_std_to_string(mock_stdout):
    """ Take a mock_stdout object and return a standardised string that will match our fixtures """
    return ''.join([str(x[0][0]) for x in mock_stdout.write.call_args_list[:-1]])


@patch('sys.stdout')
class TestConfig(unittest.TestCase):

    @patch('argparse._sys.argv', DEFAULT_ARGS)
    def test_default_args(self, mock_stdout):
        main()
        result = mock_std_to_string(mock_stdout)
        with open(f'{TEST_FOLDER}/fixtures/author_all_commits_template.md') as reader:
            assert result == reader.read()

    @patch('argparse._sys.argv', CUSTOM_TEMPLATE_ARGS)
    def test_custom_template(self, mock_stdout):
        main()
        result = mock_std_to_string(mock_stdout)
        with open(f'{TEST_FOLDER}/fixtures/jira_id_all_commits_template.md') as reader:
            assert result == reader.read()


if __name__ == '__main__':
    pytest.main([os.path.realpath(__file__)])
