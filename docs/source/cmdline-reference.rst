Cmdline Reference
=============================

Cmdline Arguments
^^^^^^^^^^^^^^^^^^

.. argparse::
   :module: samsgeneratechangelog.config
   :func: arg_parser
   :prog: sgc


Using --var
""""""""""""""

The argument --var expects two values separated by a space, and can be specified multiple times.

e.g.

.. code-block :: none

   sgc print --start-ref 0.0.4 --end-ref 1.0.0 --var header_text 0.0.1 --var change_number CR-1234 

Of course, the additional variables will only do anything if you have a corresponding entry in your template that does something with the variable!

See :ref:`template-variables` for more info.

Using config files
""""""""""""""""""""

All cmdline arguments can be specified in a :code:`.sgc` config file in a yaml format.

See :ref:`config-file-examples` for examples.