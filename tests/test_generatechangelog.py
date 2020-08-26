import os
import logging
import json
import unittest
import pytest
from unittest.mock import patch, MagicMock, Mock
from samsgeneratechangelog import GenerateChangelog

logging.basicConfig(level='DEBUG')
TEST_FOLDER = os.path.dirname(os.path.realpath(__file__))

ARG_PARSER = MagicMock()
for attr in ['template_file', 'old_version', 'new_verison', 'custom_attributes', 'group_pattern', 'group_by']:
    setattr(ARG_PARSER.return_value.parse_args.return_value, attr, None)


@patch('configargparse.ArgParser', new=ARG_PARSER)
@patch('git.Repo')
class TestGenerateChangelog(unittest.TestCase):

    def setUp(self):
        first_diff_commit = Mock()
        first_diff_commit.b_path = './README.MD'
        first_diff_commit.author = Mock()
        first_diff_commit.author.name='Sam Martin'

        self.mock_repo = MagicMock()
        self.mock_repo.refs.__getitem__.return_value.commit = first_diff_commit
        self.mock_repo.refs.__getitem__.return_value.commit.diff.return_value.iter_change_type.return_value = [
            first_diff_commit
        ]
        self.mock_repo.git.log.return_value = json.dumps({
            'author': {'name': 'Sam Martin'},
            'commit': 'ASDA1231ADA',
            'message': 'JRM-123 - First commit!!!'
        }) + ','
        self.default_args = {
            'old_version': '0.0.1',
            'new_version': '1.0.0',
            'custom_attributes': {
                'jira_id': {
                    'derived_from': 'message',
                    'pattern': r'^\w+-\d+'
                }
            }
        }

    def test_render_markdown(self, mock_repo):
        mock_repo.return_value = self.mock_repo

        generate_changelog = GenerateChangelog(**self.default_args)

        result = generate_changelog.render_markdown()
        print(result)
        with open(f'{TEST_FOLDER}/fixtures/basic_result.md') as reader:
            assert result == reader.read()


if __name__ == '__main__':
    pytest.main(
        ['/Users/sammartin/git/samsgeneratechangelog/tests/test_generatechangelog.py'])
