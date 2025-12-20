from typing import Any, Generic, Type

from sqlalchemy import delete, insert, update
from sqlalchemy.ext.asyncio import async_sessionmaker

from infrastructure.database.database_adapter import DatabaseAdapter
from infrastructure.database.models import table


class _CommonWriteRepository(Generic[table]):

    def __init__(self, session_adapter: DatabaseAdapter, model: Type[table]) -> None:
        self._model = model
        self._session: async_sessionmaker = session_adapter.transactional_session

    async def create_item(self, **kwargs: Any) -> table | None:
        async with self._session() as session:
            stmt = insert(self._model).values(kwargs).returning(self._model)
            answer = await session.execute(stmt)
            await session.commit()
        return answer.unique().scalar_one_or_none()

    async def update_item(self, **kwargs: Any) -> table | None:
        async with self._session() as session:
            stmt = (
                update(self._model)
                .values(kwargs)
                .where(self._model.uuid == kwargs["uuid"])
                .returning(self._model)
            )
            answer = await session.execute(stmt)
            await session.commit()
        return answer.unique().scalar_one_or_none()

    async def delete_item(self, **kwargs: Any) -> table | None:
        async with self._session() as session:
            stmt = (
                delete(self._model)
                .where(self._model.uuid == kwargs["uuid"])
                .returning(self._model)
            )
            answer = await session.execute(stmt)
            await session.commit()
        return answer.unique().scalar_one_or_none()
