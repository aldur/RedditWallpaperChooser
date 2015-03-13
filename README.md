# RedditWallpaperChooser
RedditWallpaperChooser will parse the most popular subreddits of your choice in order to find the best and most trending wallpapers of the day.

__Caution:__ RedditWallpaperChooser is still a work in progress.

## Requirements
We support the following Python versions:

* Python 2.7 or greater.
* Python 3.3 or greater.

Any other requirement is listed in the `requirements.txt` file.

## Installation
Until RedditWallpaperChooser will land on PyPi (soon) you can install it by simply:

```bash
$ git clone https://github.com/aldur/RedditWallpaperChooser/
$ cd RedditWallpaperChooser
$ pip install -r requirements.txt
$ # optionally edit the file RedditWallpaperChooser/constants.py
$ python main.py
```

## Configuration
You can configure RedditWallpaperChooser by editing the file `RedditWallpaperChooser/constants.py`.
Specifically, you can configure the subreddits to parse, your username and your password (to enlarge the Reddit API limits), the output file, and so on.

## Future improvements
Add specific parsers for popular image hosting sites such as:

* http://imgur.com/
* https://www.flickr.com/

Filter images by dimension, size, colors, and so on.
Add a proper test suite.
