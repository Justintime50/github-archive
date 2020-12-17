import mock
import pytest
import subprocess
from github_archive import GithubArchive


GITHUB_TOKEN = '123'
ORG_NAME = 'my_org'


@mock.patch('github_archive.archive.GITHUB_TOKEN', None)
@mock.patch('github_archive.archive.LOGGER')
def test_initialize_project_no_github_token(mock_logger):
    message = 'GITHUB_TOKEN must be present to run github-archive.'
    with pytest.raises(ValueError) as error:
        GithubArchive.initialize_project()
    assert mock_logger.critical.called_with(message)
    assert message == str(error.value)


@mock.patch('github_archive.archive.GITHUB_TOKEN', GITHUB_TOKEN)
@mock.patch('os.path.exists', return_value=False)
@mock.patch('os.makedirs')
def test_initialize_project(mock_make_dirs, mock_dir_exist):
    GithubArchive.initialize_project()
    assert mock_make_dirs.call_count == 2


@mock.patch('github_archive.archive.GITHUB_TOKEN', GITHUB_TOKEN)
@mock.patch('github_archive.archive.GithubArchive.get_repos')
@mock.patch('github_archive.archive.GithubArchive.iterate_gists')
@mock.patch('github_archive.archive.GithubArchive.iterate_repos')
@mock.patch('github_archive.archive.LOGGER')
def test_run_user_clone_true(mock_logger, mock_iterate_repos, mock_iterate_gists, mock_get_repos):
    GithubArchive.run(
        user_clone=True,
        user_pull=False,
        orgs_clone=False,
        orgs_pull=False,
        gists_clone=False,
        gists_pull=False,
    )
    mock_get_repos.assert_called_once()
    mock_iterate_repos.assert_called_once()
    mock_iterate_gists.assert_not_called()
    mock_logger.info.call_count == 3


@mock.patch('github_archive.archive.GITHUB_TOKEN', GITHUB_TOKEN)
@mock.patch('github_archive.archive.GithubArchive.get_repos')
@mock.patch('github_archive.archive.GithubArchive.iterate_gists')
@mock.patch('github_archive.archive.GithubArchive.iterate_repos')
@mock.patch('github_archive.archive.LOGGER')
def test_run_user_pull_true(mock_logger, mock_iterate_repos, mock_iterate_gists, mock_get_repos):
    GithubArchive.run(
        user_clone=False,
        user_pull=True,
        orgs_clone=False,
        orgs_pull=False,
        gists_clone=False,
        gists_pull=False,
    )
    mock_get_repos.assert_called_once()
    mock_iterate_repos.assert_called_once()
    mock_iterate_gists.assert_not_called()
    mock_logger.info.call_count == 3


@mock.patch('github_archive.archive.ORG_LIST', ORG_NAME)
@mock.patch('github_archive.archive.GITHUB_TOKEN', GITHUB_TOKEN)
@mock.patch('github_archive.archive.GithubArchive.get_all_org_repos')
@mock.patch('github_archive.archive.GithubArchive.iterate_gists')
@mock.patch('github_archive.archive.GithubArchive.determine_repo_context')
@mock.patch('github_archive.archive.LOGGER')
def test_run_orgs_clone_true(mock_logger, mock_determine_repo_context, mock_iterate_gists, mock_get_all_org_repos):
    GithubArchive.run(
        user_clone=False,
        user_pull=False,
        orgs_clone=True,
        orgs_pull=False,
        gists_clone=False,
        gists_pull=False,
    )
    mock_get_all_org_repos.assert_called_once()
    mock_determine_repo_context.assert_called_once()
    mock_iterate_gists.assert_not_called()
    mock_logger.info.call_count == 3


@mock.patch('github_archive.archive.ORG_LIST', ORG_NAME)
@mock.patch('github_archive.archive.GITHUB_TOKEN', GITHUB_TOKEN)
@mock.patch('github_archive.archive.GithubArchive.get_all_org_repos')
@mock.patch('github_archive.archive.GithubArchive.iterate_gists')
@mock.patch('github_archive.archive.GithubArchive.determine_repo_context')
@mock.patch('github_archive.archive.LOGGER')
def test_run_orgs_pull_true(mock_logger, mock_determine_repo_context, mock_iterate_gists, mock_get_all_org_repos):
    GithubArchive.run(
        user_clone=False,
        user_pull=False,
        orgs_clone=False,
        orgs_pull=True,
        gists_clone=False,
        gists_pull=False,
    )
    mock_get_all_org_repos.assert_called_once()
    mock_determine_repo_context.assert_called_once()
    mock_iterate_gists.assert_not_called()
    mock_logger.info.call_count == 3


