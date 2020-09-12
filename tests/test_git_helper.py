import unittest
from unittest.mock import Mock
from .fixtures.defaults import GIT_FOLDER
from samsgeneratechangelog.githelper import FileCommit, GitHelper


class TestGitHelper(unittest.TestCase):

    def test_commit_log_does_not_return_merge_commits(self):
        gh = GitHelper(path=GIT_FOLDER)

        results = list(gh.commit_log(rev_a='1.0.1', rev_b='1.0.2'))

        for commit in results:
            assert len(commit.commit.parents) == 1


class TestFileCommit(unittest.TestCase):

    def test_properties(self):
        mock_commit = Mock()
        fc = FileCommit(mock_commit, 'README.md', 'M', Mock())

        assert fc.file_path == 'README.md'
        assert fc.friendly_change_type == 'Modified'
        self.assertIsInstance(fc.author.name, Mock)

    def test_custom_properties(self):
        mock_commit = Mock()
        mock_commit.message = 'JIRA-1234 - My first commit'
        fc = FileCommit(
            mock_commit,
            'README.md',
            'M',
            Mock(),
            {'jira_id': {'derived_from': 'message', 'pattern': r'^\w+-\d+'}}
        )

        assert fc.jira_id == 'JIRA-1234'

    def test_custom_properties_matching_groups(self):
        mock_commit = Mock()
        mock_commit.message = 'My first commit - JIRA-1234'
        fc = FileCommit(
            mock_commit,
            'README.md',
            'M',
            Mock(),
            {'jira_id': {'derived_from': 'message', 'pattern': r'^\w+-(\d+)|\w+-(\d+)$'}}
        )

        assert fc.jira_id == '1234'

    def test_custom_properties_multiple_matching_groups_first_group_matches(self):
        mock_commit = Mock()
        mock_commit.message = 'JIRA-1234 - My first commit - JIRA-5678'
        fc = FileCommit(
            mock_commit,
            'README.md',
            'M',
            Mock(),
            {'jira_id': {'derived_from': 'message', 'pattern': r'^(\w+-\d+)|(\w+-\d+)$'}}
        )

        assert fc.jira_id == 'JIRA-1234'

    def test_custom_properties_multiple_matching_groups_second_group_matches(self):
        mock_commit = Mock()
        mock_commit.message = 'My first commit - JIRA-5678'
        fc = FileCommit(
            mock_commit,
            'README.md',
            'M',
            Mock(),
            {'jira_id': {'derived_from': 'message', 'pattern': r'^(\w+-\d+)|(\w+-\d+)$'}}
        )

        assert fc.jira_id == 'JIRA-5678'

    def test_custom_properties_multiple_matching_groups_no_group_matches(self):
        mock_commit = Mock()
        mock_commit.message = 'My first commit '
        fc = FileCommit(
            mock_commit,
            'README.md',
            'M',
            Mock(),
            {'jira_id': {'derived_from': 'message', 'pattern': r'^(\w+-\d+)|(\w+-\d+)$'}}
        )

        assert fc.jira_id == ''
