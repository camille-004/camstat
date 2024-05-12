"""Module for retrieving operating system information."""

import platform
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from typing import Callable

from .util import Util


class OSType(Enum):
    """Enum for Operating System types."""

    macOS = "Darwin"
    Windows = "Windows"
    Linux = "Linux"
    Unknown = "Unknown"


@dataclass
class OSInfo:
    """Data class to store basic OS information."""

    name: str
    version: str
    build: str | None = None


def get_macos_marketing_name() -> str:
    """Fetch the marketing name for macOS using system files.

    Returns
    -------
    str
        The marketing name extracted from the macOS software license agreement.
    """
    command = """
    awk '/SOFTWARE LICENSE AGREEMENT FOR macOS/' '/System/Library/CoreServices/Setup Assistant.app/Contents/Resources/en.lproj/OSXSoftwareLicense.rtf' | awk -F 'macOS ' '{print $NF}' | awk '{print substr($0, 0, length($0)-1)}'  # noqa
    """
    return Util.run_command(command)


class OSCommand:
    """Manage the retrieval of OS information based on OS type."""

    commands: dict[OSType, Callable[[], OSInfo]] = {
        OSType.macOS: lambda: OSInfo(
            name=f"{Util.run_command('sw_vers -productName')} "
            f"{get_macos_marketing_name()}",
            version=Util.run_command("sw_vers -productVersion"),
            build=Util.run_command("sw_vers -buildVersion"),
        ),
        OSType.Windows: lambda: OSInfo(
            name=Util.run_command("systeminfo"), version=""
        ),
        OSType.Linux: lambda: OSInfo(
            name=Util.run_command("uname -a"), version=""
        ),
    }

    @staticmethod
    def get_command(os_type: OSType) -> Callable[[], OSInfo]:
        """Retrieve the command function based on the OS type.

        Parameters
        ----------
        os_type : OSType
            The type of the operating system.

        Returns
        -------
        Callable[[], OSInfo]
            A callable that returns OSInfo with detailed OS information.
        """
        return OSCommand.commands.get(
            os_type, lambda: OSInfo(name="Unsupported OS", version="")
        )


class OSStrategy:
    """Strategy class to fetch OS information using a caching mechanism."""

    @staticmethod
    @lru_cache(maxsize=4)
    def get_os_info() -> OSInfo:
        """Retrieve OS information based on the system type.

        Uses a caching mechanism to minimize redundant retrievals.

        Returns
        -------
        OSInfo
            An instance of OSInfo containing details about the OS.
        """
        system_type = OSType(platform.system())
        return OSCommand.get_command(system_type)()
