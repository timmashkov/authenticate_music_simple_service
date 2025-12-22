from .auth import AuthRouter
from .user import UserRouter
from .role import RoleRouter

__all__: tuple[str] = ("AuthRouter", "UserRouter", "RoleRouter")
