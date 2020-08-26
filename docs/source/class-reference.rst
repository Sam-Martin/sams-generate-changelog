Class Reference
================

GenerateChangelog 
------------------

.. autoclass:: samsgeneratechangelog.GenerateChangelog
   :members:
   :undoc-members:
   :show-inheritance:

Simple Example
^^^^^^^^^^^^^^^^

.. code-block :: python

    # print_changelog.py
    from samsgeneratechangelog import GenerateChangelog
    gc = GenerateChangelog(
        old_version='0.0.1',
        new_version='1.0.0'
    )
    print(gc.render_markdown())

Custom Template Example
^^^^^^^^^^^^^^^^^^^^^^^^^

**changelog_template.j2**

.. code-block :: python


    ## New Files

    {%- for file in new_files %}
    - {{file.file_path}} - {{file.author | map(attribute='name') | unique | join(', ')}}
    {%- endfor%}

    # Modified Files

    {%- for file in modified_files %}
    - {{file.file_path}} - {{file.author | map(attribute='name') | unique | join(', ')}}
    {%- endfor%}

    # Deleted Files

    {%- for file in deleted_files %}
    - {{file.file_path}} - {{file.author | map(attribute='name') | unique | join(', ')}}
    {%- endfor%}


**print_example.py**

.. code-block :: python

    from samsgeneratechangelog import GenerateChangelog
    gc = GenerateChangelog(
        old_version='0.0.1',
        new_version='1.0.0',
        template_file='changelog_template.j2'
    )
    print(gc.render_markdown())

