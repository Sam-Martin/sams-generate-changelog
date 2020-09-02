Class Reference
================

GenerateChangelog 
------------------

This is the class you are most likely to use if you want to generate a changelog from your own Python script.

.. autoclass:: samsgeneratechangelog.GenerateChangelog
   :members:
   :undoc-members:
   :show-inheritance:

GitHelper
--------------

You will only need to interact with this class if you're creating your own template builder.

.. autoclass:: samsgeneratechangelog.GitHelper
   :members:
   :undoc-members:
   :show-inheritance:

FileCommit
-----------

This is the class from which the `file_commits` objects in the templates are instantiated.
Look here for attributes which you can use directly in your Jinja2 template.

.. autoclass:: samsgeneratechangelog.FileCommit
   :members:
   :undoc-members:
   :show-inheritance: