#!/usr/bin/env python
# encoding: utf-8

"""Wallpaper classes."""

import os.path
import requests
import shutil
import threading
import json
import zlib

from PIL import Image

from .constants import ACCEPTED_CONTENT_TYPES, OUTPUT_PATH, SIZE, RATIO
from .logger import logger

CONSTANT_RATIO = round(float(RATIO[0]) / RATIO[1], 5)


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
        self.thread = threading.Thread(target=self._store)

        self.contentSize = None
        self.contentType = None

        self._size = None

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.url == other.url

    def __hash__(self):
        return hash(self.url)

    def __str__(self):
        s = "{} - {})".format(self.name, self.url)

        if self.size:
            s += " - {}x{} - {}".format(
                self.size[0], self.size[1],
                ":".join([str(r) for r in RATIO])
                if self.ratio == CONSTANT_RATIO else self.ratio
            )

        return s

    def _store(self):
        """Download and store the wallpaper on disk.

        Set the content type as well.
        """
        if self.read_header_info():
            # We have the wallpaper in cache and are able to read its header
            # info
            logger.debug("Cache hit for wallpaper: '%s'", self.url)
        else:  # request the wallpaper to the remote
            r = requests.get(self.url, stream=True)

            self.contentType = r.headers.get('content-type', None)
            self.contentSize = r.headers.get('content-size', None)

            # We don't download it if it doesn't pass the check
            if not self.check():
                r.close()
                return

            if r.status_code == requests.codes.ok:
                with open(self.output, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)

                self._store_header_info()

            logger.info("Wallpaper from %s successfully downloaded.", self.url)

    def read_header_info(self):
        """If the item is cached, read the header information directly from the cache.
        :returns: True if read from cache did succeed.

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
        :returns: True if storing did succeed.

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

    def get_header_info(self):
        """Request url header to find the content types and sizes of the wallpaper."""
        self.thread.start()
        return self.thread

    def check(self, size=False, aspect_ratio=False):
        """Check if the wallpaper can actually be used.

        :returns: boolean.
        """
        try:
            content_type = self.contentType in ACCEPTED_CONTENT_TYPES
            if not content_type:
                return False
            if not size and not aspect_ratio:
                return content_type

            image_size = self.size
            size_fits = all([image_size[i] >= SIZE[i] for i in range(2)])
            aspect_ratio_fits = CONSTANT_RATIO == self.ratio

            if size and aspect_ratio:
                return size_fits and aspect_ratio_fits
            elif size:
                return size_fits
            else:  # aspect_ratio_fits
                return aspect_ratio_fits
        except AttributeError:
            logger.warning(
                "check called without having header wallpaper info.", exc_info=True
            )
            return False

    @property
    def size(self):
        """Return image width and height from the stored file."""
        if self.cached:
            if not self._size:
                i = Image.open(self.output)
                self._size = i.size
                i.close()
            return self._size
        else:
            return None

    @property
    def ratio(self):
        """Return the aspect ratio of the wallpaper (if cached)."""
        if self.size:
            return round(float(self.size[0]) / self.size[1], 5)

    @property
    def extension(self):
        """Guess the file extension from the HTTP content-type header."""
        try:
            return ACCEPTED_CONTENT_TYPES.get(self.contentType, None)
        except AttributeError:
            logger.warning(
                "extension called without having header wallpaper info.", exc_info=True)
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
