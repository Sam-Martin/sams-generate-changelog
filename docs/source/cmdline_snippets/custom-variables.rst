Command
""""""""""

.. code-block :: bash
    
    $ sgc print --start-ref 0.0.4 --end-ref 1.0.0 --var header_text 0.0.1 --var change_number CR-1234 --template-file test.j2

Contents of template_variables_example.j2
""""""""""""""""""""""""""""""""""""""""""

This template will output a list of commits, with our `header_text` followed by our `change_number` in the H1.

.. code-block :: none

    # {{header_text}} - {{change_number}}

    {%for sha, file_commit in file_commits | groupby('hexsha') | sort(attribute='list.0.committed_date') | reverse -%}
    - {{file_commit[0].hexsha_short}} - {{file_commit[0].committed_date}} - {{file_commit[0].message.split('\n')[0]}}
    {%endfor%}



Outputs
""""""""""""
.. code-block :: none

    # 0.0.1 - CR-1234

    - 9ec90ba - 2020-09-04 11:14:05 - Fix yaml
    - e3734ed - 2020-09-04 11:01:11 - Standardised docstrings with pydocstyle
    - fb785a1 - 2020-09-03 15:46:59 - Merge pull request #9 from Sam-Martin/bugfix/typo{%endfor%}

