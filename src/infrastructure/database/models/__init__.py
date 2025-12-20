from typing import TypeVar

from .base import Base
from .user import User

table = TypeVar("table")

__all__: tuple[str] = (
    "User",
    "Base",
    "table",
)
