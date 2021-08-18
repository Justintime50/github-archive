import logging
import logging.handlers
import os

from github_archive.constants import DEFAULT_LOCATION

LOG_PATH = os.path.join(DEFAULT_LOCATION, 'logs')
LOG_FILE = os.path.join(LOG_PATH, 'github-archive.log')

# 200kb * 5 files = 1mb of logs
LOG_MAX_BYTES = 200000  # 200kb
LOG_BACKUP_COUNT = 5


class Logger:
    @staticmethod
    def _setup_logging(logger):
        """Setup project logging (to console and log file)"""
        if not os.path.exists(LOG_PATH):
            os.makedirs(LOG_PATH)
        logger.setLevel(logging.INFO)
        handler = logging.handlers.RotatingFileHandler(
            LOG_FILE,
            maxBytes=LOG_MAX_BYTES,
            backupCount=LOG_BACKUP_COUNT,
        )
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(logging.StreamHandler())
        logger.addHandler(handler)
