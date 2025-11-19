from unittest.mock import patch

from github_archive import GithubArchive
from github_archive.logger import setup_logger


@patch("woodchips.Logger")
def test_setup_logger(mock_logger):
    """Test that we setup the `woodchips` logger correctly and that it returns a logger instance."""
    github_archive = GithubArchive()
    setup_logger(github_archive)

    mock_logger.assert_called_once()
