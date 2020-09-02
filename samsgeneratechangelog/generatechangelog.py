import os
import re
from datetime import date
import logging
from jinja2 import Template
from .githelper import GitHelper
from .config import get_module_template_path


class GenerateChangelog:
    """
    Generate a changelog by rendering a simple but flexible CommitFile object using jinja2

    Parameters
    -----------
        start_ref: string
            The commit sha or git ref (tag/head/etc) that the comparison will start from
        end_ref: string
            The commit sha or git ref (tag/head/etc) that the comparison will end at
        header_text: string
            The text that appears in the header of the template
        git_path: string
            The path (relative to the cwd or absolute) that contains the `.git` folder
        template_file: string
            The path (relative to the cwd or absolute) to a custom jinja2 template file
        template_name: string
            The name of one of the templates bundled with the SamsGenerateChangelog package
        custom_attributes: dict
            A dictionary of of custom attributes to make available under each file object in the template
    """
    templates_requiring_custom_attributes = [
        'jira_id',
        'root_folder_for_all_commits'
    ]

    def __init__(self, start_ref, end_ref, header_text, git_path='.',
                 custom_attributes=None, template_file=None,
                 template_name='default'):
        self.start_ref = start_ref
        self.end_ref = end_ref
        self.header_text = header_text
        self.git_path = git_path
        self.custom_attributes = custom_attributes
        self.template_file = self._get_template_file(template_file, template_name)
        self.git_helper = GitHelper(
            self.git_path,
            self.start_ref,
            self.end_ref,
            self.custom_attributes
        )

    def _get_template_file(self, template_file, template_name):
        if template_file:
            return template_file
        if template_name in self.templates_requiring_custom_attributes and not self.custom_attributes:
            raise ValueError(f'{template_name} requires a custom attribute specification to be provided, please consult the documentation')
        return get_module_template_path(template_name)

    def render_markdown(self):
        """ Return the rendered markdown provided by the template """
        return self._get_markdown_template().render(
            start_ref=self.start_ref,
            end_ref=self.end_ref,
            header_text=self.header_text,
            file_commits=self.git_helper.commit_log(
                self.start_ref, self.end_ref)
        )

    def _get_markdown_template(self):
        with open(self.template_file) as reader:
            return Template(reader.read())
