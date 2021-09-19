import subprocess
from threading import BoundedSemaphore
from unittest.mock import patch

import pytest
from github_archive import GithubArchive
from github_archive.archive import (
    CLONE_OPERATION,
    DEFAULT_NUM_THREADS,
    GIST_CONTEXT,
    ORG_CONTEXT,
    PULL_OPERATION,
    USER_CONTEXT,
)


def mock_thread_limiter():
    thread_limiter = BoundedSemaphore(DEFAULT_NUM_THREADS)

    return thread_limiter


@patch('github_archive.archive.Github.get_user')
@patch('github_archive.archive.GithubArchive.authenticated_user_in_users', return_value=True)
@patch('github_archive.archive.GithubArchive.view_repos')
@patch('github_archive.archive.GithubArchive.get_all_git_assets')
def test_run_token_view(mock_get_all_git_assets, mock_view_repos, mock_authed_user_in_users, mock_get_user):
    github_archive = GithubArchive(
        token='123',
        users='justintime50',
        view=True,
    )

    github_archive.authenticated_username = 'justintime50'
    github_archive.run()

    mock_get_all_git_assets.assert_called_once()
    mock_view_repos.assert_called_once()
    assert github_archive.users == []  # Assert the authed user gets removed from list


@patch('github_archive.archive.Github.get_user')
@patch('github_archive.archive.GithubArchive.authenticated_user_in_users', return_value=True)
@patch('github_archive.archive.GithubArchive.iterate_repos_to_archive')
@patch('github_archive.archive.GithubArchive.get_all_git_assets')
def test_run_token_clone(
    mock_get_all_git_assets, mock_iterate_repos_to_archive, mock_authed_user_in_users, mock_get_user
):
    github_archive = GithubArchive(
        token='123',
        users='justintime50',
        clone=True,
    )

    github_archive.authenticated_username = 'justintime50'
    github_archive.run()

    mock_get_all_git_assets.assert_called_once()
    mock_iterate_repos_to_archive.assert_called_once_with(mock_get_all_git_assets(), CLONE_OPERATION)
    assert github_archive.users == []  # Assert the authed user gets removed from list


@patch('github_archive.archive.Github.get_user')
@patch('github_archive.archive.GithubArchive.authenticated_user_in_users', return_value=True)
@patch('github_archive.archive.GithubArchive.iterate_repos_to_archive')
@patch('github_archive.archive.GithubArchive.get_all_git_assets')
def test_run_token_pull(
    mock_get_all_git_assets, mock_iterate_repos_to_archive, mock_authed_user_in_users, mock_get_user
):
    github_archive = GithubArchive(
        token='123',
        users='justintime50',
        pull=True,
    )

    github_archive.authenticated_username = 'justintime50'
    github_archive.run()

    mock_get_all_git_assets.assert_called_once()
    mock_iterate_repos_to_archive.assert_called_once_with(mock_get_all_git_assets(), PULL_OPERATION)
    assert github_archive.users == []  # Assert the authed user gets removed from list


@patch('github_archive.archive.GithubArchive.view_repos')
@patch('github_archive.archive.GithubArchive.get_all_git_assets')
def test_run_users_view(mock_get_all_git_assets, mock_view_repos):
    GithubArchive(
        users='justintime50',
        view=True,
    ).run()

    mock_get_all_git_assets.assert_called_once()
    mock_view_repos.assert_called_once()


@patch('github_archive.archive.GithubArchive.iterate_repos_to_archive')
@patch('github_archive.archive.GithubArchive.get_all_git_assets')
def test_run_users_clone(mock_get_all_git_assets, mock_iterate_repos_to_archive):
    GithubArchive(
        users='justintime50',
        clone=True,
    ).run()

    mock_get_all_git_assets.assert_called_once()
    mock_iterate_repos_to_archive.assert_called_once_with(mock_get_all_git_assets(), CLONE_OPERATION)


@patch('github_archive.archive.GithubArchive.iterate_repos_to_archive')
@patch('github_archive.archive.GithubArchive.get_all_git_assets')
def test_run_users_pull(mock_get_all_git_assets, mock_iterate_repos_to_archive):
    GithubArchive(
        users='justintime50',
        pull=True,
    ).run()

    mock_get_all_git_assets.assert_called_once()
    mock_iterate_repos_to_archive.assert_called_once_with(mock_get_all_git_assets(), PULL_OPERATION)


