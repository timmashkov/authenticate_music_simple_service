from dataclasses import dataclass
from datetime import UTC, datetime
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


@dataclass
class AuthenticationResult:
    user_id: UUID
    access_token: str
    refresh_token: str | None
    token_type: str = "bearer"
    expires_in: int = 3600


@dataclass
class TokenPayload:
    sub: UUID  # user_id
    permissions: List[str]
    exp: datetime
    iat: datetime
