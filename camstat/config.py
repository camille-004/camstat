from pathlib import Path

import toml
from pydantic import BaseModel, Field, TypeAdapter

from .entry import Entry, EntryFactory
from .singleton import SingletonMeta


class FieldConfig(BaseModel):
    name: str
    display_name: str = Field(..., alias="displayName")


class OutputConfig(BaseModel):
    format: str
    file_path: str | None = None


class AppConfig(BaseModel):
    fields: list[FieldConfig]
    display: OutputConfig


class Config(metaclass=SingletonMeta):
    _entries: list[Entry] = []
    display_config: OutputConfig | None = None

    def load_config(self, file_path: str) -> None:
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
        return self._entries

    def get_display_config(self) -> OutputConfig | None:
        return self.display_config
