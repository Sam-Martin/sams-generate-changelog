import os
import re
from datetime import date
import logging
from jinja2 import Template
from .githelper import GitHelper
from .config import Config

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
        grouping_pattern: regex
            The regex grouping pattern to use (defaults to `(.*)`)
        custom_attributes: dict
            A dictionary of of custom attributes to make available under each file object in the template
    """

    def __init__(self, **kwargs):
        """
        
        """
        self.config = Config(**kwargs)
        self.git_helper = GitHelper(
            self.config.git_path,
            self.config.old_version,
            self.config.new_version,
            self.config.custom_attributes
        )
    
    def render_markdown(self):
        """ Return the rendered markdown provided by the template """
        return self._get_markdown_template().render(
            new_version=self.config.new_version,
            old_version=self.config.old_version,
            new_files=self.git_helper.new_files,
            modified_files=self.git_helper.modified_files,
            deleted_files=self.git_helper.deleted_files,
        )
    
    def _get_markdown_template(self):
        with open(self.config.template_file) as reader:
            return Template(reader.read())