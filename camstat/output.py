"""Handle the output location and format of camstat."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from .config import Config, OutputConfig
from .entry import Entry


def format_entries(entries: list[Entry]) -> str:
    """Format a list of Entry objects into a single string.

    Parameters
    ----------
    entries : list[Entry]
        A list of Entry objects to format.

    Returns
    -------
    str
        A formatted string representing the display name and value of each
        entry.
    """
    return "\n".join(
        f"{entry.display_name}: {entry.value}" for entry in entries
    )


class OutputFormat(Enum):
    """Enumeration for output formats."""

    CONSOLE = "CONSOLE"
    FILE = "FILE"


class OutputStrategy(ABC):
    """Abstract base class for output strategies."""

    @abstractmethod
    def output(self, data: str) -> None:
        """Output the given data.

        Parameters
        ----------
        data : str
            The data to output.
        """
        pass


class ConsoleOutput(OutputStrategy):
    """Concrete implementation of OutputStrategy to output to the console."""

    def output(self, data: str) -> None:
        """Output the given data to the console.

        Parameters
        ----------
        data : str
            The data to output.
        """
        print(data)


class FileOutput(OutputStrategy):
    """Concrete implementation of OutputStrategy to output to a file."""

    def __init__(self, file_path: str):
        """Initialize the FileOutput with a specific file path.

        Parameters
        ----------
        file_path : str
            The path to the file where data will be written.
        """
        self.file_path = file_path

    def output(self, data: str) -> None:
        """Write the given data to a file specified by file_path.

        Parameters
        ----------
        data : str
            The data to output.
        """
        with open(self.file_path, "w") as file:
            file.write(data)


@dataclass
class Output:
    """Handle the output of data using a specified strategy."""

    strategy: OutputStrategy

    def output(self, data: str) -> None:
        """Output data using the configured output strategy.

        Parameters
        ----------
        data : str
            The data to output.
        """
        self.strategy.output(data)


def get_output_strategy(
    format: str, file_path: str | None = None
) -> OutputStrategy:
    """Determine the appropriate output strategy based on the format.

    Parameters
    ----------
    format : str
        The output format.
    file_path : str | None, optional
        The file path for file output, if applicable.

    Returns
    -------
    OutputStrategy
        The output strategy corresponding to the given format.

    Raises
    ------
    ValueError
        If the file path is required but not provided.
    ValueError
        If the format is unsupported.
    """
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
    """Configure the output based on the provided output configuration.

    Parameters
    ----------
    output_config : OutputConfig | None
        The output configuration settings.

    Returns
    -------
    Output
        The configured output handler.
    """
    assert output_config is not None
    strategy = get_output_strategy(
        output_config.format, output_config.file_path
    )
    return Output(strategy=strategy)


def output(config: Config) -> None:
    """Handle the output process for entries in the configuration.

    Parameters
    ----------
    config : Config
        The application configuration containing entries and output
        settings.
    """
    entries = config.get_entries()
    output_config = config.get_output_config()
    output = configure_output(output_config)

    for entry in entries:
        entry.update_value()

    data = format_entries(entries)
    output.output(data)
