from unittest.mock import patch

import pytest

from camstat.os_info import OSInfo, OSStrategy
from camstat.strategy import OSRetrievalStrategy


@pytest.fixture
def mock_os_info() -> OSInfo:
    return OSInfo(name="macOS", version="11.2", build="2OD64")


@patch("camstat.os_info.OSStrategy.get_os_info")
def test_retrieve_os_info(mock_get_os_info, mock_os_info) -> None:
    mock_get_os_info.return_value = mock_os_info
    expected = "macOS Version 11.2 (2OD64)"
    assert OSRetrievalStrategy.retrieve() == expected
