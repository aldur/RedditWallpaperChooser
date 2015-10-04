#!/usr/bin/env python
# encoding: utf-8

"""Wallpaper classes."""

import os.path
import json
import logging
import collections

# noinspection PyUnresolvedReferences
import zlib

# noinspection PyPackageRequirements
from PIL import Image

import RedditWallpaperChooser.remote
import RedditWallpaperChooser.constants
import RedditWallpaperChooser.config as config

logger = logging.getLogger(__name__)

Size = collections.namedtuple(
    "Size", "width, height"
)


class WebWallpaper(object):

    """A wallpaper from the web."""

    @staticmethod
    def extension_from_content_type(content_type):
        """
        Return the file extension by using the HTTP content-type header.

        :param content_type: An HTTP content type.
        """
        content_types = RedditWallpaperChooser.constants.ACCEPTED_CONTENT_TYPES
        if content_type not in content_types:
            logger.warning(
                "Unknown content type %s. Falling back to JPG.",
                content_type
            )
        return content_types.get(content_type, "jpg")

    @staticmethod
    def size_from_config():
        """
        Parse the configuration for target image size.

        :return: An image size.
        """
        size = config.parser.get(
            config.SECTION_WALLPAPER,
            config.WALLPAPER_SIZE
        )

        assert "x" in size, \
            "Malformed image size."

        size = size.split("x")
        assert len(size) == 2, \
            "Malformed image size."

        return Size(int(size[0]), int(size[1]))

    @staticmethod
    def ratio_from_config():
        """
        Parse the configuration for target image ratio.

        :return: The required image ration (as float).
        """
        ratio = config.parser.get(
            config.SECTION_WALLPAPER,
            config.WALLPAPER_ASPECT_RATIO,
        )

        assert ":" in ratio, \
            "Malformed image ratio."

        ratio = ratio.split(":")
        assert len(ratio) == 2, \
            "Malformed image ratio."

        return round(float(ratio[0]) / float(ratio[1]), 5)

    def __init__(self, name, url):
        self.name = name
        self.url = url

        self.storage_directory = config.parser.get(
            config.SECTION_WALLPAPER,
            config.WALLPAPER_FOLDER
        )

        self.contentSize = None
        self.contentType = None

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.url == other.url

    def __hash__(self):
        return hash(self.url)

    def __str__(self):
        s = "{} - {})".format(self.name, self.url)

        if self.image_size:
            s += " - {}x{}".format(
                *self.image_size
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

    def check(self):
        """
        Check whether the wallpaper should be returned ready to be used.

        :returns: A boolean.
        """
        if not self.is_stored:
            return False

        target_size = type(self).size_from_config()
        target_ratio = type(self).ratio_from_config()
        if not target_size and not target_ratio:
            return True

        size_fits = all((
            self.image_size.height >= target_size.height,
            self.image_size.width >= target_size.width,
        ))
        aspect_ratio_fits = target_ratio == self.ratio

        if target_size and target_ratio:
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
        _size = i.size
        i.close()

        return Size(*_size)

    @property
    def ratio(self):
        """
        Return the aspect ratio of the wallpaper (if cached).
        """
        if self.image_size:
            return round(float(self.image_size.width) / self.image_size.height, 5)

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
            type(self).extension_from_content_type(self.contentType)
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
