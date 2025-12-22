from typing import TypeVar

from .base import Base
from .user import User
from .role import Role
from .permission import Permission
from .association import UserRole, RolePermission

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
