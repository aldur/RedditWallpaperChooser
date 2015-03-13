#!/usr/bin/env python
# encoding: utf-8

"""The constants."""

# Reddit UserAgent.
REDDIT_USER_AGENT = "RedditWallpaperChooser (github.com/aldur/RedditWallpaperChooser/)"

# Authentication.
USER = None
PASSWORD = None

# Subreddits to parse for walls.
SUBREDDITS = [
    "spaceporn",
    "skyporn",
    "earthporn",
]

# Accepted content types and relative extension.
ACCEPTED_CONTENT_TYPES = {
    "image/jpeg": "jpg",
}

# Limit of walls to parse from each subreddit.
LIMIT = 5

# Cache directory and output wallpaper path.
OUTPUT_PATH = "wallpapers"
OUTPUT_WALL = "wallpaper"
