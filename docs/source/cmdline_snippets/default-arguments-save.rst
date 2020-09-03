Command
""""""""""

.. code-block :: bash
    
    $ sgc print --start-ref HEAD~3 --end-ref HEAD --header-text 0.0.1 --output-file CHANGELOG.md --entry-id 0.0.1


Outputs to `CHANGELOG.md`
""""""""""""""""""""""""""""

.. code-block :: none
    
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