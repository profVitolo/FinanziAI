from threading import Lock
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


class AdvisorBusyError(RuntimeError):
    pass


class AdvisorExecutor:
    def __init__(self):
        self._lock = Lock()

    @property
    def busy(self) -> bool:
        return self._lock.locked()

    def execute(self, operation: Callable[..., T], *args, **kwargs,) -> T:
        if not self._lock.acquire(blocking=False):
            raise AdvisorBusyError("AdvisorEngine is already processing another request.")

        try:
            return operation(*args, **kwargs)
        finally:
            self._lock.release()