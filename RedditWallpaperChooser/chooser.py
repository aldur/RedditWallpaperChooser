#!/usr/bin/env python
# encoding: utf-8

"""Reddit parser."""

import random
import shutil

from .logger import logger
from .parser import RedditParser
from .constants import LIMIT, SUBREDDITS, OUTPUT_WALL


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

    def choose_wall(self):
        """Find edible wallpapers and return a new one.

        :returns: The chosen wallpaper or None if any error occurs.
        """
        walls = self._find_walls()
        [w.get_header_info() for w in walls]

        walls = {w for w in walls if w.check()}

        new_walls = {w for w in walls if w not in self.already_chosen}
        if not new_walls:
            # fallback if every wall has been already chosen.
            new_walls = walls

        while new_walls:
            try:
                w = random.choice(tuple(new_walls))
                self.already_chosen.add(w)
                return w
            except IndexError:  # Something went wrong while fetching walls
                logger.warning("Something went wrong while fetching walls.")

        return None

    def get_wall(self, wall):
        """Download the wallpaper and store it on the local file system.

        :wall: The wallpaper to be downloaded.
        :returns: True if operation succeded.
        """
        wall.download()
        shutil.copyfile(wall.output, "{}.{}".format(OUTPUT_WALL, wall.extension))
