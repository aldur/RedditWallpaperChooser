# RedditWallpaperChooser

RedditWallpaperChooser will parse the most popular subreddits of your choice in order to find the best and most trending wallpapers of the day.

__Caution:__ RedditWallpaperChooser is still a work in progress.

## Features

* Choose the subreddits you like.
* Select aspect ratio and image size as you wish.
* Compatible with both Python 2 and Python 3.

## Requirements

We support the following Python versions:

* Python 2.7 or greater.
* Python 3.4 or greater.

Needed requirements are listed in the `requirements.txt` file.

## Installation & Usage

Until RedditWallpaperChooser will land on PyPi you can install it as follows:

```bash
$ git clone https://github.com/aldur/RedditWallpaperChooser/
$ cd RedditWallpaperChooser
$ pip install -r requirements.txt  # --user could also help you
$ pip install -r requirements_extra.txt  # optional, if you want a few goodies
$ python setup.py develop
```

You can now start collecting wallpapers.

```bash
$ ./bin/RedditWallpaperChooser
```

The absolute path of one of the downloaded wallpapers will be printed on standard output.
As a bonus, on OS X, you can set the wallpaper to the one just downloaded for you:
```bash
$ wall=$(./bin/RedditWallpaperChooser 2> /dev/null) && osascript -e "tell application \"Finder\" to set desktop picture to POSIX file \"$wall\""
```

_Note_: due to a limitation of the OS X APIs, it will only change the wallpaper of the currently selected space.

## Configuration

You can configure RedditWallpaperChooser by providing to it a INI configuration file.
You can configure which subreddits to parse, 
your username and your password (to enlarge the Reddit API limits, in the unique case you need it), 
the output directory, and so on.

Until better documentation will be developed please refer to the default configuration options as a working example.
Default configuration can be dumped with:

```bash
$ ./bin/RedditWallpaperChooser -d config.ini
```

You can then use your configuration with:

```bash
$ ./bin/RedditWallpaperChooser -c config.ini
```

## Future improvements

Add specific parsers for popular image hosting sites such as:

* http://imgur.com/
* https://www.flickr.com/

Filter and chooser wallpapers by color.

Avoid choosing again the same images.

Add a proper test suite.
