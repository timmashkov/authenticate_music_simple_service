from uuid import UUID

from sqlalchemy import insert

from domain.entities.role import CreateRoleDomainModel
from domain.repositories.role_repositories import RoleABSWriteRepository
from infrastructure.database.database_adapter import DatabaseAdapter
from infrastructure.database.models import Role, UserRole
from infrastructure.database.repositories.common.common_write_repo import (
    _CommonWriteRepository,
)


class RoleWriteRepository(RoleABSWriteRepository):

    def __init__(self, session_adapter: DatabaseAdapter) -> None:
        self._session = session_adapter
        self._write_repo: _CommonWriteRepository = _CommonWriteRepository(
            session_adapter=session_adapter, model=Role
        )

    async def create_role(self, role_data: CreateRoleDomainModel) -> Role:
        return await self._write_repo.create_item(**role_data.as_dict())

    async def add_role_to_user(self, role_uuid: UUID, user_uuid: UUID) -> None:
        async with self._session.transactional_session() as session:
            stmt = insert(UserRole).values(role_uuid=role_uuid, user_uuid=user_uuid)
            await session.execute(stmt)
            await session.commit()

    async def update_role(
        self, role_uuid: UUID, role_data: CreateRoleDomainModel
    ) -> Role:
        role_data = role_data.as_dict()
        role_data["uuid"] = role_uuid
        return await self._write_repo.update_item(**role_data)

    async def delete_role(self, uuid: UUID) -> Role:
        return await self._write_repo.delete_item(uuid=uuid)
