"""
A series of helper classes for dealing with pygit
"""
import os
import re
import logging
import git
import json
from .decorators import DebugOutput


class FileCommit():
    """ How a single file was changed by a commit """
    def __init__(self, commit, file_path, change_type, custom_attributes=None):
        change_types = {'A': 'Added', 'M': 'Modified', 'D': 'Deleted', 'R': 'Renamed', 'T': 'Type Change'}
        self.commit = commit
        self.file_path = file_path
        self.change_type = change_type
        self.custom_attributes = custom_attributes
        self.friendly_change_type = change_types.get(change_type, 'Unknown change type')

    def __getattr__(self, attr):
        """ Return the value from the commit object if the attribute 
        was one of FileCommit's directly """
        if self._get_custom_attribute(attr) is not None:
            return self._get_custom_attribute(attr)
        return getattr(self.commit, attr)
    
    def _get_custom_attribute(self, attr):
        if not self.custom_attributes or attr not in self.custom_attributes:
            return None
        attribute_spec = self.custom_attribute[attr]
        logging.debug(f"Getting custom attribute {attr} from commit"
                      f"using {attribute_spec['pattern']} against {attribute_spec['derived_from']}")
        match = re.search(
            attribute_spec['pattern'],
            getattr(self.commit, attribute_spec['derived_from']),
            re.IGNORECASE
        )
        return match[0] if match else ''
    
    def __repr__(self):
        return f"FileCommit({self.commit}, {self.file_path}, {self.change_type})"

class FileCommits():
    """ All commits relating to a single file """

    def __init__(self, file_path, commits, change_type):
        change_types = {'A': 'Added', 'M': 'Modified', 'D': 'Deleted'}
        self.change_type = change_types[change_type]
        self.file_path = file_path
        self.commits = commits

    def __getattr__(self, attr):
        """ Try and return any attribute we're
        asked for as a list of that attribute
        from our commits """
        return [
            getattr(commit, attr)
            for commit in self.commits
        ]


class GroupedFiles:
    """ Files grouped by an arbitrary parameter """

    def __init__(self, grouped_by):
        logging.debug(f'Grouping files by: {grouped_by}')
        self.grouped_by = grouped_by
        self._groups = {}

    def add(self, file):
        group_name = getattr(file, self.grouped_by)
        self._ensure_file_path(group_name, file.file_path)
        self._groups[group_name][file.file_path].append(file)

    def _ensure_file_path(self, group_name, file_path):
        self._groups[group_name] = self._groups.get(group_name, {})
        self._groups[group_name][file_path] = self._groups[group_name].get(
            file_path,
            []
        )

    def get(self, group_name):
        return self._groups.get(group_name)

    @property
    def groups(self):
        return self._groups.items()

    def __len__(self):
        return len(self.groups)


class SimpleCommit:
    """ A single commit and its attributes """

    def __init__(self, commit, file_path, custom_attributes=None):
        self.file_path = file_path
        self.commit = commit
        self.custom_attributes = custom_attributes or {}

    def __getattr__(self, attr):
        if self._get_custom_attribute(attr) is not None:
            return self._get_custom_attribute(attr)
        return getattr(self.commit, attr)

    def _get_custom_attribute(self, attr):
        if attr not in self.custom_attributes:
            return None
        attribute_spec = self.custom_attribute[attr]
        logging.debug(f"Getting custom attribute {attr} from commit"
                      f"using {attribute_spec['pattern']} against {attribute_spec['derived_from']}")
        match = re.search(
            attribute_spec['pattern'],
            getattr(self, attribute_spec['derived_from']),
            re.IGNORECASE
        )
        return match[0] if match else ''

    def __repr__(self):
        return (
            f'<samsgeneratechangelog.githelper.SimpleCommit('
            f'{self.raw_commit}, '
            f'{self.file_path}, '
            f'{self.custom_attributes})'
        )


