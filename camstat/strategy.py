"""Define retrieval strategies for entries in the display."""

import platform
from functools import lru_cache

import psutil


class OSRetrievalStrategy:
    """Provide a strategy for retrieving the operating system type."""

    @staticmethod
    @lru_cache(maxsize=1)
    def retrieve() -> str:
        """Retrieve the OS type using the `platform` module.

        This is cached to avoid repeated system calls for the same
        information.

        Returns
        -------
        str
            The name of the operating system.
        """
        return platform.system()


class CPURetrievalStrategy:
    """Provide a strategy for retrieving the current CPU usage percentage."""

    @staticmethod
    def retrieve() -> str:
        """Retrieve the current CPU usage percentage using `psutil`.

        This measures CPU usage over a one-second interval.

        Returns
        -------
        str
            The CPU usage percentage formatted as a string with a percent
            sign.
        """
        return f"{psutil.cpu_percent(interval=1)}%"


class MemoryRetrievalStrategy:
    """Provide a strategy for retrieving the current memory usage."""

    @staticmethod
    def retrieve() -> str:
        """Retrieve the current memory usage using `psutil`.

        This accesses the virtual memory stats and returns the percentage of
        memory used.

        Returns
        -------
        str
            The memory usage percentage formatted as a string with a percent
            sign.
        """
        return f"{psutil.virtual_memory().percent}%"