@patch('github_archive.archive.GithubArchive.view_repos')
@patch('github_archive.archive.GithubArchive.get_all_git_assets')
def test_run_orgs_view(mock_get_all_git_assets, mock_view_repos):
    GithubArchive(
        orgs='org1',
        view=True,
    ).run()

    mock_get_all_git_assets.assert_called_once()
    mock_view_repos.assert_called_once()


@patch('github_archive.archive.GithubArchive.iterate_repos_to_archive')
@patch('github_archive.archive.GithubArchive.get_all_git_assets')
def test_run_orgs_clone(mock_get_all_git_assets, mock_iterate_repos_to_archive):
    GithubArchive(
        orgs='org1',
        clone=True,
    ).run()

    mock_get_all_git_assets.assert_called_once()
    mock_iterate_repos_to_archive.assert_called_once_with(mock_get_all_git_assets(), CLONE_OPERATION)


@patch('github_archive.archive.GithubArchive.iterate_repos_to_archive')
@patch('github_archive.archive.GithubArchive.get_all_git_assets')
def test_run_orgs_pull(mock_get_all_git_assets, mock_iterate_repos_to_archive):
    GithubArchive(
        orgs='org1',
        pull=True,
    ).run()

    mock_get_all_git_assets.assert_called_once()
    mock_iterate_repos_to_archive.assert_called_once_with(mock_get_all_git_assets(), PULL_OPERATION)


@patch('github_archive.archive.GithubArchive.view_gists')
@patch('github_archive.archive.GithubArchive.get_all_git_assets')
def test_run_gists_view(mock_get_all_git_assets, mock_view_gists):
    GithubArchive(
        gists='justintime50',
        view=True,
    ).run()

    mock_get_all_git_assets.assert_called_once()
    mock_view_gists.assert_called_once()


@patch('github_archive.archive.GithubArchive.iterate_gists_to_archive')
@patch('github_archive.archive.GithubArchive.get_all_git_assets')
def test_run_gists_clone(mock_get_all_git_assets, mock_iterate_gists_to_archive):
    GithubArchive(
        gists='org1',
        clone=True,
    ).run()

    mock_get_all_git_assets.assert_called_once()
    mock_iterate_gists_to_archive.assert_called_once_with(mock_get_all_git_assets(), CLONE_OPERATION)


@patch('github_archive.archive.GithubArchive.iterate_gists_to_archive')
@patch('github_archive.archive.GithubArchive.get_all_git_assets')
def test_run_gists_pull(mock_get_all_git_assets, mock_iterate_gists_to_archive):
    GithubArchive(
        gists='org1',
        pull=True,
    ).run()

    mock_get_all_git_assets.assert_called_once()
    mock_iterate_gists_to_archive.assert_called_once_with(mock_get_all_git_assets(), PULL_OPERATION)


@patch('github_archive.archive.GithubArchive.view_repos')
@patch('github_archive.archive.GithubArchive.get_all_git_assets')
def test_run_stars_view(mock_get_all_git_assets, mock_view_repos):
    GithubArchive(
        stars='justintime50',
        view=True,
    ).run()

    mock_get_all_git_assets.assert_called_once()
    mock_view_repos.assert_called_once()


@patch('github_archive.archive.GithubArchive.iterate_repos_to_archive')
@patch('github_archive.archive.GithubArchive.get_all_git_assets')
def test_run_stars_clone(mock_get_all_git_assets, mock_iterate_repos_to_archive):
    GithubArchive(
        stars='justintime50',
        clone=True,
    ).run()

    mock_get_all_git_assets.assert_called_once()
    mock_iterate_repos_to_archive.assert_called_once_with(mock_get_all_git_assets(), CLONE_OPERATION)


@patch('github_archive.archive.GithubArchive.iterate_repos_to_archive')
@patch('github_archive.archive.GithubArchive.get_all_git_assets')
def test_run_stars_pull(mock_get_all_git_assets, mock_iterate_repos_to_archive):
    GithubArchive(
        stars='justintime50',
        pull=True,
    ).run()

    mock_get_all_git_assets.assert_called_once()
    mock_iterate_repos_to_archive.assert_called_once_with(mock_get_all_git_assets(), PULL_OPERATION)


@patch('os.path.exists', return_value=False)
@patch('os.makedirs')
def test_initialize_project(mock_make_dirs, mock_dir_exist):
    GithubArchive().initialize_project()

    assert mock_make_dirs.call_count == 2


