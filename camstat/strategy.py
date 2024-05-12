"""Define retrieval strategies for entries in the display."""

from functools import lru_cache

from .os_info import OSInfo, OSStrategy


class OSRetrievalStrategy:
    """Provide a strategy for retrieving the operating system type."""

    @staticmethod
    @lru_cache(maxsize=1)
    def retrieve() -> str:
        """Retrieve the OS type.

        This is cached to avoid repeated system calls for the same
        information.

        Returns
        -------
        str
            The name of the operating system.
        """
        os_info: OSInfo = OSStrategy.get_os_info()
        return f"{os_info.name} Version {os_info.version} ({os_info.build})"
