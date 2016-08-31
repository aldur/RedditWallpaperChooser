#!/usr/bin/env python
# encoding: utf-8

"""Wallpaper classes."""

import logging
import zlib

import RedditWallpaperChooser.constants
import RedditWallpaperChooser.utils

__author__ = 'aldur'

logger = logging.getLogger(__name__)


class WebWallpaper(object):

    """A wallpaper from the web."""

    def __init__(self, title, url, size, subreddit):
        self.title = title
        self.url = url
        self.size = size
        self.subreddit = subreddit

        # Produce a deterministic identifier starting form the url.
        self.id = str(zlib.adler32(self.url.encode()))

        # Store the image ratio
        self.ratio = round(float(self.size.width) / self.size.height, 5)

        self.image_type = None

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.url == other.url

    def __hash__(self):
        return hash(self.url)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "{} - {} - [{}x{}]".format(self.title, self.url, *self.size)

    def set_image_type(self, content_type):
        """
        Set the image type, based on the HTTP content type.
        """
        content_types = RedditWallpaperChooser.constants.ACCEPTED_CONTENT_TYPES
        if content_type not in content_types:
            logger.warning(
                "Unknown content type %s. Falling back to JPG.",
                content_type
            )

        self.image_type = content_types.get(content_type, "jpg")

    def fits(self, target_size, target_ratio):
        """
        :param target_size: A target size (can be None).
        :param target_ratio: A target ratio (can be None).

        :return: True if the wallpaper is bigger than the provided size and respects the ratio requirements.
        """
        if not target_size and not target_ratio:
            return True

        size_fits = False
        aspect_ratio_fits = False

        if target_size:
            size_fits = all((
                self.size.height >= target_size.height,
                self.size.width >= target_size.width,
            ))

        if target_ratio:
            aspect_ratio_fits = target_ratio == self.ratio

        if target_size and target_ratio:
            return size_fits and aspect_ratio_fits
        elif target_size:
            return size_fits
        else:  # aspect_ratio_fits
            return aspect_ratio_fits

    @property
    def info(self):
        """
        Info for this wallpaper.
        """
        return {
            "title": self.title,
            "url": self.url,
            "width": self.size.width,
            "height": self.size.height,
            "image_type": self.image_type,
            "subreddit": self.subreddit,
        }

    @property
    def info_path(self):
        """
        The path of the wallpaper's info on disk.
        """
        return "{}.json".format(self.id)

    @property
    def output_path(self):
        """
        The output path of the stored wallpaper on disk.
        """
        assert self.image_type is not None, \
            "I need the image type to generate the output path."
        return "{}.{}".format(self.id, self.image_type)
