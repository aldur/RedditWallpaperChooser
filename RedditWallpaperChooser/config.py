#!/usr/bin/env/ python
# encoding: utf-8

"""
Configuration logic.
"""

import configparser
import logging

__author__ = 'aldur'


logger = logging.getLogger(__name__)

SECTION_REDDIT = "reddit"
REDDIT_USERNAME = "username"
REDDIT_PASSWORD = "password"
REDDIT_SUBREDDITS = "subreddits"
REDDIT_RESULT_LIMIT = "result_limit"

SECTION_WALLPAPER = "wallpaper"
WALLPAPER_SIZE = "size"
WALLPAPER_ASPECT_RATIO = "aspect_ratio"
WALLPAPER_FOLDER = "output_folder"

_default_config = {
    SECTION_REDDIT: {
        REDDIT_USERNAME: "",
        REDDIT_PASSWORD: "",
        REDDIT_SUBREDDITS: "spaceporn, skyporn, earthporn, wallpapers, wallpaper",
        REDDIT_RESULT_LIMIT: "10"
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
