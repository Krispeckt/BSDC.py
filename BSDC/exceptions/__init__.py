from typing import Callable, TypeVar

T = TypeVar("T")

__all__ = (
    "IsNotCoro",
    "WaitMore",
    "UnknownException",
    "ClientNotFound",
    "TaskNotFound"
)


class IsNotCoro(Exception):
    def __init__(self, func: Callable[[T], T]) -> None:
        super().__init__(
            f"{func.__qualname__} is not a coroutine."
        )


class WaitMore(Exception):
    def __init__(self) -> None:
        super().__init__(
            "Request not available, wait more! Try again later."
        )


class UnknownException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class ClientNotFound(Exception):
    def __init__(self) -> None:
        super().__init__("BSDC client not found! Please create it again! BSDCClient.create()")


class TaskNotFound(Exception):
    def __init__(self) -> None:
        super().__init__("Task not found!")