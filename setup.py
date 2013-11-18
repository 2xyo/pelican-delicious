#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import pelican_delicious


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    readme = f.read()

packages = [
    'pelican_delicious',
]

requires = [
    'requests',
]

setup(
    name='pelican-delicious',
    version=pelican_delicious.__version__,
    description='Easily embed delicious bookmarks in your Pelican articles.',
    long_description=readme,
    author='Yohann Lepage',
    author_email='yohann@lepage.info',
    url='https://github.com/2xyo/pelican-delicious',
    packages=packages,
    package_data={'': ['LICENSE', ]},
    package_dir={'pelican_delicious': 'pelican_delicious'},
    include_package_data=True,
    install_requires=requires,
    license='BSD',
    classifiers=(
        'Development Status :: 1 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
    ),
)