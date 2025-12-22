from typing import TypeVar

from .association import RolePermission, UserRole
from .base import Base
from .permission import Permission
from .role import Role
from .user import User

table = TypeVar("table")

__all__: tuple[str] = (
    "User",
    "Base",
    "Role",
    "Permission",
    "UserRole",
    "RolePermission",
    "table",
)
