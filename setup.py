#!/usr/bin/env python
from distutils.core import setup

setup(
    name='nagioscheck',
    version='0.0.1',
    description='Run nagios locally',
    author='Danny Lawrence',
    author_email='dannyla@linux.com',
    url='https://github.com/daniellawrence/nagioscheck',
    package_dir={'': 'nagioscheck'},
    packages=[''],
    #scripts=['bin/nagioscheck'],
    long_description="https://github.com/daniellawrence/nagioscheck",
)
