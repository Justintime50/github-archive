import logging
import logging.handlers
import os

# 200kb * 5 files = 1mb of logs
LOG_MAX_BYTES = 200000  # 200kb
LOG_BACKUP_COUNT = 5


class Logger:
    @staticmethod
    def setup_logging(logger, location):
        """Setup project logging (to console and log file)"""
        log_path = os.path.join(location, 'logs')
        log_file = os.path.join(log_path, 'github-archive.log')

        if not os.path.exists(log_path):
            os.makedirs(log_path)

        logger.setLevel(logging.INFO)
        handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=LOG_MAX_BYTES,
            backupCount=LOG_BACKUP_COUNT,
        )
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(logging.StreamHandler())
        logger.addHandler(handler)
