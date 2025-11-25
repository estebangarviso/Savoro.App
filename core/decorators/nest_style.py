"""
NestJS-style decorators
"""

from typing import Type, TypeVar, Callable

T = TypeVar("T")


def Injectable() -> Callable[[Type[T]], Type[T]]:
    """
    Decorator to mark a class as injectable
    Similar to NestJS @Injectable()
    """

    def decorator(cls: Type[T]) -> Type[T]:
        setattr(cls, "_injectable", True)
        return cls

    return decorator


def Controller(prefix: str = ""):
    """
    Decorator to mark a class as controller
    Similar to NestJS @Controller()
    """

    def decorator(cls: Type[T]) -> Type[T]:
        setattr(cls, "_controller", True)
        setattr(cls, "_prefix", prefix)
        return cls

    return decorator
