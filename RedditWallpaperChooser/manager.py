#!/usr/bin/env python
# encoding: utf-8

"""
Parse subreddits searching for wallpapers.
"""

import asyncio
import http
import json
import logging
import os.path
import random

import RedditWallpaperChooser.reddit
import RedditWallpaperChooser.wallpaper
from RedditWallpaperChooser import config, constants
import aiohttp

__author__ = 'aldur'

logger = logging.getLogger(__name__)


class Manager(object):

    """Parse each subreddit and store the wallpapers they link to."""

    def __init__(self, output_path):
        assert output_path
        self.output_path = output_path

        self.subreddits = [subreddit.strip() for subreddit in config.parser.get(
            config.SECTION_REDDIT, config.REDDIT_SUBREDDITS
        ).split(",")]
        assert self.subreddits

        self.walls = set()

    async def fetch_from_subreddit(self, session, subreddit):
        """
        Fetch trending walls from selected subreddit.

        :param session: An aiohttp session.
        :param subreddit: Subreddit to be parsed.
        """
        sorting = config.parser.get(config.SECTION_REDDIT, config.REDDIT_SORTING)
        assert sorting in constants.REDDIT_ALLOWED_SORTING
        subreddit_limit = config.parser.getint(config.SECTION_REDDIT, config.REDDIT_RESULT_LIMIT)

        url = constants.REDDIT_API_FORMAT_URL.format(subreddit, sorting)
        params = {'limit': 100}

        if sorting in constants.REDDIT_NEED_TIME:
            t = config.parser.get(config.SECTION_REDDIT, config.REDDIT_TIME)
            assert t in constants.REDDIT_ALLOWED_TIME
            params.update({'t': t})
            logger.info("Fetching %s/%s wallpapers from 'r/%s'.", sorting, t, subreddit)
        else:
            logger.info("Fetching %s wallpapers from 'r/%s'.", sorting, subreddit)

        count = 0
        while count < subreddit_limit:
            async with session.get(url, params=params) as response:
                if response.status != http.HTTPStatus.OK:
                    logger.warning("Can't contact 'r/%s (status: %s).", subreddit, response.status)
                    return
                data = await response.json()

            walls, after = RedditWallpaperChooser.reddit.parse_listing(data)
            count += len(walls)

            self.walls |= {
                w for w in walls
                if w.fits(config.get_size(), config.get_ratio())
            }

            if after is None:
                break
            params.update({'after': after})

        logger.debug("Fetching from 'r/%s' completed.", subreddit)

    def fetch(self):
        """
        Globally fetch trending walls from each subreddit.
        """
        logger.info("Fetching wallpapers list from subreddits...")
        with aiohttp.ClientSession(
            headers={"User-Agent": RedditWallpaperChooser.constants.REDDIT_USER_AGENT},
            connector=aiohttp.TCPConnector(limit=5),
        ) as session:
            tasks = [
                asyncio.ensure_future(self.fetch_from_subreddit(session, subreddit))
                for subreddit in self.subreddits
            ]
            asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))

            return self.walls

    async def store_wallpaper(self, session, wallpaper):
        """
        Store the wallpaper and its information.

        :param session: An aiohttp session.
        :param wallpaper: The wallpaper to be stored.
        """
        info_path = os.path.join(self.output_path, wallpaper.info_path)

        if os.path.exists(info_path):
            logger.debug("Cache hit for wallpaper: '%s'.", wallpaper.url)
            wallpaper.image_type = json.load(open(info_path, 'r'))['image_type']
            return

        async with session.get(wallpaper.url) as response:
            if response.status != http.HTTPStatus.OK:
                logger.warning("Bad status code from '%s' (%d).", wallpaper.url, response.status)
                return
            wallpaper.set_image_type(response.headers["content-type"])

            with open(info_path, "w") as info_file:
                json.dump(wallpaper.info, info_file, indent=2)

            data = await response.read()

            wallpaper_path = os.path.join(self.output_path, wallpaper.output_path)
            with open(wallpaper_path, 'wb') as f:
                f.write(data)

            logger.debug("Wallpaper from '%s' successfully downloaded.", wallpaper.url)

    def store(self):
        """
        Store the previously fetched wallpapers.
        """
        logger.info("Storing wallpapers...")
        with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=5),
        ) as session:
            tasks = [
                asyncio.ensure_future(self.store_wallpaper(session, wallpaper))
                for wallpaper in self.walls
            ]
            asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))
        logger.info("All done!")

    def choose(self):
        """
        Choose one of the stored wallpapers and return its absolute path.
        """
        assert self.walls
        return os.path.abspath(
            os.path.join(self.output_path, random.choice(tuple(self.walls)).output_path))
