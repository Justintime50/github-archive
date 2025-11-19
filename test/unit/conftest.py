from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_git_asset():
    """This can be used for repos and/or gists, it contains shared data
    for either git asset for easier testing.
    """
    mock_git_asset = MagicMock()
    mock_git_asset.id = "123"
    mock_git_asset.name = "mock-asset-name"
    mock_git_asset.owner.name = "Mock User Name"
    mock_git_asset.owner.login = "mock_username"
    mock_git_asset.html_url = "mock/html_url"
    mock_git_asset.ssh_url = "mock/ssh_url"
    mock_git_asset.language = "Python"

    return mock_git_asset
