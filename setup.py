#!/usr/bin/env python
# encoding: utf-8

"""
Python setup file.
"""

import setuptools
import os
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
        return [line.rstrip() for line in f]


def requirements_extras():
    """Open and return the other requirement files content."""
    extra = dict()

    if not os.path.isfile(_requirements_extra):
        return extra

    with open(_requirements_extra) as f:
        extra.update({
            'extras': [line.rstrip() for line in f]
        })

    return extra


base_url = 'https://github.com/aldur/RedditWallpaperChooser'
setuptools.setup(
    name='RedditWallpaperChooser',
    description='Automatically download trending wallpapers from subreddits of your choice.',
    long_description=readme(),
    version=__version__,

    url=base_url,
    download_url='{}/releases/'.format(base_url),
    license='MIT',

    author='aldur',
    author_email='adrianodl@hotmail.it',

    packages=[
        "RedditWallpaperChooser",
    ],
    install_requires=requirements(),
    extras_require=requirements_extras(),
    scripts=[os.path.join('bin', f) for f in os.listdir('bin')],

    zip_safe=False,
    include_package_data=True,

    platforms=['any'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Topic :: Desktop Environment',
        'Topic :: Multimedia',
        'Topic :: Utilities',
    ],
    keywords="Reddit subreddit wallpaper desktop"
)
