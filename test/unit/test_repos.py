import subprocess
from unittest.mock import patch

from github_archive import GithubArchive
from github_archive.archive import (
    CLONE_OPERATION,
    PULL_OPERATION,
)
from github_archive.repos import (
    _archive_repo,
    iterate_repos_to_archive,
    view_repos,
)


@patch('github_archive.archive.Github')
@patch('github_archive.repos._archive_repo')
def test_iterate_repos_not_matching_authed_username(mock_archive_repo, mock_github_instance, mock_git_asset):
    repos = [mock_git_asset]
    github_archive = GithubArchive(
        users='mock_username',
    )

    iterate_repos_to_archive(github_archive, repos, CLONE_OPERATION)

    mock_archive_repo.assert_called_once()


@patch('github_archive.archive.Github')
@patch('github_archive.repos._archive_repo')
def test_iterate_repos_matching_authed_username(mock_archive_repo, mock_github_instance, mock_git_asset):
    repos = [mock_git_asset]
    github_archive = GithubArchive(
        token='123',
        users='mock_username',  # matches the username of the git asset
    )

    iterate_repos_to_archive(github_archive, repos, CLONE_OPERATION)

    mock_archive_repo.assert_called_once()


@patch('github_archive.archive.Github')
@patch('github_archive.repos._archive_repo')
def test_iterate_repos_include_list(mock_archive_repo, mock_github_instance, mock_git_asset):
    """Tests that we iterate repos that are on the include list."""
    repos = [mock_git_asset]
    github_archive = GithubArchive(
        users='mock_username',
        include='mock-asset-name',
    )

    iterate_repos_to_archive(github_archive, repos, CLONE_OPERATION)

    mock_archive_repo.assert_called_once()


@patch('github_archive.archive.Github')
@patch('github_archive.repos._archive_repo')
def test_iterate_repos_exclude_list(mock_archive_repo, mock_github_instance, mock_git_asset):
    """Tests that we do not iterate repos that are on the exclude list."""
    repos = [mock_git_asset]
    github_archive = GithubArchive(
        users='mock_username',
        exclude='mock-asset-name',
    )

    iterate_repos_to_archive(github_archive, repos, CLONE_OPERATION)

    mock_archive_repo.assert_not_called()


@patch('logging.Logger.info')
def test_view_repos(mock_logger, mock_git_asset):
    repos = [mock_git_asset]
    view_repos(repos)

    mock_logger.assert_called_with('mock_username/mock-asset-name')


@patch('subprocess.run')
@patch('logging.Logger.info')
def test_archive_repo_success(mock_logger, mock_subprocess, mock_git_asset):
    # TODO: Mock the subprocess better to ensure it's doing what it should
    operation = CLONE_OPERATION
    message = f'Repo: {mock_git_asset.owner.login}/{mock_git_asset.name} {operation} success!'
    github_archive = GithubArchive()
    _archive_repo(github_archive, mock_git_asset, 'mock/path', operation)

    mock_subprocess.assert_called()
    mock_logger.assert_called_once_with(message)


@patch('subprocess.run')
@patch('logging.Logger.info')
def test_archive_repo_use_https_success(mock_logger, mock_subprocess, mock_git_asset):
    # TODO: Mock the subprocess better to ensure it's doing what it should
    operation = CLONE_OPERATION
    message = f'Repo: {mock_git_asset.owner.login}/{mock_git_asset.name} {operation} success!'
    github_archive = GithubArchive(
        use_https=True,
    )
    _archive_repo(github_archive, mock_git_asset, 'mock/path', operation)

    mock_subprocess.assert_called()
    mock_logger.assert_called_once_with(message)


@patch('os.path.join', return_value='mock_user/mock_repo')
@patch('os.path.exists', return_value=True)
@patch('subprocess.run')
@patch('logging.Logger.info')
def test_archive_repo_clone_exists(mock_logger, mock_subprocess, mock_path_exists, mock_path_join, mock_git_asset):
    operation = CLONE_OPERATION
    github_archive = GithubArchive()
    _archive_repo(github_archive, mock_git_asset, 'github_archive', operation)

    mock_subprocess.assert_not_called()


@patch('subprocess.run', side_effect=subprocess.TimeoutExpired(cmd='subprocess.run', timeout=0.1))
@patch('logging.Logger.error')
def test_archive_repo_timeout_exception(mock_logger, mock_subprocess, mock_git_asset):
    operation = CLONE_OPERATION
    message = f'Git operation timed out archiving {mock_git_asset.name}.'
    github_archive = GithubArchive()
    _archive_repo(github_archive, mock_git_asset, 'mock/path', operation)

    mock_logger.assert_called_with(message)


@patch('subprocess.run', side_effect=subprocess.CalledProcessError(returncode=1, cmd='subprocess.run'))
@patch('logging.Logger.error')
def test_archive_repo_called_process_error(mock_logger, mock_subprocess, mock_git_asset):
    operation = PULL_OPERATION
    github_archive = GithubArchive()
    _archive_repo(github_archive, mock_git_asset, 'github_archive', operation)

    mock_logger.assert_called_once()
