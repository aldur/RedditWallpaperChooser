#!/usr/bin/env python
# encoding: utf-8

"""The constants."""

from RedditWallpaperChooser import __version__

__author__ = 'aldur'

# Reddit UserAgent.
REDDIT_USER_AGENT = \
    "unix:RedditWallpaperChooser:{}" \
    "(by /u/aldur999)".format(__version__)

# Reddit API format string
REDDIT_API_FORMAT_URL = \
    "https://www.reddit.com/r/{}/{}/.json"

# Allowed sorting options
REDDIT_ALLOWED_SORTING = [
    'top', 'new', 'hot', 'controversial'
]

# Options requiring a time parameter
REDDIT_NEED_TIME = [
    'top', 'controversial'
]

# Allowed time options
REDDIT_ALLOWED_TIME = [
    'hour', 'day', 'week', 'month', 'year', 'all'
]

# Accepted content types and relative extension.
ACCEPTED_CONTENT_TYPES = {
    "image/jpeg": "jpg",
    "image/png": "png",
}
