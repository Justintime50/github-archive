import mock
import argparse
from githubarchive import github_archive


@mock.patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(
                test='test'
                )
            )
def test_cli(mock_args):
    # TODO: Mock this better to actually test args are being passed
    github_archive.GitHubArchiveCLI()


def test_generate_log():
    """Test generating a log and reading its contents
    """
    content = 'Test log content'
    mock_open = mock.mock_open(read_data=content)
    with mock.patch('builtins.open', mock_open):
        result = github_archive.GitHubArchive.generate_log('test.log')
    assert content in result
