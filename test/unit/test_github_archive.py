import mock
import pytest
from githubarchive import github_archive


@mock.patch('githubarchive.github_archive.GITHUB_TOKEN', None)
@mock.patch('githubarchive.github_archive.LOGGER')
def test_github_archive_init_no_github_token(mock_logger):
    message = 'GITHUB_TOKEN must be present to run github-archive.'
    with pytest.raises(ValueError) as error:
        github_archive.GitHubArchive()
    assert mock_logger.critical.called_with(message)
    assert message == str(error.value)


@mock.patch('githubarchive.github_archive.GITHUB_TOKEN', '123')
@mock.patch('os.path.exists', return_value=False)
@mock.patch('os.makedirs')
def test_init_create_dirs(mock_make_dirs, mock_dir_exist):
    github_archive.GitHubArchive()
    assert mock_make_dirs.call_count == 3


@mock.patch('githubarchive.github_archive.GITHUB_TOKEN', '123')
@mock.patch('githubarchive.github_archive.LOGGER')
@mock.patch('githubarchive.github_archive.GitHubArchive.iterate_gists',
            return_value=True)
@mock.patch('githubarchive.github_archive.GitHubArchive.iterate_orgs',
            return_value=True)
@mock.patch('githubarchive.github_archive.GitHubArchive.iterate_repos',
            return_value=True)
def test_run_all_args_true(mock_iterate_repos, mock_iterate_orgs,
                           mock_iterate_gists, mock_logger):
    github_archive.GitHubArchive.run(
        user_clone=True,
        user_pull=True,
        orgs_clone=True,
        orgs_pull=True,
        gists_clone=True,
        gists_pull=True,
        branch='master'
    )
    assert mock_iterate_repos.call_count == 2
    assert mock_iterate_orgs.call_count == 2
    assert mock_iterate_gists.call_count == 2
    assert mock_logger.info.call_count == 9


@mock.patch('githubarchive.github_archive.GITHUB_TOKEN', '123')
@mock.patch('githubarchive.github_archive.LOGGER')
@mock.patch('githubarchive.github_archive.GitHubArchive.iterate_gists',
            return_value=True)
@mock.patch('githubarchive.github_archive.GitHubArchive.iterate_orgs',
            return_value=True)
@mock.patch('githubarchive.github_archive.GitHubArchive.iterate_repos',
            return_value=True)
def test_run_all_args_false(mock_iterate_repos, mock_iterate_orgs,
                            mock_iterate_gists, mock_logger):
    github_archive.GitHubArchive.run(
        user_clone=False,
        user_pull=False,
        orgs_clone=False,
        orgs_pull=False,
        gists_clone=False,
        gists_pull=False,
        branch='master'
    )
    assert not mock_iterate_repos.called
    assert not mock_iterate_orgs.called
    assert not mock_iterate_gists.called
    assert mock_logger.info.call_count == 9


@pytest.mark.skip('Working on mocking GitHub requests')
@mock.patch('githubarchive.github_archive.USER_REPOS', {"id": 1, "name": "repo_name", "full_name": "test_user/repo_name", "owner": {"id": 1, "name": "test_user"}})  # noqa
@mock.patch('githubarchive.github_archive.USER', '123')
def test_iterate_repos(mock_iterate_repos):
    iterate_repos = github_archive.GitHubArchive.iterate_repos(
        'clone', 'master')
    assert iterate_repos is True


# @mock.patch('githubarchive.github_archive.GitHubArchive.archive_repo',
#             return_values=('test_repo', 'master', 'test_path', 'clone'))
