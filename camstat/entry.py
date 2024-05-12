"""Define the Entry class and EntryFactory."""

from dataclasses import dataclass, field
from typing import Any, Callable

from .strategy import OSRetrievalStrategy


@dataclass
class Entry:
    """Represent a single data entry in the display.

    Encapsulates the retrieval strategy and value.
    """

    name: str
    display_name: str
    strategy: Callable[[], Any]
    _value: str = field(default="", init=False, repr=False)

    def update_value(self) -> None:
        """Execute the strategy assigned to this entry and update the value."""
        self._value = self.strategy()

    @property
    def value(self) -> str:
        """Get the current value of the entry.

        Returns
        -------
        str
            The current value of the entry.
        """
        return self._value

    @value.setter
    def value(self, v: str) -> None:
        """Set the value of the entry.

        Parameters
        ----------
        v : str
            The new value to be set for the entry.
        """
        self._value = v


class EntryFactory:
    """Entry factory.

    Factory class for creating Entry objects based on a predefined strategy
    mapping.
    """

    @staticmethod
    def create_entry(name: str, display_name: str) -> Entry:
        """Create an entry through the EntryFactory.

        The retrieval will use a strategy determined by the entry's name.

        Parameters
        ----------
        name : str
            The name of the entry, which determines the retrieval
            strategy.
        display_name : str
            The human-readable name for the entry.

        Returns
        -------
        Entry
            A new Entry object configured with the appropriate retrieval
            strategy.

        Raises
        ------
        ValueError
            If no strategyis defined for the given name.
        """
        strategy_mapping: dict[str, Callable[[], str]] = {
            "os": OSRetrievalStrategy.retrieve,
        }
        strategy = strategy_mapping.get(name)
        if strategy is None:
            raise ValueError(f"No strategy defined for {name}.")
        return Entry(name=name, display_name=display_name, strategy=strategy)
