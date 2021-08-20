import subprocess
from threading import BoundedSemaphore

import mock
import pytest
from github_archive import GithubArchive
from github_archive.archive import CLONE_OPERATION, DEFAULT_NUM_THREADS, PERSONAL_CONTEXT, PULL_OPERATION

GITHUB_TOKEN = '123'
ORG_LIST = 'org1, org2'
USER_LIST = 'user1, user2'


def mock_thread_limiter():
    thread_limiter = BoundedSemaphore(DEFAULT_NUM_THREADS)

    return thread_limiter


@mock.patch('os.path.exists', return_value=False)
@mock.patch('os.makedirs')
def test_initialize_project(mock_make_dirs, mock_dir_exist):
    GithubArchive().initialize_project()

    assert mock_make_dirs.call_count == 2


@mock.patch('github_archive.archive.LOGGER')
def test_initialize_project_missing_list(mock_logger):
    # TODO: Is it possible to test all variations easily in one test?
    # Parametrize doesn't work great because we can't easily swap the param name being used
    message = 'A git operation must be specified when a list of users or orgs is provided.'
    with pytest.raises(ValueError) as error:
        GithubArchive(users='justintime50').initialize_project()

    mock_logger.critical.assert_called_with(message)
    assert message == str(error.value)


@mock.patch('github_archive.archive.LOGGER')
def test_initialize_project_missing_operation(mock_logger):
    # TODO: Is it possible to test all variations easily in one test?
    # Parametrize doesn't work great because we can't easily swap the param name being used
    message = 'A list must be provided when a git operation is specified.'
    with pytest.raises(ValueError) as error:
        GithubArchive(
            clone=True,
        ).initialize_project()

    mock_logger.critical.assert_called_with(message)
    assert message == str(error.value)


@mock.patch('github_archive.archive.Github.get_user')
def test_get_personal_repos(mock_get_user):
    GithubArchive(
        token='123',
        users='justintime50',
    ).get_personal_repos()

    mock_get_user.assert_called_once()


@mock.patch('github_archive.archive.Github')
@mock.patch('github_archive.archive.Github.get_repos')
@mock.patch('github_archive.archive.Github.get_user')
def test_get_all_user_repos(mock_get_user, mock_get_repos, mock_github_instance):
    users = 'justintime50,user2'
    GithubArchive(
        users=users,
    ).get_all_user_repos()

    mock_get_user.call_count == len(users)
    mock_get_repos.call_count == len(users)


@mock.patch('github_archive.archive.Github')
@mock.patch('github_archive.archive.Github.get_repos')
@mock.patch('github_archive.archive.Github.get_organization')
def test_get_all_org_repos(mock_get_org, mock_get_repos, mock_github_instance):
    orgs = 'org1,org2'
    GithubArchive(
        orgs=orgs,
    ).get_all_org_repos()

    mock_get_org.call_count == len(orgs)
    mock_get_repos.call_count == len(orgs)


@mock.patch('github_archive.archive.Github')
@mock.patch('github_archive.archive.Github.get_gists')
@mock.patch('github_archive.archive.Github.get_user')
def test_get_get_all_gists(mock_get_user, mock_get_gists, mock_github_instance):
    gists = 'justintime50,user2'
    GithubArchive(
        gists=gists,
    ).get_all_gists()

    mock_get_user.call_count == len(gists)
    mock_get_gists.call_count == len(gists)


@mock.patch('github_archive.archive.Github')
@mock.patch('github_archive.archive.GithubArchive.archive_repo')
def test_iterate_repos_not_matching_authed_username(mock_archive_repo, mock_github_instance, mock_git_asset):
    repos = [mock_git_asset]
    GithubArchive(
        users='mock_username',
    ).iterate_repos_to_archive(repos, PERSONAL_CONTEXT, CLONE_OPERATION)

    mock_archive_repo.assert_called()


@mock.patch('github_archive.archive.Github')
@mock.patch('github_archive.archive.GithubArchive.archive_repo')
def test_iterate_repos_matching_authed_username(mock_archive_repo, mock_github_instance, mock_git_asset):
    repos = [mock_git_asset]
    GithubArchive(
        token='123',
        users='mock_username',
    ).iterate_repos_to_archive(repos, PERSONAL_CONTEXT, CLONE_OPERATION)

    mock_archive_repo.assert_not_called()


@mock.patch('github_archive.archive.Github')
@mock.patch('github_archive.archive.GithubArchive.archive_gist')
def test_iterate_gists(mock_archive_gist, mock_github_instance, mock_git_asset):
    gists = [mock_git_asset]
    GithubArchive(
        gists='mock_username',
    ).iterate_gists_to_archive(gists, CLONE_OPERATION)

    mock_archive_gist.assert_called()


