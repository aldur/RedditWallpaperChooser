#!/usr/bin/env python
# encoding: utf-8

from RedditWallpaperChooser.chooser import RedditWallpaperChooser
from RedditWallpaperChooser.constants import USER, PASSWORD

if __name__ == '__main__':
    rwc = RedditWallpaperChooser(USER, PASSWORD)
    w = rwc.choose_wall()
    rwc.get_wall(w)
