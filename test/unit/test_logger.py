import os

import mock
from github_archive.logger import Logger

LOG_PATH = 'test/mock-dir'
LOG_FILE = './test/test.log'


@mock.patch('os.makedirs')
@mock.patch('github_archive.archive.LOGGER')
def test_setup_logging(mock_logger, mock_make_dirs):
    with mock.patch('builtins.open', mock.mock_open()):
        Logger.setup_logging(mock_logger, LOG_PATH)
    mock_make_dirs.assert_called_once()
    mock_logger.setLevel.assert_called()
    mock_logger.addHandler.assert_called()


@mock.patch('os.makedirs')
@mock.patch('github_archive.archive.LOGGER')
def test_setup_logging_dir_exists(mock_logger, mock_make_dirs):
    # TODO: Mock this better so we don't need a gitignored empty folder for testing
    if not os.path.exists('./logs'):
        os.mkdir('logs')

    with mock.patch('builtins.open', mock.mock_open()):
        Logger.setup_logging(mock_logger, './')
    mock_make_dirs.assert_not_called()
    mock_logger.setLevel.assert_called()
    mock_logger.addHandler.assert_called()
