#!/usr/bin/env/ python
# encoding: utf-8

"""
Configuration logic.
"""

import configparser
import logging

import RedditWallpaperChooser.utils

__author__ = 'aldur'


logger = logging.getLogger(__name__)

SECTION_REDDIT = "reddit"
REDDIT_SUBREDDITS = "subreddits"
REDDIT_RESULT_LIMIT = "result_limit"
REDDIT_SORTING = "sorting"
REDDIT_TIME = "time"

SECTION_WALLPAPER = "wallpaper"
WALLPAPER_SIZE = "size"
WALLPAPER_ASPECT_RATIO = "aspect_ratio"
WALLPAPER_FOLDER = "output_folder"

_default_config = {
    SECTION_REDDIT: {
        REDDIT_SUBREDDITS: "spaceporn, skyporn, earthporn, wallpapers, wallpaper",
        REDDIT_SORTING: "hot",
        REDDIT_RESULT_LIMIT: "100",
        REDDIT_TIME: "month",
    },

    SECTION_WALLPAPER: {
        WALLPAPER_SIZE: "1920x1080",
        WALLPAPER_ASPECT_RATIO: "16:9",
        WALLPAPER_FOLDER: "wallpapers",
    },
}

parser = None


def as_dictionary():
    """
    :return: The parsed configuration as a dictionary.
    """
    assert parser, "Parse the configuration first."
    return {
        section: {
            k: v for k, v in parser.items(section)
        } for section in parser.sections()
    }


def parse_config(config_path):
    """
    Read the .ini configuration.
    Store the configuration in the "config" global variable.

    :param config_path: Path to configuration file.
    """
    global parser
    if parser is not None:
        logger.debug("Configuration already loaded, skipping.")
        return

    parser = configparser.ConfigParser()
    parser.read_dict(_default_config)
    if config_path:
        with open(config_path) as config_file:
            logger.info("Loading configuration from: '%s'.", config_path)
            parser.read_file(config_file)
    else:
        logger.info("No configuration path provided. Loading default values.")


def write_default_config(config_path):
    """
    Helper function to store default configuration.

    :param config_path: Path on which configuration will be stored.
    """
    logger.info("Storing default configuration to %s.", config_path)
    default_parser = configparser.ConfigParser()
    default_parser.read_dict(_default_config)

    with open(config_path, "w") as config_file:
        default_parser.write(config_file)


def get_size():
    """
    Parse the configuration for target image size.

    :return: An image size.
    """
    assert parser is not None

    size = parser.get(SECTION_WALLPAPER, WALLPAPER_SIZE)
    assert not size or "x" in size, "Malformed image size."

    if not size:
        return None

    size = size.split("x")
    assert len(size) == 2, "Malformed image size."

    return RedditWallpaperChooser.utils.Size(int(size[0]), int(size[1]))


def get_ratio():
    """
    Parse the configuration for target image ratio.

    :return: The required image ration (as float).
    """
    ratio = parser.get(SECTION_WALLPAPER, WALLPAPER_ASPECT_RATIO)
    assert not ratio or ":" in ratio, "Malformed image ratio."

    if not ratio:
        return None

    ratio = ratio.split(":")
    assert len(ratio) == 2, "Malformed image ratio."

    return round(float(ratio[0]) / float(ratio[1]), 5)