class GitHelper:
    """
    Helper class to facilitate in diffing and organising commits
    """

    def __init__(self, path, old_commit, new_commit, custom_attributes=None):
        logging.debug(f'Using git repo {path}')
        self.repo = git.Repo(path or os.path.dirname(
            os.path.realpath(__file__)
        ))
        self.git = self.repo.git
        self.old_version = old_commit
        self.new_version = new_commit
        self.custom_attributes = custom_attributes


    @property
    @DebugOutput
    def all_commits_by_file(self):
        """ Returns a list of all commits by file """
        result = []
        result.extend(self.new_files)
        result.extend(self.modified_files)
        result.extend(self.deleted_files)
        return result

    @property
    @DebugOutput
    def new_files(self):
        """ Returns a list of added files """
        return list(self.get_files_of_type('A'))

    @property
    @DebugOutput
    def modified_files(self):
        """ Returns a list of modified files """
        return list(self.get_files_of_type('M'))

    @property
    @DebugOutput
    def deleted_files(self):
        """ Returns a list of deleted files """
        return list(self.get_files_of_type('D'))

    def get_files_of_type(self, change_type):
        """ Yield commits pertaining to files of type change_type """
        for diff in self.get_diff_files(change_type):
            yield FileCommits(
                file_path=diff.b_path,
                commits=self.get_file_commits(diff.b_path),
                change_type=change_type
            )

    def get_diff_files(self, change_type):
        """ Get the diff between the old_version and the new_version of type change_type """
        return self.get_commit(self.old_version).diff(self.new_version).iter_change_type(change_type)

    def get_commit(self, ref):
        """ Get a single commit from a ref """
        try:
            return self.repo.refs[ref].commit
        except IndexError:
            return self.repo.commit(ref)
    
    def commit_log(self, rev_a, rev_b):
        """ Get commit objects for every commit between 
        rev_a and rev_b """
        commit_ids = self.git.log('--pretty=%H', f"{rev_a}...{rev_b}").split('\n')
        for commit_id in commit_ids:
            commit = self.repo.commit(commit_id)
            for file_commit in self.generate_file_commits_from_commit(commit):
                yield file_commit
            
    
    def generate_file_commits_from_commit(self, commit):
        """ Returns a list of FileCommit objects that represent a file changed
        by the commit, as well as the change type and all other commit metadata """
        # TODO: Support generating list of files added from first commit (i.e. commit without parents)
        diff_to_parent = commit.parents[0].diff(commit)
        for change_type in diff_to_parent.change_type:
            for change in diff_to_parent.iter_change_type(change_type):
                yield FileCommit(commit, change.b_path, change_type, self.custom_attributes)


    def get_file_commits(self, file_path):
        """ Get Detail about all the commits pertaining
        to a specific file between old_version and new_version """
        json_format = '{%n  "commit": "%H"},'

        commit_diff = f'--pretty={json_format}'
        revision = f"{self.old_version}...{self.new_version}"
        raw_log_output = self.git.log(commit_diff, revision, '--', file_path)
        valid_commit_json = f'[{raw_log_output[0:-1]}]'
        try:
            return [
                SimpleCommit(
                    self.get_commit(commit['commit']),
                    file_path,
                    self.custom_attributes
                )
                for commit in json.loads(valid_commit_json)
            ]

        except json.decoder.JSONDecodeError as ex:
            logging.error(f'json.decoder.JSONDecodeError: {valid_commit_json}')
            raise ex

    @DebugOutput
    def group_commits(self, pattern, file_list, group_by):
        """ Group commits based on the first match when the pattern is applied to the property of
        the commit specified by group_by """
        groups = {}
        group = GroupedFiles(group_by)
        for file in file_list:
            group.add(file)
        return group.groups

    @staticmethod
    def get_first_regex_match(pattern, string):
        """ For a given pattern with one or more matching groups, return 
        the first successful matching group """
        match = re.search(pattern, string)
        if not match:
            return None
        return next(
            iter([result for result in match.groups() if result]),
            None
        )
