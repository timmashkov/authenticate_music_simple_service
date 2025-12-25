from datetime import UTC, datetime, timedelta, timezone
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
        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=self.access_token_expire_minutes)
        payload = {
            "sub": str(session.user_id),
            "permissions": session.permissions,
            "exp": expire.timestamp(),
            "iat": now.timestamp(),
            "type": "access",
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, session: AuthSession) -> str:
        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=self.access_token_expire_minutes)

        payload = {
            "sub": str(session.user_id),
            "exp": expire.timestamp(),
            "iat": now.timestamp(),
            "type": "refresh",
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def refresh_tokens(self, refresh_token: str) -> tuple[str, str] | None:
        try:
            payload = jwt.decode(
                refresh_token,
                self.secret_key,
                algorithms=[self.algorithm],
            )
            if payload["scope"] == "refresh_token":
                user_id = payload["sub"]
                fresh_access_token = self.create_access_token(user_id)
                fresh_refresh_token = self.create_refresh_token(user_id)
                return fresh_access_token, fresh_refresh_token
            return None
        except jwt.ExpiredSignatureError:
            raise TokenError("Token expired")
        except jwt.InvalidTokenError as e:
            raise TokenError(f"Invalid token: {e}")

    def decode_refresh_token(self, token: str) -> str:
        payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        if payload["scope"] == "refresh_token":
            return payload["sub"]
        raise TokenError

    def verify_token(self, token: str) -> AuthSession:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            iat_timestamp = payload["iat"]
            exp_timestamp = payload["exp"]
            return AuthSession(
                user_id=UUID(payload["sub"]),
                permissions=payload.get("permissions", []),
                issued_at=datetime.fromtimestamp(iat_timestamp, tz=timezone.utc),
                expires_at=datetime.fromtimestamp(exp_timestamp, tz=timezone.utc),
                refresh_token=None,
            )
        except jwt.ExpiredSignatureError:
            raise TokenError("Token expired")
        except jwt.InvalidTokenError as e:
            raise TokenError(f"Invalid token: {e}")
