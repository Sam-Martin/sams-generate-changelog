import os
import re
import logging
from jinja2 import Template
from .githelper import GitHelper

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATES_DIR = os.path.sep.join([MODULE_DIR, 'templates'])


class GenerateChangelog:
    """
    Generate a changelog by rendering a simple but flexible CommitFile object using jinja2

    Parameters:
        start_ref (string): The commit sha or git ref (tag/head/etc) that the comparison will start from
        end_ref (string): The commit sha or git ref (tag/head/etc) that the comparison will end at
        header_text (string): The text that appears in the header of the template
        git_path (string): The path (relative to the cwd or absolute) that contains the `.git` folder
        template_file (string): The path (relative to the cwd or absolute) to a custom jinja2 template file
        template_name (string): The name of one of the templates bundled with the SamsGenerateChangelog package
        custom_attributes (dict): A dictionary of of custom attributes to make available under each file object
            in the template
    """
    markdown_comment_syntax = '[//]: # ({comment_value})'
    templates_requiring_custom_attributes = [
        'jira_id_all_commits',
        'jira_id_by_change_type',
        'root_folder_all_commits'
    ]

    def __init__(self, start_ref, end_ref, header_text, git_path='.',
                 custom_attributes=None, template_file=None,
                 template_name='author_by_change_type'):
        self.start_ref = start_ref
        self.end_ref = end_ref
        self.header_text = header_text
        self.git_path = git_path
        self.custom_attributes = custom_attributes
        self.template_file = self._get_template_file(
            template_file, template_name)
        self.git_helper = GitHelper(
            self.git_path,
            self.custom_attributes
        )

    @classmethod
    def get_template_names(cls):
        """ Returns a list of valid template names """
        return [
            os.path.splitext(file_name)[0]
            for file_name in os.listdir(TEMPLATES_DIR)
            if os.path.isfile(os.path.join(TEMPLATES_DIR, file_name))
        ]

    def _get_template_file(self, template_file, template_name):
        if template_file:
            return template_file
        if template_name in self.templates_requiring_custom_attributes and not self.custom_attributes:
            raise ValueError(
                f'{template_name} requires a custom attribute specification to be provided,'
                ' please consult the documentation'
            )
        return self._get_module_template_path(template_name)

    @staticmethod
    def _get_module_template_path(template_name):
        file_path = os.path.sep.join([TEMPLATES_DIR, f'{template_name}.j2'])
        if not os.path.isfile(file_path):
            raise ValueError(
                f"{template_name} is not a template bundled with this version of Sam's Generate Changelog")
        return file_path

    def render_markdown(self):
        """ Return the rendered markdown provided by the template """
        return self._get_markdown_template().render(
            start_ref=self.start_ref,
            end_ref=self.end_ref,
            header_text=self.header_text,
            file_commits=self.git_helper.commit_log(
                self.start_ref, self.end_ref)
        )

    def render_markdown_to_file(self, file_path, entry_id):
        old_contents = self._get_file_contents(file_path)
        new_entry = self.render_markdown()
        pattern = self._get_pattern_to_match_existing_changelog_entry(entry_id)

        if re.search(pattern, old_contents):
            logging.debug(f"Found existing changelog entry for {entry_id} in {file_path}, replacing it.")
            new_contents = self._replace_existing_entry(
                repl=new_entry,
                string=old_contents,
                entry_id=entry_id
            )
        else:
            new_contents = f'{self._delimit_entry(new_entry, entry_id)}\n\n{old_contents}'
        self._overwrite_file(file_path, new_contents)

    def _delimit_entry(self, entry, entry_id):
        entry_delimiter = self._generate_entry_delimiter(entry_id)
        return f"{entry_delimiter}\n{entry}\n{entry_delimiter}"

    def _replace_existing_entry(self, repl, string, entry_id):
        """ Replace all text delimited by entry_id delimiter
        in string with repl

        Parameters:
            repl (str): The replacement string
            string (str): The string to search
            entry_id (str): The ID to use as a delimiter for the changelog entry (usually semantic version number)
        """
        pattern = self._get_pattern_to_match_existing_changelog_entry(entry_id)
        return re.sub(pattern, self._delimit_entry(repl, entry_id), string)

    def _get_pattern_to_match_existing_changelog_entry(self, entry_id):
        entry_delimiter = self._generate_entry_delimiter(entry_id)
        escaped_entry_delimiter = re.escape(entry_delimiter)
        return re.compile(f'{escaped_entry_delimiter}.*?{escaped_entry_delimiter}', re.DOTALL)

    def _generate_entry_delimiter(self, entry_id):
        """ Generate a markdown comment that will serve as a delimiter
        that denotes the start and end of a changelog entry """
        return self.markdown_comment_syntax.format(
            comment_value=F"SamsGenerateChangelog-{entry_id}"
        )

    @staticmethod
    def _get_file_contents(file_path):
        try:
            with open(file_path, 'r+') as file:
                return file.read()
        except IOError:
            return ''

    @staticmethod
    def _overwrite_file(file_path, contents):
        with open(file_path, 'w') as file:
            file.write(contents)

    def _get_markdown_template(self):
        with open(self.template_file) as reader:
            return Template(reader.read())