@patch('github_archive.archive.LOGGER')
def test_initialize_project_missing_list(mock_logger):
    # TODO: Is it possible to test all variations easily in one test?
    # Parametrize doesn't work great because we can't easily swap the param name being used
    message = 'A git operation must be specified when a list of users or orgs is provided.'
    with pytest.raises(ValueError) as error:
        GithubArchive(users='justintime50').initialize_project()

    mock_logger.critical.assert_called_with(message)
    assert message == str(error.value)


@patch('github_archive.archive.LOGGER')
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


@patch('github_archive.archive.Github.get_user')
def test_authenticated_user_in_users(mock_get_user):
    authenticated_user_in_users = GithubArchive(
        token='123',
        users='unauthenticated_user',
    ).authenticated_user_in_users()

    assert authenticated_user_in_users is False


@patch('github_archive.archive.Github.get_user')
def test_get_all_git_assets(mock_get_user):
    GithubArchive(
        users='justintime50',
    ).get_all_git_assets(USER_CONTEXT)

    mock_get_user.assert_called_once()


@patch('github_archive.archive.Github')
@patch('github_archive.archive.Github.get_repos')
@patch('github_archive.archive.Github.get_user')
def test_get_all_user_repos(mock_get_user, mock_get_repos, mock_github_instance):
    users = 'justintime50,user2'
    GithubArchive(
        users=users,
    ).get_all_git_assets(USER_CONTEXT)

    mock_get_user.call_count == len(users)
    mock_get_repos.call_count == len(users)
    # TODO: Assert the list returned


@patch('github_archive.archive.Github')
@patch('github_archive.archive.Github.get_repos')
@patch('github_archive.archive.Github.get_organization')
def test_get_all_org_repos(mock_get_org, mock_get_repos, mock_github_instance):
    orgs = 'org1,org2'
    GithubArchive(
        orgs=orgs,
    ).get_all_git_assets(ORG_CONTEXT)

    mock_get_org.call_count == len(orgs)
    mock_get_repos.call_count == len(orgs)
    # TODO: Assert the list returned


@patch('github_archive.archive.Github')
@patch('github_archive.archive.Github.get_gists')
@patch('github_archive.archive.Github.get_user')
def test_get_get_all_gists(mock_get_user, mock_get_gists, mock_github_instance):
    gists = 'justintime50,user2'
    GithubArchive(
        gists=gists,
    ).get_all_git_assets(GIST_CONTEXT)

    mock_get_user.call_count == len(gists)
    mock_get_gists.call_count == len(gists)
    # TODO: Assert the list returned


@patch('github_archive.archive.Github')
@patch('github_archive.archive.GithubArchive.archive_repo')
def test_iterate_repos_not_matching_authed_username(mock_archive_repo, mock_github_instance, mock_git_asset):
    repos = [mock_git_asset]
    GithubArchive(
        users='mock_username',
    ).iterate_repos_to_archive(repos, CLONE_OPERATION)

    mock_archive_repo.assert_called_once()


@patch('github_archive.archive.Github')
@patch('github_archive.archive.GithubArchive.archive_repo')
def test_iterate_repos_matching_authed_username(mock_archive_repo, mock_github_instance, mock_git_asset):
    repos = [mock_git_asset]
    GithubArchive(
        token='123',
        users='mock_username',  # matches the username of the git asset
    ).iterate_repos_to_archive(repos, CLONE_OPERATION)

    mock_archive_repo.assert_called_once()


@patch('github_archive.archive.Github')
@patch('github_archive.archive.GithubArchive.archive_gist')
def test_iterate_gists(mock_archive_gist, mock_github_instance, mock_git_asset):
    gists = [mock_git_asset]
    GithubArchive(
        gists='mock_username',
    ).iterate_gists_to_archive(gists, CLONE_OPERATION)

    mock_archive_gist.assert_called()


@patch('github_archive.archive.LOGGER')
def test_view_repos(mock_logger, mock_git_asset):
    repos = [mock_git_asset]
    GithubArchive().view_repos(repos)

    mock_logger.info.assert_called_with('mock_username/mock-asset-name')


@patch('github_archive.archive.LOGGER')
def test_view_gists(mock_logger, mock_git_asset):
    gists = [mock_git_asset]
    GithubArchive().view_gists(gists)

    mock_logger.info.assert_called_with('mock_username/123')


