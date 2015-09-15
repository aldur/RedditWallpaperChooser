#!/usr/bin/env python
# encoding: utf-8

import praw
import threading

from .wallpaper import WebWallpaper
from .logger import logger
from .constants import REDDIT_USER_AGENT, LIMIT


class RedditParser(object):

    """Parse subreddits and store a list of wallpapers."""

    def __init__(self, subreddits, user=None, password=None):
        """Init the list of wallpapers."""
        user_agent = REDDIT_USER_AGENT

        self.r = praw.Reddit(user_agent=user_agent)

        if user and password:
            self.r.login(user=user, password=password)

        self.walls = set()
        self.subreddits = subreddits
        self.semaphore = threading.Semaphore()

    def _fetch_walls(self, subreddit):
        """Fetch walls from subreddit and store them in the walls set.

        :subreddit: Subreddit to be parsed.
        """
        logger.info("Fetching wallpapers from 'r/%s'.", subreddit)
        r_walls = self.r.get_subreddit(subreddit).get_hot(limit=LIMIT)

        self.semaphore.acquire()
        self.walls |= {WebWallpaper(str(w), w.url) for w in r_walls if not w.is_self}
        self.semaphore.release()

        logger.debug("Fetching from 'r/%s' completed.", subreddit)

    def fetch(self):
        """Fetch walls from all subreddits and return them."""
        threads = [
            threading.Thread(target=self._fetch_walls, args=(subreddit,))
            for subreddit
            in self.subreddits
        ]

        [t.start() for t in threads]
        [t.join() for t in threads]
        logger.info("Done fetching from subreddits.")

        return self.walls
