from unittest.mock import patch

import pytest

from github_archive import GithubArchive
from github_archive.archive import (
    CLONE_OPERATION,
    GIST_CONTEXT,
    ORG_CONTEXT,
    PULL_OPERATION,
    USER_CONTEXT,
)


@pytest.mark.parametrize(
    "args, patch_function",
    [
        (
            {
                "token": "123",
                "users": "justintime50",
                "view": True,
            },
            "github_archive.archive.view_repos",
        ),
        (
            {
                "token": "123",
                "users": "justintime50",
                "clone": True,
            },
            "github_archive.archive.iterate_repos_to_archive",
        ),
        (
            {
                "token": "123",
                "users": "justintime50",
                "pull": True,
            },
            "github_archive.archive.iterate_repos_to_archive",
        ),
    ],
)
@patch("github_archive.archive.Github.get_user")
@patch("github_archive.archive.GithubArchive.authenticated_user_in_users", return_value=True)
@patch("github_archive.archive.GithubArchive.get_all_git_assets")
def test_run_with_token(mock_get_all_git_assets, mock_authed_user_in_users, mock_get_user, args, patch_function):
    """Tests running the tool with different params when a token is specified."""
    github_archive = GithubArchive(**args)

    github_archive.authenticated_username = "justintime50"
    with patch(patch_function) as func:
        github_archive.run()

    mock_get_all_git_assets.assert_called_once()
    func.assert_called_once()
    assert github_archive.users == []  # Assert the authed user gets removed from list


@patch("github_archive.archive.view_repos")
@patch("github_archive.archive.GithubArchive.get_all_git_assets")
def test_run_users_view(mock_get_all_git_assets, mock_view_repos):
    github_archive = GithubArchive(
        users="justintime50",
        view=True,
    )

    github_archive.run()

    mock_get_all_git_assets.assert_called_once()
    mock_view_repos.assert_called_once()


@patch("github_archive.archive.iterate_repos_to_archive")
@patch("github_archive.archive.GithubArchive.get_all_git_assets")
def test_run_users_clone(mock_get_all_git_assets, mock_iterate_repos_to_archive):
    github_archive = GithubArchive(
        users="justintime50",
        clone=True,
    )

    github_archive.run()

    mock_get_all_git_assets.assert_called_once()
    mock_iterate_repos_to_archive.assert_called_once_with(github_archive, mock_get_all_git_assets(), CLONE_OPERATION)


@patch("github_archive.archive.iterate_repos_to_archive")
@patch("github_archive.archive.GithubArchive.get_all_git_assets")
def test_run_users_pull(mock_get_all_git_assets, mock_iterate_repos_to_archive):
    github_archive = GithubArchive(
        users="justintime50",
        pull=True,
    )

    github_archive.run()

    mock_get_all_git_assets.assert_called_once()
    mock_iterate_repos_to_archive.assert_called_once_with(github_archive, mock_get_all_git_assets(), PULL_OPERATION)


@patch("github_archive.archive.iterate_repos_to_fork")
@patch("github_archive.archive.GithubArchive.get_all_git_assets")
def test_run_users_fork(mock_get_all_git_assets, mock_iterate_repos_to_fork):
    github_archive = GithubArchive(
        users="justintime50",
        fork=True,
    )

    github_archive.run()

    mock_get_all_git_assets.assert_called_once()
    mock_iterate_repos_to_fork.assert_called_once()


@patch("github_archive.archive.view_repos")
@patch("github_archive.archive.GithubArchive.get_all_git_assets")
def test_run_orgs_view(mock_get_all_git_assets, mock_view_repos):
    github_archive = GithubArchive(
        orgs="org1",
        view=True,
    )

    github_archive.run()

    mock_get_all_git_assets.assert_called_once()
    mock_view_repos.assert_called_once()


@patch("github_archive.archive.iterate_repos_to_archive")
@patch("github_archive.archive.GithubArchive.get_all_git_assets")
def test_run_orgs_clone(mock_get_all_git_assets, mock_iterate_repos_to_archive):
    github_archive = GithubArchive(
        orgs="org1",
        clone=True,
    )

    github_archive.run()

    mock_get_all_git_assets.assert_called_once()
    mock_iterate_repos_to_archive.assert_called_once_with(github_archive, mock_get_all_git_assets(), CLONE_OPERATION)


@patch("github_archive.archive.iterate_repos_to_archive")
@patch("github_archive.archive.GithubArchive.get_all_git_assets")
def test_run_orgs_pull(mock_get_all_git_assets, mock_iterate_repos_to_archive):
    github_archive = GithubArchive(
        orgs="org1",
        pull=True,
    )

    github_archive.run()

    mock_get_all_git_assets.assert_called_once()
    mock_iterate_repos_to_archive.assert_called_once_with(github_archive, mock_get_all_git_assets(), PULL_OPERATION)


