Custom Attributes Examples
---------------------------

With custom attributes you can for example group together:

* Commits by Jira ID in the message
* All Terraform files
* All files by root folder

Argument structure
^^^^^^^^^^^^^^^^^^^^^

Whether supplying your custom attributes via the cmdline arguments or when 
instantiating :class:`~samsgeneratechangelog.GenerateChangelog` you need to supply a structure as follows:

.. code-block :: json

    {
        "attribute_name": {
            "derived_from": "commit_attribute",
            "pattern": "regex pattern"
        }
    }

e.g.

.. code-block :: json

    {
        "jira_id": {
            "derived_from": "message", 
            "pattern": "^\w+-\d+"
        }
    }

Usage
^^^^^^^^^

In the example above, the :class:`~samsgeneratechangelog.FileCommit` objects (accessible 
in the template via the :code:`file_commits` variable) will be given a new attribute called :attr:`jira_id`.
This attribute will be produced by applying the pattern :code:`^\\w+-\\d+` against the 
:attr:`~samsgeneratechangelog.FileCommit.commit` object's :attr:`message` attribute.

The pattern :code:`^\\w+-\\d+` will take a commit message like:

.. code-block :: none

    JIRA-1234 - Added additional templates

and return 

.. code-block :: none

    JIRA-1234

Meaning that in your template you can do something like:

.. code-block :: none

    {%- for file_commit in file_commits %}
    - {{file_commit.jira_id}} - {{file_commit.file_path}} - {{file_commit.hexsha_short}}
    {%- endfor %}

and it will render as

.. code-block :: none

    - JIRA-1234 - samsgeneratechangelog/templates/change_type.j2 - 2f4dbc5