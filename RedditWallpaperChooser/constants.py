#!/usr/bin/env python
# encoding: utf-8

"""The constants."""

# Reddit UserAgent.
REDDIT_USER_AGENT = "RedditWallpaperChooser (github.com/aldur/RedditWallpaperChooser/)"

# Authentication.
USER = None
PASSWORD = None

# Check for wallpapers greater than SIZE
CHECK_SIZE = True
# Check for wallpapers with given RATIO
CHECK_RATIO = True

SIZE = (1920, 1080)  # Width x height
RATIO = (16, 9)  # 16:9

# Subreddits to parse for walls.
SUBREDDITS = [
    "spaceporn",
    "skyporn",
    "earthporn",
    "wallpapers",
    "wallpaper",
    # "Movieposterporn",  # useful on mobile devices
    # "ArtPorn",  # for art lovers
]

# Accepted content types and relative extension.
ACCEPTED_CONTENT_TYPES = {
    "image/jpeg": "jpg",
}

# Limit of walls to parse from each subreddit.
LIMIT = 10

# Cache directory and output wallpaper path.
OUTPUT_PATH = "wallpapers"
OUTPUT_WALL = "wallpaper"
STORE_EXTENSION = False  # True if you want the output wallpaper to have an extension
