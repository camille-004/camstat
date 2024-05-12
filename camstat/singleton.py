"""Define the Singleton metaclass."""

from typing import Any


class SingletonMeta(type):
    """A metaclass that creates a singleton instance for a class.

    Ensures that only one instance of a class is created throughout the
    lifetime of the app. Any subsequent attempts to create an instance of the
    singleton class will return the same instance.
    """

    _instances: dict[type, "SingletonMeta"] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> "SingletonMeta":
        """Return the singleton instance of the class.

        Create a new one if the instance does not exist.

        Returns
        -------
        SingletonMeta
            The singleton instance of the class.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
