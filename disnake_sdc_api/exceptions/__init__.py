from typing import Callable, TypeVar

T = TypeVar("T")

__all__ = (
    "IsNotCoro",
    "WaitMore",
    "UnknownException"
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
