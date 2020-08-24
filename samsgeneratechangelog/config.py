import os
import logging
import configargparse


class Config:

    def __init__(self, **kwargs):
        self.config = None
        self.kwargs = kwargs
        self.defaults = {
            'custom_attributes': None,
            'template_file': self._get_module_template_path('default'),
            'group_by': 'file_path',
            'group_pattern': '(.*)',
            'git_path': '.'
        }

    def register_arguments(self):
        self.arg_parser = configargparse.ArgParser(
            default_config_files=['sgc.conf'],
            description="Generate change log in Markdown"
        )
        self.arg_parser.add(
            'verb',
            nargs=1,
            choices=['print']
        )
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
            default=self.defaults['git_path'],
            env_var='SGC_git_path',
            help='The path to the root of the git repo'
        )
        self.arg_parser.add(
            '--group-pattern',
            required=False,
            default=self.defaults['group_pattern'],
            help='Regex pattern whose matching group will be used to group commits'
        )
        self.arg_parser.add(
            '--group-by',
            required=False,
            default=self.defaults['group_by'],
            help='Commit attribute to use to group commits'
        )
        self.arg_parser.add(
            '--template-file',
            required=False,
            default=self.defaults['template_file'],
            help='Jinja2 template file for changelog output'
        )
        self.config = self.arg_parser.parse_args()
        logging.debug(self.config)

    def _get_module_template_path(self, template_name):
        module_dir = os.path.dirname(os.path.realpath(__file__))
        templates_dir = 'templates'
        return os.path.sep.join([module_dir, templates_dir, f'{template_name}.j2'])

    def __getattr__(self, attr):
        if attr in self.kwargs:
            logging.debug(f"Getting {attr} from {self.__class__.name} kwargs")
            return self.kwargs[attr]
        try:
            result = getattr(self.config, attr)
            logging.debug(f"Getting {attr} from env vars/config/cmdline args")
            return result
        except AttributeError:
            logging.debug(f"Getting {attr} from defaults")
            return self.defaults.get(attr)
