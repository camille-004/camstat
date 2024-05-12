from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from .config import Config, OutputConfig
from .entry import Entry


def format_entries(entries: list[Entry]) -> str:
    return "\n".join(
        f"{entry.display_name}: {entry.value}" for entry in entries
    )


class OutputFormat(Enum):
    CONSOLE = "CONSOLE"
    FILE = "FILE"


class OutputStrategy(ABC):
    @abstractmethod
    def output(self, data: str) -> None:
        pass


class ConsoleOutput(OutputStrategy):
    def output(self, data: str) -> None:
        print(data)


class FileOutput(OutputStrategy):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def output(self, data: str) -> None:
        with open(self.file_path, "w") as file:
            file.write(data)


@dataclass
class Output:
    strategy: OutputStrategy

    def output(self, data: str) -> None:
        self.strategy.output(data)


def get_output_strategy(
    format: str, file_path: str | None = None
) -> OutputStrategy:
    format_str = OutputFormat[format.upper()]
    match format_str:
        case OutputFormat.CONSOLE:
            return ConsoleOutput()
        case OutputFormat.FILE:
            if file_path is None:
                raise ValueError("File path must be provided for file output.")
            return FileOutput(file_path)
        case _:
            raise ValueError("Unsupported display format.")


def configure_output(output_config: OutputConfig | None) -> Output:
    assert output_config is not None
    strategy = get_output_strategy(
        output_config.format, output_config.file_path
    )
    return Output(strategy=strategy)


def output(config: Config) -> None:
    entries = config.get_entries()
    output_config = config.get_display_config()
    output = configure_output(output_config)

    for entry in entries:
        entry.update_value()

    data = format_entries(entries)
    output.output(data)
