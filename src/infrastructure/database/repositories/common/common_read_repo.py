from typing import Any, Callable, Generic, Iterable, Type
from uuid import UUID

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import async_sessionmaker

from infrastructure.database.database_adapter import DatabaseAdapter
from infrastructure.database.models import table


class _CommonReadRepository(Generic[table]):

    def __init__(
        self,
        session_adapter: DatabaseAdapter,
        model: Type[table],
        query_modifier: Callable[[select], select] = None,
    ) -> None:
        self._model = model
        self._session: async_sessionmaker = session_adapter.autocommit_session
        self._query_modifier = query_modifier

    @classmethod
    def __set_filter(cls, query: select, filters: Any = None) -> select:
        if filters:
            query = filters.filter(query)
        return query

    def _get_query(self) -> select:
        query = select(self._model)
        if self._query_modifier:
            query = self._query_modifier(query)
        return query

    async def get_item(self, uuid: str | UUID) -> table | None:
        async with self._session() as session:
            stmt = self._get_query().where(self._model.uuid == uuid)
            answer = await session.execute(stmt)
        return answer.unique().scalar_one_or_none()

    async def find(
        self,
        filters: Any = None,
    ) -> Iterable[table]:
        query = self._get_query()
        query = self.__set_filter(query, filters)
        async with self._session() as session:
            result = await session.execute(query)
            return result.scalars().unique().all()

    async def _run_custom_command(self, command: text) -> None:
        async with self._session() as session:
            await session.execute(command)
