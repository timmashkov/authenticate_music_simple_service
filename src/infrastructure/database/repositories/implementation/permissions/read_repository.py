from typing import Iterable
from uuid import UUID

from domain.repositories.permissions_repository import PermissionABSReadRepository
from infrastructure.database.database_adapter import DatabaseAdapter
from infrastructure.database.models import Permission
from infrastructure.database.repositories.common.common_read_repo import (
    _CommonReadRepository,
)


class PermissionReadRepository(PermissionABSReadRepository):

    def __init__(self, session_adapter: DatabaseAdapter) -> None:
        self._read_repo: _CommonReadRepository = _CommonReadRepository(
            session_adapter=session_adapter, model=Permission
        )

    async def get_by_id(self, user_id: UUID) -> Permission | None:
        return await self._read_repo.get_item(user_id)

    async def find_permissions(self, filters) -> Iterable[Permission]:
        return await self._read_repo.find(filters)
