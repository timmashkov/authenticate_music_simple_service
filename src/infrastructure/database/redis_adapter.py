from typing import Any, Optional

import orjson
import redis.asyncio as redis


class RedisAdapter:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        password: Optional[str] = None,
        db: int = 0,
    ) -> None:
        self.redis = redis.Redis(
            host=host, port=port, password=password, db=db, decode_responses=True
        )

    async def set(self, key: str, value: Any, ex: Optional[int] = None) -> bool:
        serialized_value = orjson.dumps(value)
        return await self.redis.set(key, serialized_value, ex=ex)

    async def get(self, key: str) -> Optional[Any]:
        value = await self.redis.get(key)
        if value:
            return orjson.loads(value)
        return None

    async def delete(self, key: str) -> bool:
        return await self.redis.delete(key) > 0

    async def exists(self, key: str) -> bool:
        return await self.redis.exists(key) > 0

    async def close(self):
        await self.redis.close()
