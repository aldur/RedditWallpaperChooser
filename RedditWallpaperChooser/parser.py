#!/usr/bin/env python
# encoding: utf-8

"""
Parse subreddits searching for wallpapers.
"""

import praw
import threading
import logging

from .wallpaper import WebWallpaper
from .constants import REDDIT_USER_AGENT, LIMIT

logger = logging.getLogger(__name__)


class RedditParser(object):

    """Parse subreddits and store a list of wallpapers."""

    def __init__(
            self, subreddits,
            user=None, password=None
    ):
        self.r = praw.Reddit(user_agent=REDDIT_USER_AGENT)

        if user and password:
            self.r.login(user=user, password=password)

        self.walls = set()
        self.subreddits = subreddits
        self.semaphore = threading.Semaphore()

    def _fetch_walls(self, subreddit):
        """
        Fetch trending walls from selected subreddit.

        :subreddit: Subreddit to be parsed.
        """
        logger.info("Fetching wallpapers from 'r/%s'.", subreddit)
        r_walls = self.r.get_subreddit(subreddit).get_hot(limit=LIMIT)

        self.semaphore.acquire()
        self.walls |= {WebWallpaper(str(w), w.url) for w in r_walls if not w.is_self}
        self.semaphore.release()

        logger.debug("Fetching from 'r/%s' completed.", subreddit)

    def fetch(self):
        """
        Globally fetch trending walls from each subreddit.
        """
        threads = [
            threading.Thread(target=self._fetch_walls, args=(subreddit,))
            for subreddit
            in self.subreddits
        ]

        [t.start() for t in threads]
        [t.join() for t in threads]
        logger.info("Fetching from subreddits: done.")

        return self.walls
