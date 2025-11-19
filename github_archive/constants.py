import os
from typing import Literal


DEFAULT_BASE_URL = "https://api.github.com"
DEFAULT_LOCATION = os.path.join("~", "github-archive")
DEFAULT_NUM_THREADS = 10
DEFAULT_TIMEOUT = 300

DEFAULT_LOG_LEVEL = "info"
LOG_LEVEL_CHOICES = Literal[
    "debug",
    "info",
    "warning",
    "error",
    "critical",
]

LOGGER_NAME = "github-archive"

CLONE_OPERATION = "clone"
PULL_OPERATION = "pull"

GIST_CONTEXT = "gist"
ORG_CONTEXT = "org"
PERSONAL_CONTEXT = "personal"
STAR_CONTEXT = "star"
USER_CONTEXT = "user"
