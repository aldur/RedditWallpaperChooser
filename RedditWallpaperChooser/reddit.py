#!/usr/bin/env/ python
# encoding: utf-8

"""
Reddit API handler.
"""

import logging

import RedditWallpaperChooser.constants
import RedditWallpaperChooser.utils
import RedditWallpaperChooser.wallpaper

__author__ = 'aldur'

logger = logging.getLogger(__name__)


def parse_listing(listing):
    """
    Parse a Reddit listing, looking for wallpaper links.

    :param listing: The listing to be parsed, i.e. a JSON as returned by an API call.
    :return: A list of wallpapers and the 'after' token, if any.
    """
    assert listing['kind'] == 'Listing'
    children = listing['data']['children']

    return {w for w in (
        parse_child(child)
        for child in children
        if child['kind'] == 't3'
    ) if w is not None}, listing['data'].get('after', None)


def parse_child(child):
    """
    Parse a Reddit Listing child of type 'link'.

    :param child: The child to be parsed.
    :return: A wallpaper object from the child.
    """
    assert child['kind'] == 't3'
    data = child['data']

    title = data['title']
    url = data['url']
    subreddit = data['subreddit']
    try:
        source = data['preview']['images'][0]['source']
        url = source['url']
        width = source['width']
        height = source['height']

        return RedditWallpaperChooser.wallpaper.WebWallpaper(
            title, url, RedditWallpaperChooser.utils.Size(width, height), subreddit
        )
    except KeyError:  # Old posts do not have the 'preview' API field.
        logger.debug("Ignoring '{}' - '{}' from 'r/{}'.".format(title, url, subreddit))
        return None