@patch("github_archive.archive.iterate_repos_to_fork")
@patch("github_archive.archive.GithubArchive.get_all_git_assets")
def test_run_orgs_fork(mock_get_all_git_assets, mock_iterate_repos_to_fork):
    github_archive = GithubArchive(
        orgs="org1",
        fork=True,
    )

    github_archive.run()

    mock_get_all_git_assets.assert_called_once()
    mock_iterate_repos_to_fork.assert_called_once()


@patch("github_archive.archive.view_gists")
@patch("github_archive.archive.GithubArchive.get_all_git_assets")
def test_run_gists_view(mock_get_all_git_assets, mock_view_gists):
    github_archive = GithubArchive(
        gists="justintime50",
        view=True,
    )

    github_archive.run()

    mock_get_all_git_assets.assert_called_once()
    mock_view_gists.assert_called_once()


@patch("github_archive.archive.iterate_gists_to_archive")
@patch("github_archive.archive.GithubArchive.get_all_git_assets")
def test_run_gists_clone(mock_get_all_git_assets, mock_iterate_gists_to_archive):
    github_archive = GithubArchive(
        gists="org1",
        clone=True,
    )

    github_archive.run()

    mock_get_all_git_assets.assert_called_once()
    mock_iterate_gists_to_archive.assert_called_once_with(github_archive, mock_get_all_git_assets(), CLONE_OPERATION)


@patch("github_archive.archive.iterate_gists_to_archive")
@patch("github_archive.archive.GithubArchive.get_all_git_assets")
def test_run_gists_pull(mock_get_all_git_assets, mock_iterate_gists_to_archive):
    github_archive = GithubArchive(
        gists="org1",
        pull=True,
    )

    github_archive.run()

    mock_get_all_git_assets.assert_called_once()
    mock_iterate_gists_to_archive.assert_called_once_with(github_archive, mock_get_all_git_assets(), PULL_OPERATION)


@patch("github_archive.archive.iterate_gists_to_fork")
@patch("github_archive.archive.GithubArchive.get_all_git_assets")
def test_run_gists_fork(mock_get_all_git_assets, mock_iterate_gists_to_fork):
    github_archive = GithubArchive(
        gists="org1",
        fork=True,
    )

    github_archive.run()

    mock_get_all_git_assets.assert_called_once()
    mock_iterate_gists_to_fork.assert_called_once()


@patch("github_archive.archive.view_repos")
@patch("github_archive.archive.GithubArchive.get_all_git_assets")
def test_run_stars_view(mock_get_all_git_assets, mock_view_repos):
    github_archive = GithubArchive(
        stars="justintime50",
        view=True,
    )

    github_archive.run()

    mock_get_all_git_assets.assert_called_once()
    mock_view_repos.assert_called_once()


@patch("github_archive.archive.iterate_repos_to_archive")
@patch("github_archive.archive.GithubArchive.get_all_git_assets")
def test_run_stars_clone(mock_get_all_git_assets, mock_iterate_repos_to_archive):
    github_archive = GithubArchive(
        stars="justintime50",
        clone=True,
    )

    github_archive.run()

    mock_get_all_git_assets.assert_called_once()
    mock_iterate_repos_to_archive.assert_called_once_with(github_archive, mock_get_all_git_assets(), CLONE_OPERATION)


@patch("github_archive.archive.iterate_repos_to_archive")
@patch("github_archive.archive.GithubArchive.get_all_git_assets")
def test_run_stars_pull(mock_get_all_git_assets, mock_iterate_repos_to_archive):
    github_archive = GithubArchive(
        stars="justintime50",
        pull=True,
    )

    github_archive.run()

    mock_get_all_git_assets.assert_called_once()
    mock_iterate_repos_to_archive.assert_called_once_with(github_archive, mock_get_all_git_assets(), PULL_OPERATION)


@patch("github_archive.archive.iterate_repos_to_fork")
@patch("github_archive.archive.GithubArchive.get_all_git_assets")
def test_run_stars_fork(mock_get_all_git_assets, mock_iterate_repos_to_fork):
    github_archive = GithubArchive(
        stars="justintime50",
        fork=True,
    )

    github_archive.run()

    mock_get_all_git_assets.assert_called_once()
    mock_iterate_repos_to_fork.assert_called_once()


@patch("github_archive.archive.setup_logger")
@patch("os.path.exists", return_value=False)
@patch("os.makedirs")
def test_initialize_project(mock_make_dirs, mock_dir_exist, mock_logger):
    github_archive = GithubArchive(
        users="justintime50",
        clone=True,
    )

    github_archive.initialize_project()

    mock_logger.assert_called_once_with(github_archive)
    assert mock_make_dirs.call_count == 2


