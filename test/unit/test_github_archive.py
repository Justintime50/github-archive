import mock
import pytest
from githubarchive import github_archive


@mock.patch('githubarchive.github_archive.GITHUB_TOKEN', None)
def test_github_archive_init_no_github_token():
    message = 'Error: GitHub GITHUB_TOKEN must be present to run github-archive.'  # noqa
    with pytest.raises(SystemExit) as error:
        github_archive.GitHubArchive()
    assert message in str(error.value)


@pytest.mark.skip('Need to mock logger')
@mock.patch('githubarchive.github_archive.LOGGER', 'logging.getLogger(__name__)')  # noqa
def test_github_archive_init_logger():
    github_archive.GitHubArchive()
