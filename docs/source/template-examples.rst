Template Examples
--------------------

`Sam's Generate Changelog` uses Jinja2 templates to create the changelog.
The following arguments are passed into the `Template()`.

* start_ref
* end_ref
* header_text
* file_commits

The first three are mandatory arguments when running `sgc` from the cmdline or instantiating `GenerateChangelog` 
from within a Python script.

The last one (`file_commits`) however is where the power of SamsGenerateChangelog resides.

The `file_commits` template variable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The `file_commits` variable in each template contains a list of :class:`~samsgeneratechangelog.FileCommit` objects.
This object makes you to group your changes by 
:attr:`~samsgeneratechangelog.FileCommit.author_date`,
:attr:`~samsgeneratechangelog.FileCommit.author`,
:attr:`~samsgeneratechangelog.FileCommit.file_path`,
:attr:`~samsgeneratechangelog.FileCommit.friendly_change_type`,
and more importantly, *custom attributes*.


At its most simple, you can loop over all file commits and just print out the detail about it.

.. code-block ::

    {%- for file_commit in file_commits %}
    - {{file_commit.file_path}} - {{file_commit.hexsha_short}} - {{file_commit.author.name}} {{file_commit.author.email}} - {{file_commit.committed_date}} - {{file_commit.friendly_change_type}}
    {%- endfor %}

This will output something like the following:

.. code-block ::

    - samsgeneratechangelog/templates/author.j2 - 2f4dbc5 - Sam Martin here@there.com - 2020-09-01 17:08:02 - Added
    - samsgeneratechangelog/templates/author_single_file_entry.j2 - 2f4dbc5 - Sam Martin here@there.com - 2020-09-01 17:08:02 - Added
    - samsgeneratechangelog/templates/change_type.j2 - 2f4dbc5 - Sam Martin here@there.com - 2020-09-01 17:08:02 - Added

This shows some of the attributes that are available on the `file_commits` object, but the real power of this objects 
comes from how easy it is to group!

Grouping file_commits
^^^^^^^^^^^^^^^^^^^^^^
With Jinja2's `groupby` functionality we can group these file commits any way we like.

.. code-block ::
    
    {%- for author_name, author_file_commits in file_commits | groupby('author.name') | sort(attribute='grouper') %}

    ## {{author_name}}

    {%- for file_commit in author_file_commits  | sort(attribute='file_path')  %}
    - {{file_commit.file_path}} - {{file_commit.hexsha_short}} - {{file_commit.author.name}} {{file_commit.author.email}} - {{file_commit.committed_date}} - {{file_commit.friendly_change_type}}
    {%- endfor %}    
    {%- endfor %}

Two important things to note:

1. We're grouping by `author.name` indicating the attribute :attr:`author` in the :class:`~samsgeneratechangelog.FileCommit` has its own attribute :attr:`name`
2. We're sorting by `attribute='grouper'`. The `grouper` attribute is the same as `author_name` at the beginning the for loop

This will output something like:

.. code-block ::

    ## Sam Martin
    - samsgeneratechangelog/config.py - 2f4dbc5 - Sam Martin here@there.com - 2020-09-01 17:08:02 - Modified
    - samsgeneratechangelog/generatechangelog.py - 2f4dbc5 - Sam Martin here@there.com - 2020-09-01 17:08:02 - Modified
    - samsgeneratechangelog/githelper.py - 2f4dbc5 - Sam Martin here@there.com - 2020-09-01 17:08:02 - Modified