Using the cmdline
------------------

Print to screen
^^^^^^^^^^^^^^^^^^

The default template is `author_by_change_type` which prints out a list of files commited grouped by auth and change type


.. include:: cmdline_snippets/default-arguments.rst


You can see that the file :code:`tests/test_default_templates.py` appears twice, once per commit.

Save to file
^^^^^^^^^^^^^^^^^^

By adding :code:`--output-file` and :code:`--entry-id` we can write the output to a markdown file.


.. include:: cmdline_snippets/default-arguments-save.rst


You can see that this adds the Markdown comment syntax with a delimiter at the beginning and end of the
changelog entry. This is invisible once rendered and ensures that running the same command repeatedly 
will *replace* the changelog entry rather than keep prepending it repeatedly.


.. note :: Note the repetition of *0.0.1* as the :code:`--var header_text` and the :code:`--entry-id`. 
    The entry ID is used as a delimiter to uniquely identify an entry in the file.


Included templates
^^^^^^^^^^^^^^^^^^^^

You can specify an alternative template (you can see a full list of templates in the 
:code:`samsgeneratechangelog/templates/` folder in the GitHub repo).

Command
"""""""""""

.. code-block :: bash

    sgc print --start-ref HEAD~3 --end-ref HEAD --var header_text 0.0.1 --template-name author_by_change_type

Outputs
"""""""""""""""
.. code-block :: none

    # 0.0.1

    ## Sam Martin's Files


    ### Added

    - tests/fixtures/custom_template.j2 - 2020-09-02 11:26:13
    - tests/test_cmdline_arguments.py - 2020-09-02 11:26:13

    ### Modified

    - docs/Makefile - 2020-09-02 10:00:21
    - docs/source/class-reference.rst - 2020-09-02 10:00:21
    - samsgeneratechangelog/__init__.py - 2020-09-02 11:26:13
    - samsgeneratechangelog/__main__.py - 2020-09-02 11:26:13
    - samsgeneratechangelog/config.py - 2020-09-02 11:26:13
    - samsgeneratechangelog/generatechangelog.py - 2020-09-02 11:26:13
    - samsgeneratechangelog/githelper.py - 2020-09-02 10:00:21
    - tests/test_default_templates.py - 2020-09-02 11:26:13


By passing the template name :code:`author_by_change_type` we can see :code:`tests/test_default_templates.py` only appears once per change type, 
showing the commit time of the latest commit for that change type. 

Custom templates & attributes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using Jinja2 you can create your own custom templates and (optionally) use your own custom attributes.

Custom attributes are values returned from a regex matching group applied to a commit parameter.

In this example we're going to match a Jira ID at the beginning of the commit message using the following JSON:

.. code-block :: json

    {
        "jira_id": {
            "derived_from": "message", 
            "pattern": "^\\w+-\\d+"
        }
    }

This will provide us a custom attribute :code:`jira_id` pulled from the commit message using the :code:`^\\w+-\\d+` pattern which will be accessible on each :code:`file_commit` object inside
the Jinja2 template. 

We will group our commits by that custom attribute, then subgroup them by change type. 
Finally we will identify the `last_commit` for each file in that change type and print 
the author and commit date for it.

.. note:: Note how we escaped the regex character classes in the pattern JSON with an 
    extra slash so :code:`^\w+-\d+` became :code:`^\\w+-\\d+`. Without this we will get a JSON parsing error.


Commits for `HEAD~9` to `HEAD~8`
""""""""""""""""""""""""""""""""""""""""""

.. code-block :: none

    ac77514 JIRA-1234 - Cleaned up unused methods
    2f4dbc5 JIRA-1234 - Added additional templates


Contents of `jira_id_by_change_type.j2`
"""""""""""""""""""""""""""""""""""""""

.. code-block :: none

    # {{header_text}}
    {%- for jira_id, jira_id_files in file_commits | groupby('jira_id') | sort(attribute='grouper')  %}

    ## {{jira_id | default('No Jira ID in commit', true)}}
    {%- for change_type, change_type_files in jira_id_files | groupby('friendly_change_type') | sort(attribute='grouper') %}

    ### {{change_type}}
    {% for file_path, file_path_files in change_type_files | groupby('file_path')  | sort(attribute='grouper')   %}
    {%- with %}
    {%- set last_commit = file_path_files | sort(attribute='committed_date') | last %}
    - {{file_path}} - {{last_commit.author.name}} - {{last_commit.committed_date}}
    {%- endwith %}
    {%- endfor %}
    {%- endfor %}
    {%- endfor %}

Command
""""""""

.. code-block :: bash

    sgc print --start-ref HEAD~9 --end-ref HEAD~8 --var header_text 0.0.1 --custom-attribute '{"jira_id": {"derived_from": "message", "pattern": "^\\w+-\\d+"}}' --template-file jira_id_by_change_type.j2 

Outputs
""""""""

.. code-block :: none

    # 0.0.1

    ## JIRA-1234

    ### Added

    - samsgeneratechangelog/templates/author.j2 - Sam Martin - 2020-09-01 17:08:02
    - samsgeneratechangelog/templates/author_single_file_entry.j2 - Sam Martin - 2020-09-01 17:08:02
    - samsgeneratechangelog/templates/change_type.j2 - Sam Martin - 2020-09-01 17:08:02
    - tests/fixtures/author_single_file_entry_template.md - Sam Martin - 2020-09-01 17:08:02
    - tests/fixtures/author_template.md - Sam Martin - 2020-09-01 17:08:02
    - tests/fixtures/change_type_template.md - Sam Martin - 2020-09-01 17:08:02

    ### Deleted

    - samsgeneratechangelog/templates/default.j2 - Sam Martin - 2020-09-01 17:08:02
    - tests/fixtures/basic_result.md - Sam Martin - 2020-09-01 17:08:02

    ### Modified

    - samsgeneratechangelog/config.py - Sam Martin - 2020-09-01 17:08:02
    - samsgeneratechangelog/generatechangelog.py - Sam Martin - 2020-09-01 17:08:02
    - samsgeneratechangelog/githelper.py - Sam Martin - 2020-09-01 17:08:02
    - tests/test_generatechangelog.py - Sam Martin - 2020-09-01 17:08:02

.. _template-variables:

Custom template variables
^^^^^^^^^^^^^^^^^^^^^^^^^^

All the templates bundled with Sam's Generate Changelog allow header text to be specified using 
:code:`--var header_text <value>`. But what if you want to add, say, a CR number to that?


.. include:: cmdline_snippets/custom-variables.rst
