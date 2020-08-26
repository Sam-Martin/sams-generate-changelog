"""
A series of helper classes for dealing with pygit
"""
import os
import re
import logging
import git
import json
from .decorators import DebugOutput

    

class FileCommits():
    """ All commits relating to a single file """

    def __init__(self, file_path, commits, change_type):
        change_types = {'A': 'Added', 'M': 'Modified', 'D': 'Deleted'}
        self.change_type = change_types[change_type]
        self.file_path=file_path
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
        self.grouped_by = grouped_by
        self._files = {}
    
    def add(self, file):
        self._files[file.file_path] = self._files.get(file.file_path, [])
        self._files[file.file_path].append(file)
    
    def get(self, file_path):
        return self._files.get(file_path)
    
    @property
    def files(self):
        return self._files.items()
    
    def __len__(self):
        return len(self.files)

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
        return ''.join([f'<samsgeneratechangelog.githelper.SimpleCommit(',
                        f'{self.raw_commit}, ',
                        f'{self.file_path}, ',
                        f'{self.custom_attributes})'
                        ])


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

    @property
    @DebugOutput
    def all_commits_by_file(self):
        """ Returns a list of all commits by file """
        result = []
        result.extend(self.new_files)
        result.extend(self.modified_files)
        result.extend(self.deleted_files)
        return result

    def get_files_of_type(self, change_type):
        """ Yield commits pertaining to files of type change_type """
        for diff in self.get_diff(change_type):
            yield FileCommits(
                file_path=diff.b_path,
                commits=self.get_file_commits(diff.b_path),
                change_type=change_type
            )

    def get_diff(self, change_type):
        """ Get the diff commits between the old_version and the new_version of type change_type """
        return self.get_commit(self.old_version).diff(self.new_version).iter_change_type(change_type)

    def get_commit(self, ref):
        """ Get a single commit from a ref """
        try:
            return self.repo.refs[ref].commit
        except IndexError:
            return self.repo.commit(ref)

    def get_file_commits(self, file_path):
        """ Get Detail about all the commits pertaining
        to a specific file between old_version and new_version """
        #   "subject": "%s",%n
        #   "body": "%b",%n
        json_format = '{%n  "commit": "%H",%n  "abbreviated_commit": "%h",%n  "tree": "%T",%n  "abbreviated_tree": "%t",%n  "parent": "%P",%n  "abbreviated_parent": "%p",%n  "refs": "%D",%n  "encoding": "%e",%n "sanitized_subject_line": "%f",%n  "commit_notes": "%N",%n  "verification_flag": "%G?",%n  "signer": "%GS",%n  "signer_key": "%GK",%n  "author": {%n    "name": "%aN",%n    "email": "%aE",%n    "date": "%aD"%n  },%n  "commiter": {%n    "name": "%cN",%n    "email": "%cE",%n    "date": "%cD"%n  }%n},'

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
    def group_commits(self, pattern, file_list, group_by='file_path'):
        """ Group commits based on the first match when the pattern is applied to the property of
        the commit specified by group_by (defaults to file_path) """
        groups = {}
        group = GroupedFiles(group_by)
        for file in file_list:
            group.add(file)
        return group

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
