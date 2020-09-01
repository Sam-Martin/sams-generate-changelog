import json
from unittest.mock import Mock, MagicMock

MOCK_AUTHOR = Mock(spec=['name', 'email'], email='here@there.com')
MOCK_AUTHOR.configure_mock(name='Sam Martin')
FIRST_DIFF_COMMIT = Mock(**{
    'b_path': './README.MD',
    'author': MOCK_AUTHOR
})
MOCK_REPO = MagicMock(**{
    'return_value.refs.__getitem__.return_value.commit': FIRST_DIFF_COMMIT,
    'return_value.refs.__getitem__.return_value.commit.diff.return_value.iter_change_type.return_value': [
        FIRST_DIFF_COMMIT,
        FIRST_DIFF_COMMIT,
        FIRST_DIFF_COMMIT
    ],
    'return_value.git.log.return_value': json.dumps({
        'author': {'name': 'Sam Martin'},
        'commit': 'ASDA1231ADA',
        'message': 'JRM-123 - First commit!!!'
    }) + ','
})
