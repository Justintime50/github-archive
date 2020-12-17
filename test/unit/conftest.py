import pytest
import mock


@pytest.fixture
def mock_object():
    """This can be used for repos and/or gists
    """
    mock_object = mock.MagicMock()
    mock_object.id = '123'
    mock_object.name = 'Mock Name'
    mock_object.owner.name = 'Mock Name'
    return mock_object
