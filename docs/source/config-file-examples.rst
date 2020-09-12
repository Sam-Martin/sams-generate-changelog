.. _config-file-examples:

Using config files
---------------------------

By default SamsGenerateChangelog will look for a yaml config file named :code:`.sgc` in the current working directory.
You can use all *named* arguments you would supply to the cmdline as key names in the config file.

Example :code:`.sgc` with custom attributes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block :: none

    output-file: CHANGELOG.md
    template-name: jira_id_all_commits
    custom-attributes: |
        {
            "jira_id": {
                "derived_from": "message",
                "pattern": "^\\w+-\\d+"
            }
        }

.. Note :: Note the :code:`|` character after :code:`custom-attributes:`, this indicates a multi-line string 
    (a JSON string specifically) that will be passed to the argument :code:`--custom-attributes` as a single line string.