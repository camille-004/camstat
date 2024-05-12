from dataclasses import dataclass, field
from typing import Any, Callable

from .strategy import (
    CPURetrievalStrategy,
    MemoryRetrievalStrategy,
    OSRetrievalStrategy,
)


@dataclass
class Entry:
    name: str
    display_name: str
    strategy: Callable[[], Any]
    _value: str = field(default="", init=False, repr=False)

    def update_value(self) -> None:
        self._value = self.strategy()

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, v: str) -> None:
        self._value = v


class EntryFactory:
    @staticmethod
    def create_entry(name: str, display_name: str) -> Entry:
        strategy_mapping: dict[str, Callable] = {
            "os": OSRetrievalStrategy.retrieve,
            "cpu_usage": CPURetrievalStrategy.retrieve,
            "memory_usage": MemoryRetrievalStrategy.retrieve,
        }
        strategy = strategy_mapping.get(name)
        if strategy is None:
            raise ValueError(f"No strategy defined for {name}.")
        return Entry(name=name, display_name=display_name, strategy=strategy)
