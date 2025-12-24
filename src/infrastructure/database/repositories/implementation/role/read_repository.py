from typing import Iterable

from sqlalchemy import select

from domain.repositories.role_repositories import RoleABSReadRepository
from infrastructure.database.database_adapter import DatabaseAdapter
from infrastructure.database.models import Role
from infrastructure.database.repositories.common.common_read_repo import (
    _CommonReadRepository,
)


class RoleReadRepository(RoleABSReadRepository):

    def __init__(self, session_adapter: DatabaseAdapter) -> None:
        self._session = session_adapter.autocommit_session
        self._read_repo: _CommonReadRepository = _CommonReadRepository(
            session_adapter=session_adapter, model=Role
        )

    async def get_by_name(self, name: str) -> Role | None:
        async with self._session() as session:
            stmt = select(Role).where(Role.name == name)
            found_role = await session.execute(stmt)
        return found_role.scalar_one_or_none()

    async def find_roles(self, filters) -> Iterable[Role]:
        return await self._read_repo.find(filters)
