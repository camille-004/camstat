from typing import Any


class SingletonMeta(type):
    _instances: dict[type, "SingletonMeta"] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> "SingletonMeta":
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
