#!/usr/bin/env python
# encoding: utf-8

"""
RedditWallpaperChooser main file.
"""

import argparse
import json
import logging
import os
import sys

import RedditWallpaperChooser.config
import RedditWallpaperChooser.manager

__author__ = 'aldur'

_config_file_path = "config"
_default_config_file_path = "default_config"
_log_level = "log_level"

logger = logging.getLogger(__name__)


def _setup_logging(log_level):
    """
    Configure an handler for the logging facilities.

    :param log_level: Log level.
    """
    assert log_level, "I need a logging level."

    module_logger = logging.getLogger(RedditWallpaperChooser.__name__)
    module_logger.setLevel(log_level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = None
    try:
        # noinspection PyUnresolvedReferences, PyPackageRequirements
        import colorlog
        formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(levelname)-6s%(reset)s %(cyan)s%(name)-10s %(white)s%(message)s",
            datefmt=None,
            reset=True,
            log_colors={
                'DEBUG': 'blue',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red',
                'EXCEPTION': 'red',
            }
        )
    except ImportError:
        formatter = logging.Formatter(
            "%(levelname)s - %(name)s - %(message)s",
        )
    finally:
        console_handler.setFormatter(formatter)

    module_logger.addHandler(console_handler)


def _cmd_line_parser():
    """
    Parse the command line configuration.

    :return: A new command line configuration parser.
    """

    def _to_add_argument(s):
        return "-{}".format(s[0]), "--{}".format(s),

    parser = argparse.ArgumentParser(
        description="Automatically download trending wallpapers from subreddits of your choice."
    )

    parser.add_argument(
        *_to_add_argument(_config_file_path),
        metavar="<configuration file path>",
        type=str,
        required=False,
        help='path to a INI configuration file'
    )

    parser.add_argument(
        *_to_add_argument(_default_config_file_path),
        metavar="<default configuration file path>",
        type=str,
        required=False,
        help='dump default configuration to this INI file and exit'
    )

    parser.add_argument(
        *_to_add_argument(_log_level),
        choices=['CRITICAL',
                 'ERROR',
                 'WARNING',
                 'INFO',
                 'DEBUG',
                 'NOTSET'],
        default='INFO',
        help="set logging level"
    )

    return parser


def _create_output_directory():
    """
    Create the output directory, if needed.
    """
    output_path = RedditWallpaperChooser.config.parser.get(
        RedditWallpaperChooser.config.SECTION_WALLPAPER,
        RedditWallpaperChooser.config.WALLPAPER_FOLDER
    )

    exists = os.path.exists(output_path)
    is_dir = os.path.isdir(output_path)

    if exists and not is_dir:
        logger.error(
            "The output path '%s' already exists and is not a directory. I can't continue.",
            output_path
        )
        sys.exit(False)

    if not exists:
        os.mkdir(output_path)

    return output_path


def main():
    """
    Main, what else?
    """
    # Handle CLI arguments
    cli_parser = _cmd_line_parser()
    cli_args = vars(cli_parser.parse_args())

    log_mapping = {
        'CRITICAL': logging.CRITICAL,
        'ERROR': logging.ERROR,
        'WARNING': logging.WARNING,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
        'NOTSET': logging.NOTSET,
        'NONE': None,
    }

    # Configure logging
    log_level = log_mapping[cli_args[_log_level]]
    _setup_logging(log_level)

    default_config_path = cli_args.get(_default_config_file_path, None)
    if default_config_path is not None:
        RedditWallpaperChooser.config.write_default_config(default_config_path)
        return 0

    # Parse .ini configuration
    config_path = cli_args.get(_config_file_path)
    RedditWallpaperChooser.config.parse_config(config_path)
    output_path = _create_output_directory()

    logger.debug(
        "Dumping loaded configuration:\n%s",
        json.dumps(
            RedditWallpaperChooser.config.as_dictionary(),
            indent=2,
        )
    )

    manager = RedditWallpaperChooser.manager.Manager(output_path)
    manager.fetch()
    manager.store()
    print(manager.choose())
