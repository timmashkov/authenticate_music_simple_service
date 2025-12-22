from .auth import AuthRouter
from .permission import PermissionRouter
from .role import RoleRouter
from .user import UserRouter

__all__: tuple[str] = ("AuthRouter", "UserRouter", "RoleRouter", "PermissionRouter")
