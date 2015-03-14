# RedditWallpaperChooser
RedditWallpaperChooser will parse the most popular subreddits of your choice in order to find the best and most trending wallpapers of the day.

__Caution:__ RedditWallpaperChooser is still a work in progress.

## Features
* Select any subreddit you like.
* Select image ratio and image size as you wish.
* Compatible with both Python 2 and Python 3.

## Requirements
We support the following Python versions:

* Python 2.7 or greater.
* Python 3.4 or greater.

Any other requirement is listed in the `requirements.txt` file.

## Installation & Usage
Until RedditWallpaperChooser will land on PyPi (soon) you can install it by simply:

```bash
$ git clone https://github.com/aldur/RedditWallpaperChooser/
$ cd RedditWallpaperChooser
$ pip install -r requirements.txt  # --user could also help you
$ # optionally edit the file RedditWallpaperChooser/constants.py
```

You can then simply run it with:
```bash
$ python main.py

```

As a bonus, on OS X, you can set the wallpaper to the one just downloaded for you:
```bash
$ python main.py 2> /dev/null && wall=$(readlink -f wallpaper) && osascript -e "tell application \"Finder\" to set desktop picture to POSIX file \"$wall\""
```

In addition, the output path will be printed to the standard output, so, if you prefer, you can get it with:
```bash
$ wall=$(python main.py 2> /dev/null)  # suppress logs
```
_Note_: due to a limitation in the AppleScript syntax, it will only change the wallpaper of the currently selected space.

## Configuration
You can configure RedditWallpaperChooser by editing the file `RedditWallpaperChooser/constants.py`.
Specifically, you can configure the subreddits to parse, your username and your password (to enlarge the Reddit API limits, in the unique case you need it), the output file, and so on.

## Future improvements
Add specific parsers for popular image hosting sites such as:

* http://imgur.com/
* https://www.flickr.com/

Filter wallpaper choice by color.
Avoid choosing again used images.
Add a proper test suite.
Add better configuration handling.
