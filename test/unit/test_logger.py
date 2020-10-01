import mock
from github_archive.logger import Logger


@mock.patch('github_archive.logger.LOG_PATH', 'test/mock-dir')
@mock.patch('github_archive.logger.LOG_FILE', './test/test.log')
@mock.patch('os.makedirs')
@mock.patch('github_archive.archive.LOGGER')
def test_setup_logging(mock_logger, mock_make_dirs):
    with mock.patch('builtins.open', mock.mock_open()):
        Logger._setup_logging(mock_logger)
    mock_make_dirs.assert_called_once()
    mock_logger.setLevel.assert_called()
    mock_logger.addHandler.assert_called()


@mock.patch('os.makedirs')
@mock.patch('github_archive.archive.LOGGER')
def test_setup_logging_dir_exists(mock_logger, mock_make_dirs):
    with mock.patch('builtins.open', mock.mock_open()):
        Logger._setup_logging(mock_logger)
    mock_make_dirs.assert_not_called()
    mock_logger.setLevel.assert_called()
    mock_logger.addHandler.assert_called()
