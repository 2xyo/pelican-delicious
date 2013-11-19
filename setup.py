#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import os
from setuptools import setup, find_packages

try:
    here = os.path.abspath(os.path.normpath(os.path.dirname(__file__)))
    readme = open(os.path.join(here, 'README.rst')).read()
except:
    readme = """\
Pelican Delicious Bookmarks is a library to make it easy to add your
Delicious bookmarks in your Pelican blogs. """

requires = [
    'requests',
    'beautifulsoup4'
]

setup(
    name='pelican-delicious',
    version='0.0.1',
    description='Easily embed delicious bookmarks in your Pelican articles.',
    long_description=readme,
    author='Yohann Lepage',
    author_email='yohann@lepage.info',
    url='https://github.com/2xyo/pelican-delicious',
    packages=find_packages(),
    package_data={'': ['LICENSE', ]},
    package_dir={'pelican_delicious': 'pelican_delicious'},
    include_package_data=True,
    install_requires=requires,
    tests_require=['nose>=1.0'],
    test_suite='nose.collector',
    license='BSD',
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: Freely Distributable',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
    ),
)
