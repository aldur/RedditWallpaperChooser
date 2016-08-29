#!/usr/bin/env python
# encoding: utf-8

"""
Python setup file.
"""

import setuptools
import os.path

from RedditWallpaperChooser import __version__

__author__ = 'aldur'

_readme = "README.md"
_requirements = "requirements.txt"
_requirements_extra = "requirements_extra.txt"


def readme():
    """Open and return the _readme contents."""
    if not os.path.isfile(_readme):
        return ""

    with open(_readme) as f:
        return f.read()


def requirements():
    """Open and return the _requirements contents."""
    if not os.path.isfile(_requirements):
        return []

    with open(_requirements) as f:
        return [line.rstrip().split("==")[0] for line in f]


def requirements_extras():
    """Open and return the other requirement files content."""
    extra = dict()

    if not os.path.isfile(_requirements_extra):
        return extra

    with open(_requirements_extra) as f:
        extra.update({
            'extras':
            [line.rstrip().split("==")[0] for line in f]
        })

    return extra


setuptools.setup(
    name='RedditWallpaperChooser',
    description='Automatically download the most trending wallpapers from subreddits of your choice.',
    long_description=readme(),
    version=__version__,

    url='https://github.com/aldur/RedditWallpaperChooser',
    license='MIT',

    author='aldur',
    author_email='adrianodl@hotmail.it',

    packages=[
        "RedditWallpaperChooser",
    ],
    install_requires=requirements(),
    extras_require=requirements_extras(),
    scripts=[
        "bin/RedditWallpaperChooser"
    ],

    zip_safe=False,
    include_package_data=True,

    # TODO: include classifiers and keywords.
)
