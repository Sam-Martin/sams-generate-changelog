import os
import re
from datetime import date
import logging
from jinja2 import Template
from .githelper import GitHelper
from .config import get_module_template_path


class GenerateChangelog:
    """
    Generate a changelog by grouping commits and rendering them using jinja2

    Parameters
    -----------
        old_version: string
            The last version you want to diff against (must be a git ref, e.g. a tag or commit hash)
        new_version: string
            The new version you want to create (must be a git ref, e.g. a tag or commit hash)
        group_by: string
            The commit attribute to group by (defaults to file_path)
        group_pattern: regex
            The regex grouping pattern to use (defaults to `(.*)`)
        custom_attributes: dict
            A dictionary of of custom attributes to make available under each file object in the template
    """

    def __init__(self,
                 old_version, new_version, git_path='.', custom_attributes=None,
                 template_file=None, group_by='friendly_change_type', group_pattern='(.*)'):
        self.old_version = old_version
        self.new_version = new_version
        self.git_path = git_path
        self.custom_attributes = custom_attributes
        self.template_file = template_file or get_module_template_path('default')
        self.group_by = group_by
        self.group_pattern = group_pattern
        self.git_helper = GitHelper(
            self.git_path,
            self.old_version,
            self.new_version,
            self.custom_attributes
        )

    def render_markdown(self):
        """ Return the rendered markdown provided by the template """
        return self._get_markdown_template().render(
            new_version=self.new_version,
            old_version=self.old_version,
            groups=self.git_helper.group_commits(
                file_list=self.git_helper.commit_log(self.old_version, self.new_version), 
                group_by=self.group_by,
                pattern=self.group_pattern
            )
        )

    def _get_markdown_template(self):
        with open(self.template_file) as reader:
            return Template(reader.read())
