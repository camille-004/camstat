from unittest.mock import patch

import pytest

from camstat.util import Util


@patch("subprocess.check_output")
def test_run_command(mock_check_output: str) -> None:
    mock_check_output.return_value = b"test\n"
    assert Util.run_command("echo test") == "test"


@patch("subprocess.check_output")
def test_run_command_failure(mock_check_output: str) -> None:
    mock_check_output.side_effect = Exception("error")
    with pytest.raises(Exception):
        Util.run_command("invalid command")
