#!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

import os
import os.path
import sys

from .constants import OUTPUT_PATH

exists = os.path.exists(OUTPUT_PATH)
is_dir = os.path.isdir(OUTPUT_PATH)


if exists and not is_dir:
    print(
        "The output path '{}' already exists and is not a directory. I can't continue.".format(
            OUTPUT_PATH
        ), file=sys.stderr
    )
    sys.exit(False)

if not exists:
    os.mkdir(OUTPUT_PATH)
