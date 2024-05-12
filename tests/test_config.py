from typing import Any
from unittest.mock import mock_open, patch

import pytest

from camstat.config import Config


@pytest.fixture
def config_data() -> dict[str, Any]:
    return {
        "fields": [{"name": "os", "displayName": "Operating System"}],
        "display": {"format": "CONSOLE"},
    }


@patch("builtins.open", new_callable=mock_open)
@patch("camstat.config.toml.load")
@patch("pathlib.Path.exists", return_value=True)
def test_load_config(
    mock_exists, mock_toml_load, mock_file, config_data
) -> None:
    mock_toml_load.return_value = config_data
    config = Config()
    config.load_config("path/to/config.toml")
    assert config.get_output_config().format == "CONSOLE"
    assert len(config.get_entries()) == 1


@patch("builtins.open", new_callable=mock_open, read_data="")
def test_load_config_file_not_found(mock_file: str) -> None:
    config = Config()
    with pytest.raises(FileNotFoundError):
        config.load_config("path/does/not/exist.toml")
