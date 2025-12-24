from uuid import UUID

from domain.entities.user import CreateUserDomainModel
from domain.repositories.permissions_repository import PermissionABSWriteRepository
from infrastructure.database.database_adapter import DatabaseAdapter
from infrastructure.database.models import Permission
from infrastructure.database.repositories.common.common_write_repo import (
    _CommonWriteRepository,
)


class PermissionWriteRepository(PermissionABSWriteRepository):

    def __init__(self, session_adapter: DatabaseAdapter) -> None:
        self._write_repo: _CommonWriteRepository = _CommonWriteRepository(
            session_adapter=session_adapter, model=Permission
        )

    async def create_permission(
        self, permission_data: CreateUserDomainModel
    ) -> Permission:
        return await self._write_repo.create_item(**permission_data.as_dict())

    async def update_permission(
        self, permission_uuid: UUID, permission_data: CreateUserDomainModel
    ) -> Permission:
        permission_data = permission_data.as_dict()
        permission_data["uuid"] = permission_uuid
        return await self._write_repo.update_item(**permission_data)

    async def delete_permission(self, uuid: UUID) -> Permission:
        return await self._write_repo.delete_item(uuid=uuid)
