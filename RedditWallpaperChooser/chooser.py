#!/usr/bin/env python
# encoding: utf-8

"""Reddit parser."""

import random
import shutil
import os.path

from .logger import logger
from .parser import RedditParser
from .constants import LIMIT, SUBREDDITS, OUTPUT_WALL, STORE_EXTENSION


class RedditWallpaperChooser(object):

    """Handle subreddit parsing and selected wallpaper choice."""

    def __init__(self, user=None, password=None):
        """Init the subreddit list and the reddit parser."""
        self.already_chosen = set()
        self.r = RedditParser(SUBREDDITS, user, password)

    def _find_walls(self, limit=LIMIT):
        """Parse subreddits and find the hottest wallpapers.
        :limit: The maximum limit of results for each subreddit.
        :returns: A set of WebWallpapers.

        """
        logger.info("Getting walls from Reddit.")
        return self.r.fetch()

    def choose_wall(self, size=False, aspect_ratio=False):
        """Find edible wallpapers and return a new one.

        :size: If set to True, check for specific wallpaper size.
        :aspect_ratio: If set to True, check for specific aspect ratio.
        :returns: The chosen wallpaper or None if any error occurs.
        """
        walls = self._find_walls()  # Download the wallpaper list from Reddit

        # Store the wallpapers / check the cache
        threads = [w.get_header_info() for w in walls]
        [t.join() for t in threads]

        # Select edible wallpapers
        walls = {w for w in walls if w.check(size, aspect_ratio)}

        try:
            w = random.choice(tuple(walls))
            return w
        except IndexError:  # Something went wrong while fetching walls
            logger.error("Something went wrong while fetching walls, sorry.")

        return None

    def get_wall(self, wall):
        """Download the wallpaper and store it on the local file system.

        :wall: The wallpaper to be downloaded.
        :returns: The realpath of the output file, on success.
        """
        if wall:
            if STORE_EXTENSION:
                output = "{}.{}".format(OUTPUT_WALL, wall.extension)
            else:
                output = OUTPUT_WALL
            shutil.copyfile(wall.output, output)

            logger.info(
                "Wallpaper %s succesfully downloaded to %s",
                wall, output
            )

            return os.path.realpath(output)
