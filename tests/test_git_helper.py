import os
import unittest
from samsgeneratechangelog import GitHelper

TEST_FOLDER = os.path.dirname(os.path.realpath(__file__))
GIT_FOLDER = os.path.join(TEST_FOLDER, '..')


class TestGitHelper(unittest.TestCase):

    def test_commit_log_does_not_return_merge_commits(self):
        gh = GitHelper(path=GIT_FOLDER)
        
        results = list(gh.commit_log(rev_a='1.0.1', rev_b='1.0.2'))

        for commit in results:
            assert len(commit.commit.parents) == 1

