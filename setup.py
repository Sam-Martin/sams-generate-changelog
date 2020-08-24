#!/usr/bin/env python

from distutils.core import setup

setup(
    name='samsgeneratechangelog', 
    description='Let Sam generate a changelog for you by grouping commits by file, or commit message, or anything!',
    author='Sam Martin', 
    author_email='samjackmartin+sams_generate_changelog@gmail.com', 
    url='https://github.com/Sam-Martin/sams-generate-changelog',
    install_request=['jinja2', 'configargparse', 'gitpython'],
    package_data={
        "": ["templates/*.j2"],
    },
    entry_points={
        'console_scripts': ['sgc=samsgeneratechngelog.__main:main']
    }

)