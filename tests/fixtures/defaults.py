import os

TEST_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
GIT_FOLDER = os.path.join(TEST_FOLDER, '..')
DEFAULT_ARGS = {
    'start_ref': '0520826f8057485f8f86f7198149c7b4ea6b6aa2',
    'end_ref': 'ac77514f027554af76506833825d418e5072a866',
    'template_variables': {'header_text': '1.0.0'},
    'git_path': GIT_FOLDER
}
