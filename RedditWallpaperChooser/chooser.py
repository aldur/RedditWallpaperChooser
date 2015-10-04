#!/usr/bin/env python
# encoding: utf-8

"""Reddit parser."""

import random
import logging
import threading
import os.path
import sys

import RedditWallpaperChooser.parser
import RedditWallpaperChooser.config as config

# TODO: LIMIT request number.

logger = logging.getLogger(__name__)


class Chooser(object):

    """Handle subreddit parsing and selected wallpaper choice."""

    @staticmethod
    def _create_output_directory():
        """
        Create the output directory, if needed.
        """
        output_path = config.parser.get(
            config.SECTION_WALLPAPER,
            config.WALLPAPER_FOLDER
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

    def choose_random_trending_wall(self):
        """
        Find edible wallpapers and return a new one.

        :returns: The chosen wallpaper or None if any error occurs.
        """
        type(self)._create_output_directory()

        logger.info("Getting wallpapers from Reddit.")
        r = RedditWallpaperChooser.parser.RedditParser()
        walls = r.fetch()  # Download the wallpaper list from Reddit

        # Store the wallpapers on disk.
        threads = [
            threading.Thread(target=w.store) for w in walls
        ]
        [t.start() for t in threads]
        [t.join() for t in threads]

        filtered_walls = tuple(w for w in walls if w.check())

        try:
            w = random.choice(filtered_walls)
            return w
        except IndexError:  # Something went wrong while fetching walls
            logger.error("Something went wrong while fetching walls, sorry.")
            return None
