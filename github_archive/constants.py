import os

from typing_extensions import (
    Literal,
)


DEFAULT_BASE_URL = 'https://api.github.com'
DEFAULT_LOCATION = os.path.expanduser(os.path.join('~', 'github-archive'))
DEFAULT_NUM_THREADS = 10
DEFAULT_TIMEOUT = 300

DEFAULT_LOG_LEVEL = 'info'
LOG_LEVEL_CHOICES = Literal[
    'debug',
    'info',
    'warning',
    'error',
    'critical',
]
