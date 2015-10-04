#!/usr/bin/env python
# encoding: utf-8

"""
RedditWallpaperChooser main file.
"""

import sys
import logging

import RedditWallpaperChooser.chooser
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


def main():
    """
    Main, what else?
    """
    _setup_logging(logging.DEBUG)

    rwc = RedditWallpaperChooser.chooser.Chooser(USER, PASSWORD)
    w = rwc.choose_random_trending_wall()

    if w:
        print(w.absolute_output_path)  # Print on stdout
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
