import copy
import subprocess
from unittest.mock import (
    MagicMock,
    patch,
)

from github import Repository

from github_archive import GithubArchive
from github_archive.archive import (
    CLONE_OPERATION,
    PULL_OPERATION,
)
from github_archive.repos import (
    _archive_repo,
    _fork_repo,
    iterate_repos_to_archive,
    iterate_repos_to_fork,
    view_repos,
)


@patch("github_archive.archive.Github")
@patch("github_archive.repos._archive_repo")
def test_iterate_repos_not_matching_authed_username(mock_archive_repo, mock_github_instance, mock_git_asset):
    repos = [mock_git_asset]
    github_archive = GithubArchive(
        users="mock_username",
    )

    iterate_repos_to_archive(github_archive, repos, CLONE_OPERATION)

    mock_archive_repo.assert_called_once()


@patch("github_archive.archive.Github")
@patch("github_archive.repos._archive_repo")
def test_iterate_repos_matching_authed_username(mock_archive_repo, mock_github_instance, mock_git_asset):
    repos = [mock_git_asset]
    github_archive = GithubArchive(
        token="123",
        users="mock_username",  # matches the username of the git asset
    )

    iterate_repos_to_archive(github_archive, repos, CLONE_OPERATION)

    mock_archive_repo.assert_called_once()


@patch("github_archive.archive.Github")
@patch("github_archive.repos._archive_repo")
def test_iterate_repos_include_list(mock_archive_repo, mock_github_instance, mock_git_asset):
    """Tests that we iterate repos that are on the include list."""
    mock_non_include_asset = copy.deepcopy(mock_git_asset)
    mock_non_include_asset.name = "not-the-name"
    repos = [mock_git_asset, mock_non_include_asset]
    github_archive = GithubArchive(
        users="mock_username",
        include="mock-asset-name",
    )

    iterate_repos_to_archive(github_archive, repos, CLONE_OPERATION)

    mock_archive_repo.assert_called_once()  # Called once even though there are two, ensure we filtered


@patch("github_archive.archive.Github")
@patch("github_archive.repos._archive_repo")
def test_iterate_repos_exclude_list(mock_archive_repo, mock_github_instance, mock_git_asset):
    """Tests that we do not iterate repos that are on the exclude list."""
    mock_non_exclude_asset = copy.deepcopy(mock_git_asset)
    mock_non_exclude_asset.name = "not-the-name"
    repos = [mock_git_asset, mock_non_exclude_asset]
    github_archive = GithubArchive(
        users="mock_username",
        exclude="mock-asset-name",
    )

    iterate_repos_to_archive(github_archive, repos, CLONE_OPERATION)

    mock_archive_repo.assert_called_once()  # Called once even though there are two, ensure we filtered


@patch("github_archive.archive.Github")
@patch("github_archive.repos._archive_repo")
def test_iterate_repos_languages_list(mock_archive_repo, mock_github_instance, mock_git_asset):
    """Tests that we iterate repos that are one of the languages in the list."""
    mock_non_language_asset = copy.deepcopy(mock_git_asset)
    mock_non_language_asset.language = "Go"
    repos = [mock_git_asset, mock_non_language_asset]
    github_archive = GithubArchive(
        users="mock_username",
        languages="python",
    )

    iterate_repos_to_archive(github_archive, repos, CLONE_OPERATION)

    mock_archive_repo.assert_called_once()  # Called once even though there are two, ensure we filtered


@patch("logging.Logger.info")
def test_view_repos(mock_logger, mock_git_asset):
    repos = [mock_git_asset]
    view_repos(repos)

    mock_logger.assert_called_with("mock_username/mock-asset-name")


@patch("github_archive.archive.Github")
@patch("subprocess.check_output")
@patch("logging.Logger.info")
def test_archive_repo_success(mock_logger, mock_subprocess, mock_github, mock_git_asset):
    operation = CLONE_OPERATION
    message = f"Repo: {mock_git_asset.owner.login}/{mock_git_asset.name} {operation} success!"
    github_archive = GithubArchive(token="123")
    _archive_repo(github_archive, mock_git_asset, "mock/path", operation)

    mock_subprocess.assert_called_once_with(
        ["git", "clone", "mock/ssh_url", "mock/path"],
        stderr=-2,
        text=True,
        timeout=300,
    )
    mock_logger.assert_called_once_with(message)


@patch("subprocess.check_output")
@patch("logging.Logger.info")
def test_archive_repo_use_https_success(mock_logger, mock_subprocess, mock_git_asset):
    operation = CLONE_OPERATION
    message = f"Repo: {mock_git_asset.owner.login}/{mock_git_asset.name} {operation} success!"
    github_archive = GithubArchive(
        use_https=True,
    )
    _archive_repo(github_archive, mock_git_asset, "mock/path", operation)

    mock_subprocess.assert_called_once_with(
        ["git", "clone", "mock/html_url", "mock/path"],
        stderr=-2,
        text=True,
        timeout=300,
    )
    mock_logger.assert_called_once_with(message)


@patch("os.path.join", return_value="mock_user/mock_repo")
@patch("os.path.exists", return_value=True)
@patch("subprocess.check_output")
@patch("logging.Logger.info")
def test_archive_repo_clone_exists(mock_logger, mock_subprocess, mock_path_exists, mock_path_join, mock_git_asset):
    operation = CLONE_OPERATION
    github_archive = GithubArchive()
    _archive_repo(github_archive, mock_git_asset, "github_archive", operation)

    mock_subprocess.assert_not_called()


@patch("subprocess.check_output", side_effect=subprocess.TimeoutExpired(cmd="subprocess.check_output", timeout=0.1))
@patch("logging.Logger.error")
def test_archive_repo_timeout_exception(mock_logger, mock_subprocess, mock_git_asset):
    operation = CLONE_OPERATION
    message = f"Git operation timed out archiving {mock_git_asset.name}."
    github_archive = GithubArchive()
    _archive_repo(github_archive, mock_git_asset, "mock/path", operation)

    mock_logger.assert_called_with(message)


@patch(
    "subprocess.check_output", side_effect=subprocess.CalledProcessError(cmd="subprocess.check_output", returncode=1)
)
@patch("logging.Logger.error")
def test_archive_repo_called_process_error(mock_logger, mock_subprocess, mock_git_asset):
    operation = PULL_OPERATION
    github_archive = GithubArchive()
    _archive_repo(github_archive, mock_git_asset, "github_archive", operation)

    mock_logger.assert_called_once()


@patch("github_archive.archive.Github")
@patch("github_archive.repos._fork_repo")
def test_iterate_repos_to_fork(mock_fork_repo, mock_github_instance):
    repo = MagicMock(spec=Repository.Repository)
    github_archive = GithubArchive(
        gists="mock_username",
    )
    iterate_repos_to_fork(github_archive, [repo])

    mock_fork_repo.assert_called_once()


@patch("logging.Logger.info")
@patch("github.Repository.Repository.create_fork")
def test_fork_repo_success(mock_create_fork, mock_logger):
    repo = MagicMock(spec=Repository.Repository)
    repo.create_fork = mock_create_fork
    _fork_repo(repo)

    mock_create_fork.assert_called_once()
    mock_logger.assert_called_once()


@patch("logging.Logger.error")
@patch("github.Repository.Repository.create_fork", side_effect=Exception())
def test_fork_repo_failure(mock_create_fork, mock_logger):
    repo = MagicMock(spec=Repository.Repository)
    repo.create_fork = mock_create_fork
    _fork_repo(repo)

    mock_create_fork.assert_called_once()
    mock_logger.assert_called_once()
