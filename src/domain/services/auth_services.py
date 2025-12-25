from abc import ABC, abstractmethod

from domain.entities.auth import AuthSession


class TokenProvider(ABC):

    @abstractmethod
    def create_access_token(self, session: AuthSession) -> str:
        pass

    @abstractmethod
    def create_refresh_token(self, session: AuthSession) -> str:
        pass

    @abstractmethod
    def verify_token(self, token: str) -> AuthSession:
        pass

    @abstractmethod
    def refresh_tokens(self, refresh_token: str) -> tuple[str, str] | None:
        pass
