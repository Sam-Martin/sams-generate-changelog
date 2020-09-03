import os
TEST_FOLDER = os.path.dirname(os.path.realpath(__file__))


class TestMixin:

    def _delete_files(self):
        for file in ['CHANGELOG.md', 'CHANGELOG-existing.md']:
            try:
                os.remove(os.path.join(TEST_FOLDER, file))
            except FileNotFoundError:
                pass

    def assertFileContentsEqual(self, file_a, file_b):
        with open(os.path.join(TEST_FOLDER, file_a)) as reader:
            result = reader.read()
        with open(os.path.join(TEST_FOLDER, file_b)) as reader:
            expected_result = reader.read()

        print(result)
        assert result == expected_result
