#!/usr/bin/env python
# encoding: utf-8

"""Wallpaper classes."""

import os.path
import requests
import shutil
import threading
import json
import zlib

from .constants import ACCEPTED_CONTENT_TYPES, OUTPUT_PATH
from .logger import logger


class WebWallpaper(object):

    """Wallpapers from the web."""

    def __init__(self, name, url):
        """
        Init the name, the url, the size of the wall, and so on.
        Storage is the directory when it will be saved.
        """
        self.name = name
        self.url = url

        self.storage = OUTPUT_PATH

        self.event = threading.Event()
        # TODO: lazy initialization?
        self.thread = threading.Thread(target=self._store)

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.url == other.url)

    def __hash__(self):
        return hash(self.url)

    def _store(self):
        """Download and store the wallpaper on disk.

        Set the content type as well.
        """
        if self.read_header_info():
            # We have the wallpaper in cache and are able to read its header
            # info
            logger.debug("Cache hit for wallpaper: '%s'", self.url)
            self.event.set()
        else:  # request the wallpaper to the remote
            r = requests.get(self.url, stream=True)

            self.contentType = r.headers.get('content-type', None)
            self.contentSize = r.headers.get('content-size', None)

            self.event.set()

            if not self.check():  # We don't download it if it doesn't pass the check
                r.close()
                return

            if r.status_code == requests.codes.ok:
                with open(self.output, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)

                self._store_header_info()

            logger.info("Wallpaper from %s successfully downloaded.", self.url)

    def read_header_info(self):
        """If the item is cached, read the header informations directly from the cache.
        :returns: True if read from cache succeded.

        """
        if self.cached:
            json_path = "{}.json".format(self.output)

            with open(json_path, "r") as json_file:
                j = json.load(
                    json_file
                )

                self.contentSize = j["contentSize"]
                self.contentType = j["contentType"]

            return True
        return False

    def _store_header_info(self):
        """Store header info on file system, through a json file.
        :returns: True if storing succeded.

        """
        json_path = "{}.json".format(self.output)

        with open(json_path, "w") as json_file:
            json.dump(
                {
                    "contentType": self.contentType,
                    "contentSize": self.contentSize,
                },
                json_file
            )

        return True

    def get_header_info(self, store=True):
        """Request url header to find the content types and sizes of the wallpaper."""
        if store:  # While doing the header request, store the wallpaper too.
            self.thread.start()
            self.event.wait()
        else:
            r = requests.head(self.url)

            self.contentType = r.headers.get('content-type', None)
            self.contentSize = r.headers.get('content-size', None)

    def check(self):
        """Check if the wallpaper can actually be used.

        :returns: boolean.
        """
        try:
            return self.contentType in ACCEPTED_CONTENT_TYPES
        except AttributeError:
            logger.warning("check called without having header wallpaper info.", exc_info=True)
            return False

    def download(self):
        """Download the wallpaper to a specified output directory.

        :returns: True if download succeded.
        """
        if self.thread.isAlive():  # we are still downloading the image
            self.thread.join()
        else:  # we need the image
            self._store()
        return True

    @property
    def extension(self):
        """Guess the file extension from the HTTP content-type header."""
        try:
            return ACCEPTED_CONTENT_TYPES.get(self.contentType, None)
        except AttributeError:
            logger.warning("extension called without having header wallpaper info.", exc_info=True)
            return "jpg"  # Fallback to jpg

    @property
    def output(self):
        """The output path of the stored wallpaper on disk."""
        # Generate a deterministic hash from the url
        hash_string = str(zlib.adler32(self.url.encode()))
        output = os.path.join(self.storage, hash_string)

        return output

    @property
    def cached(self):
        """Return True if wall is cached on disk."""
        return os.path.exists(self.output)


class ImgurWebWallpaper(WebWallpaper):

    """Wallpapers from the Imgur hosting."""
    pass
