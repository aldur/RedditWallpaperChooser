#!/usr/bin/env/ python
# encoding: utf-8

"""
Handle remote interaction.
"""

import shutil
import requests
import logging

import RedditWallpaperChooser.constants

__author__ = 'aldur'
logger = logging.getLogger(__name__)


def store(wallpaper):
    """
    Download the wallpaper and store it on disk.

    :param wallpaper: The wallpaper to be stored.
    """
    # Request the wallpaper.
    r = requests.get(wallpaper.url, stream=True)

    # Set the content type / size.
    wallpaper.contentType = r.headers.get('content-type', None)
    wallpaper.contentSize = r.headers.get('content-size', None)

    accepted_contents_type = RedditWallpaperChooser.constants.ACCEPTED_CONTENT_TYPES
    if wallpaper.contentType not in accepted_contents_type:
        r.close()
        logger.debug("Skipping not supported content-type: %s.", wallpaper.contentType)
        return

    if r.status_code == requests.codes.ok:
        with open(wallpaper.output_path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

        wallpaper.store_header_info()
    else:
        logger.warning(
            "Bad status code for wallpaper at %s: %d.",
            wallpaper.url,
            r.status_code
        )

    r.close()
