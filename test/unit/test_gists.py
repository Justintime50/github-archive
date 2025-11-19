import subprocess
from unittest.mock import (
    MagicMock,
    patch,
)

from github import Gist

from github_archive import GithubArchive
from github_archive.archive import (
    CLONE_OPERATION,
    PULL_OPERATION,
)
from github_archive.gists import (
    _archive_gist,
    _fork_gist,
    iterate_gists_to_archive,
    iterate_gists_to_fork,
    view_gists,
)


@patch("github_archive.archive.Github")
@patch("github_archive.gists._archive_gist")
def test_iterate_gists(mock_archive_gist, mock_github_instance, mock_git_asset):
    gists = [mock_git_asset]
    github_archive = GithubArchive(
        gists="mock_username",
    )

    iterate_gists_to_archive(github_archive, gists, CLONE_OPERATION)

    mock_archive_gist.assert_called()


@patch("subprocess.check_output")
@patch("logging.Logger.info")
def test_archive_gist_success(mock_logger, mock_subprocess, mock_git_asset):
    operation = CLONE_OPERATION
    message = f"Gist: {mock_git_asset.owner.login}/{mock_git_asset.id} {operation} success!"
    github_archive = GithubArchive()
    _archive_gist(github_archive, mock_git_asset, "mock/path", operation)

    mock_subprocess.assert_called_once_with(
        ["git", "clone", "mock/html_url", "mock/path"],
        stderr=-2,
        text=True,
        timeout=300,
    )
    mock_logger.assert_called_once_with(message)


@patch("os.path.exists", return_value=True)
@patch("subprocess.check_output")
@patch("logging.Logger.info")
def test_archive_gist_clone_exists(mock_logger, mock_subprocess, mock_path_exists, mock_git_asset):
    operation = CLONE_OPERATION
    github_archive = GithubArchive()
    _archive_gist(github_archive, mock_git_asset, "github_archive", operation)

    mock_subprocess.assert_not_called()


@patch("subprocess.check_output", side_effect=subprocess.TimeoutExpired(cmd="subprocess.check_output", timeout=0.1))
@patch("logging.Logger.error")
def test_archive_gist_timeout_exception(mock_logger, mock_subprocess, mock_git_asset):
    operation = CLONE_OPERATION
    message = f"Git operation timed out archiving {mock_git_asset.id}."
    github_archive = GithubArchive()
    _archive_gist(github_archive, mock_git_asset, "mock/path", operation)

    mock_logger.assert_called_with(message)


@patch(
    "subprocess.check_output", side_effect=subprocess.CalledProcessError(cmd="subprocess.check_output", returncode=1)
)
@patch("logging.Logger.error")
def test_archive_gist_called_process_error(mock_logger, mock_subprocess, mock_git_asset):
    operation = PULL_OPERATION
    github_archive = GithubArchive()
    _archive_gist(github_archive, mock_git_asset, "github_archive", operation)

    mock_logger.assert_called()


@patch("logging.Logger.info")
def test_view_gists(mock_logger, mock_git_asset):
    gists = [mock_git_asset]
    view_gists(gists)

    mock_logger.assert_called_with("mock_username/123")


@patch("github_archive.archive.Github")
@patch("github_archive.gists._fork_gist")
def test_iterate_gists_to_fork(mock_fork_gist, mock_github_instance):
    gist = MagicMock(spec=Gist.Gist)
    github_archive = GithubArchive(
        gists="mock_username",
    )

    iterate_gists_to_fork(github_archive, [gist])

    mock_fork_gist.assert_called_once()


@patch("logging.Logger.info")
@patch("github.Gist.Gist.create_fork")
def test_fork_gist_success(mock_create_fork, mock_logger):
    gist = MagicMock(spec=Gist.Gist)
    gist.create_fork = mock_create_fork
    _fork_gist(gist)

    mock_create_fork.assert_called_once()
    mock_logger.assert_called_once()


@patch("logging.Logger.warning")
@patch("github.Gist.Gist.create_fork", side_effect=Exception())
def test_fork_gist_failure(mock_create_fork, mock_logger):
    gist = MagicMock(spec=Gist.Gist)
    gist.create_fork = mock_create_fork
    _fork_gist(gist)

    mock_create_fork.assert_called_once()
    mock_logger.assert_called_once()
