import os
import configargparse


def get_module_template_path(template_name):
    module_dir = os.path.dirname(os.path.realpath(__file__))
    templates_dir = 'templates'
    return os.path.sep.join([module_dir, templates_dir, f'{template_name}.j2'])


ARG_PARSER = configargparse.ArgParser(
    default_config_files=['sgc.conf'],
    description="Generate change log in Markdown"
)
ARG_PARSER.add(
    'verb',
    choices=['print'],
    default='print'
)
ARG_PARSER.add(
    '--config-file',
    required=False,
    help='The path to an sgc.conf file'
)
ARG_PARSER.add(
    '--old-version',
    env_var='SGC_old_version',
    required=True,
    help='The git ref (e.g. a tag) of the old version'
)
ARG_PARSER.add(
    '--new-version',
    env_var='SGC_new_version',
    required=True,
    help='The git ref (e.g. a tag) of the new version'
)
ARG_PARSER.add(
    '--git-path',
    required=False,
    default='.',
    env_var='SGC_git_path',
    help='The path to the root of the git repo'
)
ARG_PARSER.add(
    '--group-pattern',
    required=False,
    default=r'(.*)',
    help='Regex pattern whose matching group will be used to group commits'
)
ARG_PARSER.add(
    '--group-by',
    required=False,
    default='file_path',
    help='Commit attribute to use to group commits'
)
ARG_PARSER.add(
    '--template-file',
    required=False,
    default=None,
    help='Jinja2 template file for changelog output'
)
ARG_PARSER.add(
    '--template-name',
    required=False,
    default='default',
    help='Name of a bundled Jinja2 template for changelog output',
    choices=['default', 'change_type', 'author',],
)
ARG_PARSER.add(
    '--log-level',
    required=False,
    default='WARN',
    choices=['ERROR', 'WARN', 'INFO', 'DEBUG'],
    help='Log level'
)

