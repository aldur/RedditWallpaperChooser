# RedditWallpaperChooser

RedditWallpaperChooser will download from any subreddit of your choice the trending wallpapers of the day.

__Caution:__ RedditWallpaperChooser is still a work in progress.

## Features

* Choose the subreddits you like.
* Filter by aspect ratio and image size.
* Python 2 and Python 3 compatibility.

## Requirements

We support the following Python versions:

* Python 2.7 or greater.
* Python 3.4 or greater.

Additional requirements are listed in the `requirements.txt` file.

## Installation & Usage

Until RedditWallpaperChooser will land on PyPi you can install it as follows:

```bash
$ git clone https://github.com/aldur/RedditWallpaperChooser/
$ cd RedditWallpaperChooser
$ pip install . .[extras]  # --user could also help you
```

You'll find `RedditWallpaperChooser` in your `PATH`. You can now start collecting wallpapers.

```bash
$ RedditWallpaperChooser
```

The absolute path of one of the downloaded wallpapers will be printed to standard output.

### macOS

As a bonus, on macOS, you can set the wallpaper to the one just downloaded for you:
```bash
$ wall=$(./bin/RedditWallpaperChooser 2> /dev/null) && osascript -e "tell application \"Finder\" to set desktop picture to POSIX file \"$wall\""
```

_Note_: due to a limitation of the macOS APIs, it will only change the wallpaper of the currently selected space.

## Configuration

You can configure RedditWallpaperChooser by providing a `ini` configuration file.
In it, you can specify the following general options:

- the subreddits to parse (`subreddits`)
- the number of results per subreddit (`result_limit`)
- your username and your password (just in case you need to increase Reddit API limits) (`username` and `password`)
- the output directory (`output_folder`)
- a regex filter to apply to the wallpaper names (`re_filter`)

Additionally, you can also filter the candidate wallpapers to be selected and returned at the end of the download process:

- by aspect ratio (`aspect_ratio`)
- by size (`size`)

Until better documentation will be developed please refer to the default configuration options as a working example;
You can dump it as follows:

```bash
$ RedditWallpaperChooser -d config.ini
```

You can then use your configuration with:

```bash
$ RedditWallpaperChooser -c config.ini
```

## Future improvements

- Add specific parsers for popular image hosting sites such as:
    * https://imgur.com/
    * https://www.flickr.com/
- Filter and chooser wallpapers by color.
- Avoid choosing again the same images.
- Add a proper test suite.
