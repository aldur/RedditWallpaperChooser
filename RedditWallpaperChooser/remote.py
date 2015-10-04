#!/usr/bin/env/ python
# encoding: utf-8

"""
Handle remote interaction.
"""

import shutil
import requests
import logging

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

    # Abort the download it if it doesn't pass the check.
    if not wallpaper.check():
        r.close()
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
