#!/usr/bin/env python
# encoding: utf-8

"""The constants."""

from RedditWallpaperChooser import __version__

# Reddit UserAgent.
REDDIT_USER_AGENT = \
    "unix:RedditWallpaperChooser:{}" \
    "(by /u/aldur999)".format(__version__)

# RedditWallpaperChooser application ID
REDDIT_CLIENT_ID = "XQ7-8tIJnfK34w"

# Accepted content types and relative extension.
ACCEPTED_CONTENT_TYPES = {
    "image/jpeg": "jpg",
    "image/png": "png",
}