@mock.patch('github_archive.archive.ORG_LIST', ORG_NAME)
@mock.patch('github_archive.archive.GITHUB_TOKEN', GITHUB_TOKEN)
@mock.patch('github_archive.archive.GithubArchive.get_all_org_repos')
@mock.patch('github_archive.archive.GithubArchive.iterate_gists')
@mock.patch('github_archive.archive.GithubArchive.iterate_repos')
@mock.patch('github_archive.archive.LOGGER')
def test_run_orgs_list_without_flag(mock_logger, mock_iterate_repos, mock_iterate_gists, mock_get_all_org_repos):
    GithubArchive.run(
        user_clone=False,
        user_pull=False,
        orgs_clone=False,
        orgs_pull=False,
        gists_clone=False,
        gists_pull=False,
    )
    mock_get_all_org_repos.assert_not_called()
    mock_iterate_repos.assert_not_called()
    mock_iterate_gists.assert_not_called()
    mock_logger.info.call_count == 3


@mock.patch('github_archive.archive.GITHUB_TOKEN', GITHUB_TOKEN)
@mock.patch('github_archive.archive.GithubArchive.get_gists')
@mock.patch('github_archive.archive.GithubArchive.iterate_gists')
@mock.patch('github_archive.archive.GithubArchive.iterate_repos')
@mock.patch('github_archive.archive.LOGGER')
def test_run_gists_clone_true(mock_logger, mock_iterate_repos, mock_iterate_gists, mock_get_gists):
    GithubArchive.run(
        user_clone=False,
        user_pull=False,
        orgs_clone=False,
        orgs_pull=False,
        gists_clone=True,
        gists_pull=False,
    )
    mock_get_gists.assert_called_once()
    mock_iterate_repos.assert_not_called()
    mock_iterate_gists.assert_called_once()
    mock_logger.info.call_count == 3


@mock.patch('github_archive.archive.GITHUB_TOKEN', GITHUB_TOKEN)
@mock.patch('github_archive.archive.GithubArchive.get_gists')
@mock.patch('github_archive.archive.GithubArchive.iterate_gists')
@mock.patch('github_archive.archive.GithubArchive.iterate_repos')
@mock.patch('github_archive.archive.LOGGER')
def test_run_gists_pull_true(mock_logger, mock_iterate_repos, mock_iterate_gists, mock_get_gists):
    GithubArchive.run(
        user_clone=False,
        user_pull=False,
        orgs_clone=False,
        orgs_pull=False,
        gists_clone=False,
        gists_pull=True,
    )
    mock_get_gists.assert_called_once()
    mock_iterate_repos.assert_not_called()
    mock_iterate_gists.assert_called_once()
    mock_logger.info.call_count == 3


@mock.patch('github_archive.archive.USER.get_repos')
def test_get_repos(mock_get_repos):
    GithubArchive.get_repos()
    mock_get_repos.assert_called_once()


@mock.patch('github_archive.archive.GITHUB_TOKEN', GITHUB_TOKEN)
@mock.patch('github_archive.archive.Github.get_organization')
def test_get_all_org_repos(mock_get_organization):
    GithubArchive.get_all_org_repos()
    mock_get_organization.assert_called_once()


@mock.patch('github_archive.archive.USER.get_gists')
def test_get_gists(mock_get_gists):
    GithubArchive.get_gists()
    mock_get_gists.assert_called_once()


@pytest.mark.parametrize('context', [('orgs'), ('user')])
@mock.patch('github_archive.archive.GithubArchive.iterate_repos')
def test_determine_repo_context_orgs(mock_iterate_repos, context, mock_object):
    repos = [mock_object]
    GithubArchive.determine_repo_context(repos, context, 'clone')
    mock_iterate_repos.assert_called_once()


@mock.patch('github_archive.archive.GithubArchive.iterate_repos')
@mock.patch('github_archive.archive.LOGGER')
def test_determine_repo_context_bad_param(mock_logger, mock_determine_repo_context, mock_object):
    repos = [mock_object]
    context = 'bad-param'
    message = f'Could not determine what action to take with {context}.'
    with pytest.raises(ValueError):
        GithubArchive.determine_repo_context(repos, context, 'clone')
    mock_determine_repo_context.assert_not_called()
    mock_logger.error.assert_called_once_with(message)


@mock.patch('github_archive.archive.GithubArchive.archive_repo')
@mock.patch('github_archive.archive.USER')
def test_iterate_repos_matching_owner_name(mock_user, mock_archive_repo, mock_object):
    mock_user.name = 'Mock Name'
    repos = [mock_object]
    GithubArchive.iterate_repos(repos, 'user', 'clone')
    mock_archive_repo.assert_called()


@mock.patch('github_archive.archive.GithubArchive.archive_repo')
@mock.patch('github_archive.archive.USER')
def test_iterate_repos_not_matching_owner_name(mock_user, mock_archive_repo, mock_object):
    mock_user.name = 'Mock Name Does Not Match'
    repos = [mock_object]
    GithubArchive.iterate_repos(repos, 'user', 'clone')
    mock_archive_repo.assert_not_called()


@mock.patch('github_archive.archive.GithubArchive.archive_repo')
@mock.patch('github_archive.archive.USER')
def test_iterate_org_repos_success(mock_user, mock_archive_repo, mock_object):
    mock_user.name = 'Mock Name'
    repos = [mock_object]
    GithubArchive.iterate_repos(repos, 'orgs', 'clone')
    mock_archive_repo.assert_called()


