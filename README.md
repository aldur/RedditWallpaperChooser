# RedditWallpaperChooser

RedditWallpaperChooser will download the trending wallpapers of the day from any subreddit of your choice.

## Features

* Choose the subreddits you like.
* Filter by aspect ratio and image size.

## Requirements

We make use of Python's 3 asynchronous APIs and `async`/`await` syntax.
For this reason, we only support Python versions ≥ 3.5.

Additional requirements are listed in the `requirements.txt` file.

## Installation & Usage

Until RedditWallpaperChooser will land on PyPi you can install it as follows:

```bash
$ git clone https://github.com/aldur/RedditWallpaperChooser/
$ cd RedditWallpaperChooser
$ pip install . .[extras]  # --user could also help you
```

You'll find `reddit-wallpaper-chooser` in your `PATH`. You can now start collecting wallpapers.

```bash
$ reddit-wallpaper-chooser
```

The absolute path of one of the downloaded wallpapers will be printed out to standard output.

### macOS

As a bonus, on macOS, you can set the wallpaper to the one just downloaded for you:
```bash
$ wall=$(reddit-wallpaper-chooser 2> /dev/null) && osascript -e "tell application \"Finder\" to set desktop picture to POSIX file \"$wall\""
```

_Note_: due to a limitation of the macOS APIs, it will only change the wallpaper of the currently selected space.

## Configuration

You can configure RedditWallpaperChooser by providing a `ini` configuration file.
In it, you can specify the following general options:

- the subreddits to parse (`subreddits`)
- the number of results per subreddit (`result_limit`)
- the output directory (`output_folder`)
- the subreddit sorting (`sorting`)
- a time parameter for 'top'/'controversial' sorting (`time`)

Additionally, you can also filter the candidate wallpapers to be selected and returned at the end of the download process:

- by aspect ratio (`aspect_ratio`)
- by minimum size (`size`)

Until better documentation will be developed please refer to the default configuration options as a working example;
You can dump it as follows:

```bash
$ reddit-wallpaper-chooser -d config.ini
```

You can then use your configuration with:

```bash
$ reddit-wallpaper-chooser -c config.ini
```

## Future improvements

- Filter wallpapers by color.
- Avoid choosing again the same images.
- Add a proper test suite.