@patch('subprocess.run')
@patch('github_archive.archive.LOGGER')
def test_archive_repo_success(mock_logger, mock_subprocess, mock_git_asset):
    # TODO: Mock the subprocess better to ensure it's doing what it should
    operation = CLONE_OPERATION
    message = f'Repo: {mock_git_asset.owner.login}/{mock_git_asset.name} {operation} success!'
    GithubArchive().archive_repo(mock_thread_limiter(), mock_git_asset, 'mock/path', operation)

    mock_subprocess.assert_called()
    mock_logger.info.assert_called_once_with(message)


@patch('os.path.exists', return_value=True)
@patch('subprocess.run')
@patch('github_archive.archive.LOGGER')
def test_archive_repo_clone_exists(mock_logger, mock_subprocess, mock_git_asset):
    operation = CLONE_OPERATION
    GithubArchive().archive_repo(mock_thread_limiter(), mock_git_asset, 'github_archive', operation)

    mock_subprocess.assert_not_called()


@patch('shutil.rmtree')
@patch('subprocess.run', side_effect=subprocess.TimeoutExpired(cmd=subprocess.run, timeout=0.1))
@patch('github_archive.archive.LOGGER')
def test_archive_repo_timeout_exception(mock_logger, mock_subprocess, mock_remove_dir, mock_git_asset):
    operation = CLONE_OPERATION
    message = f'Git operation timed out archiving {mock_git_asset.name}.'
    GithubArchive().archive_repo(mock_thread_limiter(), mock_git_asset, 'mock/path', operation)

    mock_logger.error.assert_called_with(message)
    # TODO: This is difficult to mock because it must not exist and then later exist in the same function
    # mock_remove_dir.assert_called_once_with('mock/path')


@patch('shutil.rmtree')
@patch('subprocess.run', side_effect=subprocess.CalledProcessError(returncode=1, cmd=subprocess.run))
@patch('github_archive.archive.LOGGER')
def test_archive_repo_called_process_error(mock_logger, mock_subprocess, mock_remove_dir, mock_git_asset):
    operation = PULL_OPERATION
    GithubArchive().archive_repo(mock_thread_limiter(), mock_git_asset, 'github_archive', operation)

    mock_logger.error.assert_called()
    # TODO: This is difficult to mock because it must not exist and then later exist in the same function
    # mock_remove_dir.assert_called_once_with('mock/path')


@patch('subprocess.run')
@patch('github_archive.archive.LOGGER')
def test_archive_gist_success(mock_logger, mock_subprocess, mock_git_asset):
    # TODO: Mock the subprocess better to ensure it's doing what it should
    operation = CLONE_OPERATION
    message = f'Gist: {mock_git_asset.owner.login}/{mock_git_asset.id} {operation} success!'
    GithubArchive().archive_gist(mock_thread_limiter(), mock_git_asset, 'mock/path', operation)

    mock_subprocess.assert_called()
    mock_logger.info.assert_called_once_with(message)


@patch('os.path.exists', return_value=True)
@patch('subprocess.run')
@patch('github_archive.archive.LOGGER')
def test_archive_gist_clone_exists(mock_logger, mock_subprocess, mock_path_exists, mock_git_asset):
    operation = CLONE_OPERATION
    GithubArchive().archive_gist(mock_thread_limiter(), mock_git_asset, 'github_archive', operation)

    mock_subprocess.assert_not_called()


@patch('shutil.rmtree')
@patch('subprocess.run', side_effect=subprocess.TimeoutExpired(cmd=subprocess.run, timeout=0.1))
@patch('github_archive.archive.LOGGER')
def test_archive_gist_timeout_exception(mock_logger, mock_subprocess, mock_remove_dir, mock_git_asset):
    operation = CLONE_OPERATION
    message = f'Git operation timed out archiving {mock_git_asset.id}.'
    GithubArchive().archive_gist(mock_thread_limiter(), mock_git_asset, 'mock/path', operation)

    mock_logger.error.assert_called_with(message)
    # TODO: This is difficult to mock because it must not exist and then later exist in the same function
    # mock_remove_dir.assert_called_once_with('mock/path')


@patch('shutil.rmtree')
@patch('subprocess.run', side_effect=subprocess.CalledProcessError(returncode=1, cmd=subprocess.run))
@patch('github_archive.archive.LOGGER')
def test_archive_gist_called_process_error(mock_logger, mock_subprocess, mock_remove_dir, mock_git_asset):
    operation = PULL_OPERATION
    GithubArchive().archive_gist(mock_thread_limiter(), mock_git_asset, 'github_archive', operation)

    mock_logger.error.assert_called()
    # TODO: This is difficult to mock because it must not exist and then later exist in the same function
    # mock_remove_dir.assert_called_once_with('mock/path')
