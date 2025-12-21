from typing import Optional
from uuid import UUID


class SessionManager:
    def __init__(self, redis_client, session_ttl: int = 2592000) -> None:  # 30 days
        self.redis = redis_client
        self.session_ttl = session_ttl

    async def save_session(
        self, user_id: UUID, access_token: str, refresh_token: str
    ) -> None:
        session_data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": str(user_id),
        }
        await self.redis.set(f"session:{user_id}", session_data, ex=self.session_ttl)

    async def get_session(self, user_id: UUID) -> Optional[dict]:
        return await self.redis.get(f"session:{user_id}")

    async def delete_session(self, user_id: UUID) -> bool:
        return await self.redis.delete(f"session:{user_id}")
