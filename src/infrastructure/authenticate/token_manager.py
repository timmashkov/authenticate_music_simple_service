from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt

from domain.entities.auth import AuthSession
from domain.exceptions.auth_exceptions import TokenError
from domain.services.auth_services import TokenProvider


class TokenManager(TokenProvider):
    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        access_token_expire_minutes: int = 60,
        refresh_token_expire_days: int = 30,
    ) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days

    def create_access_token(self, session: AuthSession) -> str:
        expires_delta = timedelta(minutes=self.access_token_expire_minutes)
        expire = datetime.now(UTC) + expires_delta

        payload = {
            "sub": str(session.user_id),
            "permissions": session.permissions,
            "exp": expire,
            "iat": datetime.now(UTC),
            "type": "access",
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, session: AuthSession) -> str:
        expires_delta = timedelta(days=self.refresh_token_expire_days)
        expire = datetime.now(UTC) + expires_delta

        payload = {
            "sub": str(session.user_id),
            "exp": expire,
            "iat": datetime.now(UTC),
            "type": "refresh",
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_refresh_token(self, token: str) -> str:
        payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        if payload["scope"] == "refresh_token":
            return payload["sub"]
        raise TokenError

    def verify_token(self, token: str) -> AuthSession:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

            return AuthSession(
                user_id=UUID(payload["sub"]),
                permissions=payload.get("permissions", []),
                issued_at=payload["iat"],
                expires_at=payload["exp"],
                refresh_token=None,
            )
        except jwt.ExpiredSignatureError:
            raise TokenError("Token expired")
        except jwt.InvalidTokenError as e:
            raise TokenError(f"Invalid token: {e}")
