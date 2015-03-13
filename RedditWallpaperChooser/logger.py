#!/usr/bin/env python
# encoding: utf-8

import logging
import logging.config

# Logging configuration
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },

    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },

    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
})

logger = logging.getLogger("RedditWallpaperChooser")
logger.setLevel(logging.DEBUG)

logging.getLogger("requests").setLevel(logging.WARNING)