@mock.patch('github_archive.archive.LOGGER')
def test_view_repos(mock_logger, mock_git_asset):
    repos = [mock_git_asset]
    GithubArchive().view_repos(repos)

    mock_logger.info.assert_called_with('mock_username/mock-asset-name')


@mock.patch('github_archive.archive.LOGGER')
def test_view_gists(mock_logger, mock_git_asset):
    gists = [mock_git_asset]
    GithubArchive().view_gists(gists)

    mock_logger.info.assert_called_with('mock_username/123')


@mock.patch('subprocess.run')
@mock.patch('github_archive.archive.LOGGER')
def test_archive_repo_success(mock_logger, mock_subprocess, mock_git_asset):
    # TODO: Mock the subprocess better to ensure it's doing what it should
    operation = CLONE_OPERATION
    message = f'Repo: {mock_git_asset.name} {operation} success!'
    GithubArchive().archive_repo(mock_thread_limiter(), mock_git_asset, 'mock/path', operation)

    mock_logger.info.assert_called_once_with(message)


@mock.patch('os.path.exists', return_value=True)
@mock.patch('subprocess.run')
@mock.patch('github_archive.archive.LOGGER')
def test_archive_repo_clone_exists(mock_logger, mock_subprocess, mock_path_exists, mock_git_asset):
    operation = CLONE_OPERATION
    GithubArchive().archive_repo(mock_thread_limiter(), mock_git_asset, 'mock/path', operation)

    mock_logger.info.assert_not_called()


@mock.patch('subprocess.run', side_effect=subprocess.TimeoutExpired(cmd=subprocess.run, timeout=0.1))
@mock.patch('github_archive.archive.LOGGER')
def test_archive_repo_timeout_exception(mock_logger, mock_subprocess, mock_git_asset):
    operation = CLONE_OPERATION
    message = f'Git operation timed out archiving {mock_git_asset.name}.'
    GithubArchive().archive_repo(mock_thread_limiter(), mock_git_asset, 'mock/path', operation)

    mock_logger.error.assert_called_with(message)


@mock.patch('subprocess.run', side_effect=subprocess.CalledProcessError(returncode=1, cmd=subprocess.run))
@mock.patch('github_archive.archive.LOGGER')
def test_archive_repo_called_process_error(mock_logger, mock_subprocess, mock_git_asset):
    operation = PULL_OPERATION
    GithubArchive().archive_repo(mock_thread_limiter(), mock_git_asset, 'mock/path', operation)

    mock_logger.error.assert_called()


@mock.patch('subprocess.run')
@mock.patch('github_archive.archive.LOGGER')
def test_archive_gist_success(mock_logger, mock_subprocess, mock_git_asset):
    # TODO: Mock the subprocess better to ensure it's doing what it should
    operation = CLONE_OPERATION
    message = f'Gist: {mock_git_asset.id} {operation} success!'
    GithubArchive().archive_gist(mock_thread_limiter(), mock_git_asset, 'mock/path', operation)

    mock_logger.info.assert_called_once_with(message)


@mock.patch('os.path.exists', return_value=True)
@mock.patch('subprocess.run')
@mock.patch('github_archive.archive.LOGGER')
def test_archive_gist_clone_exists(mock_logger, mock_subprocess, mock_path_exists, mock_git_asset):
    operation = CLONE_OPERATION
    GithubArchive().archive_gist(mock_thread_limiter(), mock_git_asset, 'mock/path', operation)

    mock_logger.info.assert_not_called()


@mock.patch('subprocess.run', side_effect=subprocess.TimeoutExpired(cmd=subprocess.run, timeout=0.1))
@mock.patch('github_archive.archive.LOGGER')
def test_archive_gist_timeout_exception(mock_logger, mock_subprocess, mock_git_asset):
    operation = CLONE_OPERATION
    message = f'Git operation timed out archiving {mock_git_asset.id}.'
    GithubArchive().archive_gist(mock_thread_limiter(), mock_git_asset, 'mock/path', operation)
    mock_logger.error.assert_called_with(message)


@mock.patch('subprocess.run', side_effect=subprocess.CalledProcessError(returncode=1, cmd=subprocess.run))
@mock.patch('github_archive.archive.LOGGER')
def test_archive_gist_called_process_error(mock_logger, mock_subprocess, mock_git_asset):
    operation = PULL_OPERATION
    GithubArchive().archive_gist(mock_thread_limiter(), mock_git_asset, 'mock/path', operation)
    mock_logger.error.assert_called()
