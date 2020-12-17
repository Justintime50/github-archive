import logging
import logging.handlers
import os

GITHUB_ARCHIVE_LOCATION = os.path.expanduser(
    os.getenv('GITHUB_ARCHIVE_LOCATION', '~/github-archive')
)
LOG_PATH = os.path.join(GITHUB_ARCHIVE_LOCATION, 'logs')
LOG_FILE = os.path.join(LOG_PATH, 'github-archive.log')
LOG_MAX_BYTES = int(os.getenv('GITHUB_ARCHIVE_LOG_MAX_BYTES', 200000))
LOG_BACKUP_COUNT = int(os.getenv('GITHUB_ARCHIVE_LOG_BACKUP_COUNT', 5))


class Logger():
    @staticmethod
    def _setup_logging(logger):
        """Setup project logging (to console and log file)
        """
        if not os.path.exists(LOG_PATH):
            os.makedirs(LOG_PATH)
        logger.setLevel(logging.INFO)
        handler = logging.handlers.RotatingFileHandler(
            LOG_FILE,
            maxBytes=LOG_MAX_BYTES,
            backupCount=LOG_BACKUP_COUNT
        )
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(logging.StreamHandler())
        logger.addHandler(handler)
