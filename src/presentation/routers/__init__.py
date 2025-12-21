from .auth import AuthRouter
from .user import UserRouter

__all__: tuple[str] = ("AuthRouter", "UserRouter")