@mock.patch('github_archive.archive.GithubArchive.archive_gist')
@mock.patch('github_archive.archive.USER')
def test_iterate_gists_success(mock_user, mock_archive_gist, mock_object):
    gists = [mock_object]
    GithubArchive.iterate_gists(gists, 'clone')
    mock_archive_gist.assert_called()


@mock.patch('subprocess.run')
@mock.patch('github_archive.archive.LOGGER')
def test_archive_repo_success(mock_logger, mock_subprocess, mock_object):
    operation = 'clone'
    message = f'Repo: {mock_object.name} {operation} success!'
    GithubArchive.archive_repo(mock_object, 'mock/path', operation)
    mock_logger.info.assert_called_once_with(message)


@mock.patch('os.path.exists', return_value=True)
@mock.patch('subprocess.run')
@mock.patch('github_archive.archive.LOGGER')
def test_archive_repo_clone_exists(mock_logger, mock_subprocess, mock_path_exists, mock_object):
    operation = 'clone'
    message = f'Repo: {mock_object.name} already cloned, skipping clone operation.'
    GithubArchive.archive_repo(mock_object, 'mock/path', operation)
    mock_logger.info.assert_called_once_with(message)


@mock.patch('subprocess.run', side_effect=subprocess.TimeoutExpired(cmd=subprocess.run, timeout=0.1))
@mock.patch('github_archive.archive.LOGGER')
def test_archive_repo_timeout_exception(mock_logger, mock_subprocess, mock_object):
    operation = 'clone'
    message = f'Git operation timed out archiving {mock_object.name}.'
    GithubArchive.archive_repo(mock_object, 'mock/path', operation)
    mock_logger.error.assert_called_with(message)


@mock.patch('subprocess.run', side_effect=subprocess.CalledProcessError(returncode=1, cmd=subprocess.run))
@mock.patch('github_archive.archive.LOGGER')
def test_archive_repo_called_process_error(mock_logger, mock_subprocess, mock_object):
    operation = 'pull'
    GithubArchive.archive_repo(mock_object, 'mock/path', operation)
    mock_logger.error.assert_called()


@mock.patch('subprocess.run')
@mock.patch('github_archive.archive.LOGGER')
def test_archive_repo_bad_param(mock_logger, mock_subprocess, mock_object):
    operation = 'bad-param'
    message = f'Could not determine what action to take with {mock_object.name} based on {operation}.'
    with pytest.raises(ValueError):
        GithubArchive.archive_repo(mock_object, 'mock/path', operation)
    mock_logger.error.assert_called_once_with(message)


@mock.patch('subprocess.run')
@mock.patch('github_archive.archive.LOGGER')
def test_archive_gist_success(mock_logger, mock_subprocess, mock_object):
    operation = 'clone'
    message = f'Gist: {mock_object.id} {operation} success!'
    GithubArchive.archive_gist(mock_object, 'mock/path', operation)
    mock_logger.info.assert_called_once_with(message)


@mock.patch('os.path.exists', return_value=True)
@mock.patch('subprocess.run')
@mock.patch('github_archive.archive.LOGGER')
def test_archive_gist_clone_exists(mock_logger, mock_subprocess, mock_path_exists, mock_object):
    operation = 'clone'
    message = f'Gist: {mock_object.id} already cloned, skipping clone operation.'
    GithubArchive.archive_gist(mock_object, 'mock/path', operation)
    mock_logger.info.assert_called_once_with(message)


@mock.patch('subprocess.run', side_effect=subprocess.TimeoutExpired(cmd=subprocess.run, timeout=0.1))
@mock.patch('github_archive.archive.LOGGER')
def test_archive_gist_timeout_exception(mock_logger, mock_subprocess, mock_object):
    operation = 'clone'
    message = f'Git operation timed out archiving {mock_object.id}.'
    GithubArchive.archive_gist(mock_object, 'mock/path', operation)
    mock_logger.error.assert_called_with(message)


@mock.patch('subprocess.run', side_effect=subprocess.CalledProcessError(returncode=1, cmd=subprocess.run))
@mock.patch('github_archive.archive.LOGGER')
def test_archive_gist_called_process_error(mock_logger, mock_subprocess, mock_object):
    operation = 'pull'
    GithubArchive.archive_gist(mock_object, 'mock/path', operation)
    mock_logger.error.assert_called()


@mock.patch('subprocess.run')
@mock.patch('github_archive.archive.LOGGER')
def test_archive_gist_bad_param(mock_logger, mock_subprocess, mock_object):
    operation = 'bad-param'
    message = f'Could not determine what action to take with {mock_object.id} based on {operation}.'
    with pytest.raises(ValueError):
        GithubArchive.archive_gist(mock_object, 'mock/path', operation)
    mock_logger.error.assert_called_once_with(message)
