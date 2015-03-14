#!/usr/bin/env python
# encoding: utf-8

import sys

from RedditWallpaperChooser.chooser import RedditWallpaperChooser
from RedditWallpaperChooser.constants import USER, PASSWORD, CHECK_SIZE, CHECK_RATIO

if __name__ == '__main__':
    rwc = RedditWallpaperChooser(USER, PASSWORD)
    w = rwc.choose_wall(CHECK_SIZE, CHECK_RATIO)
    out = rwc.get_wall(w)

    if out:
        print(out)  # Print on stdout
        sys.exit(0)
    else:
        sys.exit(1)
