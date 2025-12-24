from typing import Iterable
from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.orm import joinedload

from domain.repositories.user_repositories import UserABSReadRepository
from infrastructure.database.database_adapter import DatabaseAdapter
from infrastructure.database.models import User
from infrastructure.database.repositories.common.common_read_repo import (
    _CommonReadRepository,
)


class UserReadRepository(UserABSReadRepository):

    def __init__(self, session_adapter: DatabaseAdapter) -> None:
        self._session = session_adapter.autocommit_session
        self._read_repo: _CommonReadRepository = _CommonReadRepository(
            session_adapter=session_adapter, model=User
        )

    async def get_by_id(self, user_id: UUID) -> User | None:
        return await self._read_repo.get_item(user_id)

    async def get_user_by_login_data(self, login: str, password: str) -> User | None:
        async with self._session() as session:
            query = select(User).where(
                and_(User.login == login, User.password == password)
            )
            result = await session.execute(query)
        return result.scalar_one_or_none()

    async def get_user_with_roles(
        self,
        user_id: UUID,
    ) -> User | None:
        async with self._session() as session:
            query = (
                select(User).where(User.uuid == user_id).options(joinedload(User.roles))
            )
            result = await session.execute(query)
        return result.unique().scalar_one_or_none()

    async def find_users(self, filters) -> Iterable[User]:
        return await self._read_repo.find(filters)
