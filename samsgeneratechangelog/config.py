import os
import logging
import configargparse


class Config:

    def __init__(self, **kwargs):
        kwargs_defaults = {
            'custom_attributes': None,
        }
        self.kwargs = {**kwargs_defaults, **kwargs}
        self.arg_parser = configargparse.ArgParser(
            default_config_files=['sgc.conf'],
            description="Generate change log in Markdown"
        )
        self.register_arguments()

    def register_arguments(self):
        self.arg_parser.add(
            '--config-file',
            required=False,
            help='The path to an sgc.conf file'
        )
        self.arg_parser.add(
            '--old-version',
            env_var='SGC_old_version',
            required=True,
            help='The git ref (e.g. a tag) of the old version'
        )
        self.arg_parser.add(
            '--new-version',
            env_var='SGC_new_version',
            required=True,
            help='The git ref (e.g. a tag) of the new version'
        )
        self.arg_parser.add(
            '--git-path',
            required=False,
            default='.',
            env_var='SGC_git_path',
            help='The path to the root of the git repo'
        )
        self.arg_parser.add(
            '--group-pattern',
            required=False,
            default=r'(.*)',
            help='Regex pattern whose matching group will be used to group commits'
        )
        self.arg_parser.add(
            '--group-by',
            required=False,
            default='file_path',
            help='Commit attribute to use to group commits'
        )
        self.arg_parser.add(
            '--template-file',
            required=False,
            default=self._get_module_template_path('default'),
            help='Jinja2 template file for changelog output'
        )
        self.args = self.arg_parser.parse_args()

    def _get_module_template_path(self, template_name):
        module_dir = os.path.dirname(os.path.realpath(__file__))
        templates_dir = 'templates'
        return os.path.sep.join([module_dir, templates_dir, f'{template_name}.j2'])

    def __getattr__(self, attr):
        if attr in self.args:
            return getattr(self.args, attr)
        return None
