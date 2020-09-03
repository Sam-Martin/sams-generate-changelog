
# Sam's Changelog Generator

Yet another changelog generator!

Sam’s Changelog Generator focusses on making it easy to group information about your commits by `author_date`, `author`, `file_path`, `friendly_change_type`, and more importantly, custom attributes!

This makes it easy to generate a changelog that’s as simple as a list of all commits/files that changed, or as complicated as a list of Python files changed grouped by module and then grouped by author with their last changed date.

# Documentation

For full documentation go to [ReadTheDocs](https://sams-generate-changelog.readthedocs.io/en/latest/).

# Installation

```
pip install samsgeneratechangelog
```

# Usage

## Command

```
$ sgc print --start-ref HEAD~3 --end-ref HEAD --header-text 0.0.1 --output-file CHANGELOG.md --entry-id 0.0.1
```

## Outputs to CHANGELOG.md

```
# 0.0.1

[//]: # (SamsGenerateChangelog-0.0.1)
 # 0.0.1

 ## Sam Martin's Files


 ### Added

 - tests/fixtures/custom_template.j2 - 2020-09-02 11:26:13
 - tests/test_cmdline_arguments.py - 2020-09-02 11:26:13

 ### Modified

 - samsgeneratechangelog/__init__.py - 2020-09-02 11:26:13
 - samsgeneratechangelog/__main__.py - 2020-09-02 11:26:13
 - samsgeneratechangelog/config.py - 2020-09-02 11:26:13
 - samsgeneratechangelog/generatechangelog.py - 2020-09-02 11:26:13
 - tests/test_default_templates.py - 2020-09-02 11:26:13
 [//]: # (SamsGenerateChangelog-0.0.1)
```