@pytest.mark.parametrize(
    "args, expected_message",
    [
        ({"users": "justintime50"}, "A git operation must be specified when a list of users or orgs is provided."),
        ({"clone": True}, "A list must be provided when a git operation is specified."),
        ({}, "At least one git operation and one list must be provided to run github-archive."),
        (
            {"users": "justintime50", "clone": True, "include": "mock-repo", "exclude": "another-mock-repo"},
            "The include and exclude flags are mutually exclusive. Only one can be used on each run.",
        ),
        (
            {"users": "justintime50", "clone": True, "include": "mock-repo", "languages": "python"},
            "The include and exclude flags cannot be used with the languages flag.",
        ),
    ],
)
@patch("github_archive.archive.Github.get_user")
@patch("logging.Logger.critical")
def test_initialize_project_args(mock_logger, mock_get_user, args, expected_message):
    """Tests various alterations of CLI args and asserts that the error message matches the situation."""
    with pytest.raises(ValueError) as error:
        github_archive = GithubArchive(**args)
        github_archive.initialize_project()

    mock_logger.assert_called_with(expected_message)
    assert expected_message == str(error.value)


@patch("github_archive.archive.Github.get_user")
def test_authenticated_user_in_users(mock_get_user):
    github_archive = GithubArchive(
        token="123",
        users="unauthenticated_user",
    )

    authenticated_user_in_users = github_archive.authenticated_user_in_users()

    assert authenticated_user_in_users is False


@patch("github_archive.archive.Github.get_user")
def test_get_all_git_assets_repos(mock_get_user):
    github_archive = GithubArchive(
        users="justintime50",
    )

    github_archive.get_all_git_assets(USER_CONTEXT)

    mock_get_user.assert_called_once()


@patch("github_archive.archive.Github.get_user")
def test_get_all_git_assets_gists(mock_get_user):
    # TODO: This test doesn't yet do anything because we need to populate the `git_assets` list with mock data
    github_archive = GithubArchive(
        gists="justintime50",
    )

    github_archive.get_all_git_assets(GIST_CONTEXT)

    mock_get_user.assert_called_once()


@patch("github_archive.archive.Github")
@patch("github_archive.archive.Github.get_repos")
@patch("github_archive.archive.Github.get_user")
def test_get_all_user_repos(mock_get_user, mock_get_repos, mock_github_instance):
    users = "justintime50,user2"
    github_archive = GithubArchive(
        users=users,
    )

    github_archive.get_all_git_assets(USER_CONTEXT)

    mock_get_user.call_count == len(users)
    mock_get_repos.call_count == len(users)
    # TODO: Assert the list returned


@patch("github_archive.archive.Github")
@patch("github_archive.archive.Github.get_repos")
@patch("github_archive.archive.Github.get_organization")
def test_get_all_org_repos(mock_get_org, mock_get_repos, mock_github_instance):
    orgs = "org1,org2"
    github_archive = GithubArchive(
        orgs=orgs,
    )

    github_archive.get_all_git_assets(ORG_CONTEXT)

    mock_get_org.call_count == len(orgs)
    mock_get_repos.call_count == len(orgs)
    # TODO: Assert the list returned


@patch("github_archive.archive.Github")
@patch("github_archive.archive.Github.get_gists")
@patch("github_archive.archive.Github.get_user")
def test_get_all_gists(mock_get_user, mock_get_gists, mock_github_instance):
    gists = "justintime50,user2"
    github_archive = GithubArchive(
        gists=gists,
    )

    github_archive.get_all_git_assets(GIST_CONTEXT)

    mock_get_user.call_count == len(gists)
    mock_get_gists.call_count == len(gists)
    # TODO: Assert the list returned


@patch("os.path.exists", return_value=True)
@patch("shutil.rmtree")
@patch("logging.Logger.debug")
def test_remove_failed_dirs(mock_logger, mock_remove_dir, mock_path_exists):
    """Tests that we remove failed dirs correctly."""
    github_archive = GithubArchive()

    github_archive.remove_failed_dirs("mock/path", ["mock_dir"])

    mock_logger.assert_called_once()
    mock_remove_dir.assert_called_once()


@patch("os.path.exists", return_value=True)
@patch("os.chmod")
@patch("logging.Logger.debug")
def test_remove_failed_dirs_on_error(mock_logger, mock_chmod, mock_path_exists):
    """Tests that we remove failed dirs correctly when there's an error such as read-only `.git` folders on Windows."""
    with pytest.raises(OSError):
        github_archive = GithubArchive()

        github_archive.remove_failed_dirs("mock/path", ["mock_dir"])

    mock_logger.assert_called_once()
    mock_chmod.assert_called_once()
