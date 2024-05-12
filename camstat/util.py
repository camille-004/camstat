"""Utility module."""

from subprocess import check_output


class Util:
    """Utility class."""

    @staticmethod
    def run_command(command: list[str] | str) -> str:
        """Execute a shell command and return its output.

        Parameters
        ----------
        command : list[str] | str
            The command to execute.

        Returns
        -------
        str
            The output from the command as a string.
        """
        return check_output(command, shell=True, text=True).strip()
