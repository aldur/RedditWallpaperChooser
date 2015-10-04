#!/usr/bin/env python
# encoding: utf-8

import sys
import logging

from RedditWallpaperChooser.chooser import RedditWallpaperChooser, get_wall
from RedditWallpaperChooser.constants import USER, PASSWORD, CHECK_SIZE, CHECK_RATIO


def _setup_logging(log_level):
    """
    Configure an handler for the logging facilities.

    :param log_level: Log level.
    """
    assert log_level, "I need a logging level."

    logger = logging.getLogger(RedditWallpaperChooser.__name__)
    logger.setLevel(log_level)

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
                'INFO'	: 'green',
                'WARNING'	: 'yellow',
                'ERROR'		: 'red',
                'CRITICAL'	: 'red',
                'EXCEPTION'	: 'red',
            }
        )
    except ImportError:
        formatter = logging.Formatter(
            "%(levelname)s - %(name)s - %(message)s",
        )
    finally:
        console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)


if __name__ == '__main__':
    _setup_logging(logging.DEBUG)

    rwc = RedditWallpaperChooser(USER, PASSWORD)
    w = rwc.choose_wall(CHECK_SIZE, CHECK_RATIO)
    output_path = get_wall(w)

    if output_path:
        print(output_path)  # Print on stdout
        sys.exit(0)
    else:
        sys.exit(1)
