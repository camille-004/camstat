"""camstat configurations."""

from pathlib import Path

import toml
from pydantic import BaseModel, Field, TypeAdapter

from .entry import Entry, EntryFactory
from .singleton import SingletonMeta


class FieldConfig(BaseModel):
    """Configuration for individual fields within the display."""

    name: str
    display_name: str = Field(..., alias="displayName")


class OutputConfig(BaseModel):
    """Configuration for the output format and file path settings."""

    format: str
    file_path: str | None = None


class AppConfig(BaseModel):
    """Application configuration.

    Holds all settings related to field and output configs.
    """

    fields: list[FieldConfig]
    display: OutputConfig


class Config(metaclass=SingletonMeta):
    """Singleton configuration manager for the display.

    Ensures a single instance of the configuration.
    """

    _entries: list[Entry] = []
    display_config: OutputConfig | None = None

    def load_config(self, file_path: str) -> None:
        """
        Load the configuration from a TOML file and initializes settings.

        Parameters
        ----------
        file_path : str
            The path to the configuration file.

        Raises
        ------
        FileNotFoundError
            If the specified file does not exist.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"No configuration file found at {path}.")

        config_data = toml.load(path)
        app_config = TypeAdapter(AppConfig).validate_python(config_data)
        self._entries = [
            EntryFactory.create_entry(field.name, field.display_name)
            for field in app_config.fields
        ]
        self.display_config = app_config.display

    def get_entries(self) -> list[Entry]:
        """Retrieve the list of Entry objects.

        Returns
        -------
        list[Entry]
            A list of Entry objects.
        """
        return self._entries

    def get_output_config(self) -> OutputConfig | None:
        """Retrieve the output configuration.

        Returns
        -------
        OutputConfig | None
            The current display configuration, if set.
        """
        return self.display_config
