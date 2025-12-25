from dataclasses import dataclass
from datetime import UTC, datetime, timedelta, timezone
from typing import List
from uuid import UUID


@dataclass
class UserData:
    age: int
    phone_number: str
    data: dict
    login: str
    password: str
    email: str
    uuid: UUID
    created_at: datetime
    updated_at: datetime


@dataclass
class AuthSession:
    user_id: UUID
    permissions: List[str]
    issued_at: datetime
    expires_at: datetime
    refresh_token: str | None = None

    def is_expired(self) -> bool:
        return datetime.now(UTC) > self.expires_at

    def can_refresh(self) -> bool:
        return self.refresh_token is not None and not self.is_expired()

    def time_until_expiry(self) -> timedelta:
        now = datetime.now(timezone.utc)
        if now > self.expires_at:
            return timedelta(seconds=0)
        return self.expires_at - now


@dataclass
class AuthenticationResult:
    user_id: UUID
    access_token: str
    refresh_token: str | None
    token_type: str = "bearer"
    expires_in: int = 3600
    time_left_for_token: timedelta | None = None


@dataclass
class TokenPayload:
    sub: UUID  # user_id
    permissions: List[str]
    exp: datetime
    iat: datetime
