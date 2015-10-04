#!/usr/bin/env python
# encoding: utf-8

"""
Parse subreddits searching for wallpapers.
"""

import praw
import threading
import logging

import RedditWallpaperChooser.wallpaper
import RedditWallpaperChooser.constants
import RedditWallpaperChooser.config as config

logger = logging.getLogger(__name__)


class RedditParser(object):

    """Parse subreddits and store a list of wallpapers."""

    def __init__(self):
        self.r = praw.Reddit(
            user_agent=RedditWallpaperChooser.constants.REDDIT_USER_AGENT
        )

        username = config.parser.get(config.SECTION_REDDIT, config.REDDIT_USERNAME)
        password = config.parser.get(config.SECTION_REDDIT, config.REDDIT_PASSWORD)

        if username and password:
            self.r.login(user=username, password=password)

        subreddits = config.parser.get(
            config.SECTION_REDDIT, config.REDDIT_SUBREDDITS
        ).split(",")
        subreddits = [subreddit.strip() for subreddit in subreddits]
        self.subreddits = subreddits

        self.walls = set()
        self.semaphore = threading.Semaphore()

    def _fetch_walls(self, subreddit):
        """
        Fetch trending walls from selected subreddit.

        :subreddit: Subreddit to be parsed.
        """
        logger.info("Fetching wallpapers from 'r/%s'.", subreddit)
        r_walls = self.r.get_subreddit(subreddit).get_hot(
            limit=config.parser.getint(
                config.SECTION_REDDIT, config.REDDIT_RESULT_LIMIT
            )
        )

        # TODO: context manager?
        self.semaphore.acquire()
        self.walls |= {
            RedditWallpaperChooser.wallpaper.WebWallpaper(str(w), w.url) for w in r_walls if not w.is_self
        }
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
