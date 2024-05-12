import platform
from functools import lru_cache

import psutil


class OSRetrievalStrategy:
    @staticmethod
    @lru_cache(maxsize=1)
    def retrieve() -> str:
        return platform.system()


class CPURetrievalStrategy:
    @staticmethod
    def retrieve() -> str:
        return f"{psutil.cpu_percent(interval=1)}%"


class MemoryRetrievalStrategy:
    @staticmethod
    def retrieve() -> str:
        return f"{psutil.virtual_memory().percent}%"
