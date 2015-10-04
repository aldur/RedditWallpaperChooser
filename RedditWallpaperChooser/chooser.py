#!/usr/bin/env python
# encoding: utf-8

"""Reddit parser."""

import random
import shutil
import logging
import os.path
import threading

from .parser import RedditParser
from .constants import SUBREDDITS, OUTPUT_WALL, STORE_EXTENSION

# TODO: LIMIT request number.

logger = logging.getLogger(__name__)


class Chooser(object):

    """Handle subreddit parsing and selected wallpaper choice."""

    def __init__(self, user=None, password=None):
        """
        Init the subreddit list and the reddit parser.
        """
        self.r = RedditParser(SUBREDDITS, user, password)

    def _find_walls(self):
        """
        Ask the parser to find the most trending wallpapers.

        :returns: A set of WebWallpapers.
        """
        logger.info("Getting wallpapers from Reddit.")
        return self.r.fetch()

    def choose_random_trending_wall(self):
        """
        Find edible wallpapers and return a new one.

        :returns: The chosen wallpaper or None if any error occurs.
        """
        walls = self._find_walls()  # Download the wallpaper list from Reddit

        # Store the wallpapers on disk.
        threads = [
            threading.Thread(target=w.store) for w in walls
        ]
        [t.start() for t in threads]
        [t.join() for t in threads]

        try:
            w = random.choice(tuple(walls))
            return w
        except IndexError:  # Something went wrong while fetching walls
            logger.error("Something went wrong while fetching walls, sorry.")
            return None
