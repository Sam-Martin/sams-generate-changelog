Sam's Generate Changelog
=================================================

.. image:: https://img.shields.io/pypi/v/samsgeneratechangelog?style=flat-square   :alt: PyPI
.. image:: https://img.shields.io/github/workflow/status/sam-martin/sams-generate-changelog/Python%20package
.. image:: https://img.shields.io/requires/github/Sam-Martin/sams-generate-changelog?style=flat-square   :alt: Requires.io
.. image:: https://img.shields.io/pypi/dm/samsgeneratechangelog?style=flat-square   :alt: PyPI - Downloads
.. image:: https://img.shields.io/github/license/sam-martin/sams-generate-changelog?style=flat-square   :alt: GitHub

Yet another changelog generator!

Sam's Generate Changelog focusses on making it easy to group information about your commits by 
:attr:`~samsgeneratechangelog.FileCommit.author_date`,
:attr:`~samsgeneratechangelog.FileCommit.author`,
:attr:`~samsgeneratechangelog.FileCommit.file_path`,
:attr:`~samsgeneratechangelog.FileCommit.friendly_change_type`,
and more importantly, *custom attributes*!

This makes it easy to generate a changelog that's as simple as a list of all commits/files that changed, or as 
complicated as a list of Python files changed grouped by module and then grouped by author with their last changed
date.

Installation
----------------

.. code-block :: bash

   pip install samsgeneratechangelog

Usage
------------

.. include:: cmdline_snippets/default-arguments-save.rst


.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   examples
   cmdline-reference
   class-reference

