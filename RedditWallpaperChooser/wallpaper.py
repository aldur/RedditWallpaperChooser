#!/usr/bin/env python
# encoding: utf-8

"""Wallpaper classes."""

import os.path
import json
import zlib
import logging

# noinspection PyPackageRequirements
from PIL import Image

from .constants import ACCEPTED_CONTENT_TYPES, OUTPUT_PATH, SIZE, RATIO
import RedditWallpaperChooser.remote

CONSTANT_RATIO = round(float(RATIO[0]) / RATIO[1], 5)
logger = logging.getLogger(__name__)


class WebWallpaper(object):

    """A wallpaper from the web."""

    @staticmethod
    def extension_from_content_type(content_type):
        """
        Return the file extension by using the HTTP content-type header.

        :param content_type: An HTTP content type.
        """
        if content_type not in ACCEPTED_CONTENT_TYPES:
            logger.warning(
                "Unknown content type %s. Falling back to JPG.",
                content_type
            )
        return ACCEPTED_CONTENT_TYPES.get(content_type, "jpg")

    def __init__(self, name, url):
        self.name = name
        self.url = url

        self.storage_directory = OUTPUT_PATH

        self.contentSize = None
        self.contentType = None

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.url == other.url

    def __hash__(self):
        return hash(self.url)

    def __str__(self):
        s = "{} - {})".format(self.name, self.url)

        if self.image_size:
            s += " - {}x{} - {}".format(
                self.image_size[0], self.image_size[1],
                ":".join([str(r) for r in RATIO])
                if self.ratio == CONSTANT_RATIO else self.ratio
            )

        return s

    def store(self):
        """
        At the end of this call,
        the wallpaper and its header info will be stored on disk.
        """
        if self.parse_header_info():
            # The wallpaper was already stored, as well as its info.
            logger.debug("Cache hit for wallpaper: '%s'.", self.url)
            return

        RedditWallpaperChooser.remote.store(self)

        logger.info("Wallpaper from %s successfully downloaded.", self.url)

    def parse_header_info(self):
        """
        If the wallpaper has already been stored,
        read its header information directly from the cache.

        :returns: True if read from cache did succeed.
        """
        if not self.is_stored:
            return False

        with open(self.header_path, "r") as json_file:
            j = json.load(json_file)

            self.contentSize = j["contentSize"]
            self.contentType = j["contentType"]

            return True

    def store_header_info(self):
        """
        Store header info on file system, through a json file.
        """
        with open(self.header_path, "w") as json_file:
            json.dump(
                {
                    "contentType": self.contentType,
                    "contentSize": self.contentSize,
                },
                json_file
            )

    # TODO: fix target_size and target_aspect_ratio
    def check(
            self, target_size=False, target_aspect_ration=False
    ):
        """
        Check whether the wallpaper should be stored/used.

        :param target_size: Minimum required image size.
        :param target_aspect_ration: Required aspect ratio.
        :returns: A boolean.
        """
        if self.contentType is None:
            logger.warning(
                "The content type field should be populated before calling check."
            )
            return

        accepted_content_type = self.contentType in ACCEPTED_CONTENT_TYPES
        if not accepted_content_type:
            return False
        if not target_size and not target_aspect_ration:
            return accepted_content_type

        size_fits = all([self.image_size[i] >= SIZE[i] for i in range(2)])
        aspect_ratio_fits = CONSTANT_RATIO == self.ratio

        if target_size and target_aspect_ration:
            return size_fits and aspect_ratio_fits
        elif target_size:
            return size_fits
        else:  # aspect_ratio_fits
            return aspect_ratio_fits

    @property
    def image_size(self):
        """
        Return the image width and height as read the stored file.
        """
        if not self.is_stored:
            logger.warning(
                "Can't get size of not-stored wallpaper."
            )

        i = Image.open(self.output_path)
        _size = i.image_size()
        i.close()

        return _size

    @property
    def ratio(self):
        """
        Return the aspect ratio of the wallpaper (if cached).
        """
        if self.image_size:
            return round(float(self.image_size[0]) / self.image_size[1], 5)

    @property
    def _common_path_prefix(self):
        # Generate a deterministic hash from the url
        hash_string = str(zlib.adler32(self.url.encode()))
        return os.path.join(
            self.storage_directory,
            hash_string,
        )

    @property
    def header_path(self):
        """
        The path of the wallpaper's header on disk.
        """
        return "{}.json".format(self._common_path_prefix)

    @property
    def output_path(self):
        """
        The output path of the stored wallpaper on disk.
        """
        assert self.contentType is not None, \
            "I need the content type to generate the output path."

        return "{}.{}".format(
            self._common_path_prefix,
            WebWallpaper.extension_from_content_type(self.contentType)
        )

    @property
    def absolute_output_path(self):
        """
        Return the absolute output path.
        """
        return os.path.realpath(self.output_path)

    @property
    def is_stored(self):
        """
        Return True if wall is stored on disk.
        """
        return os.path.exists(self.header_path)


class ImgurWebWallpaper(WebWallpaper):
    """Wallpapers from the Imgur hosting."""
    pass
