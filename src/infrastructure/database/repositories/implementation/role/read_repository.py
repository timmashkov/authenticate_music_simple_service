from sqlalchemy import select

from domain.entities.role import ReadRoleDomainModel
from domain.repositories.role_repositories import RoleABSReadRepository
from infrastructure.database.database_adapter import DatabaseAdapter
from infrastructure.database.models import Role
from infrastructure.database.repositories.common.common_read_repo import (
    _CommonReadRepository,
)


class RoleReadRepository(RoleABSReadRepository):

    def __init__(self, session_adapter: DatabaseAdapter) -> None:
        self._session = session_adapter
        self._read_repo: _CommonReadRepository = _CommonReadRepository(
            session_adapter=session_adapter, model=Role
        )

    async def get_by_name(self, name: str) -> ReadRoleDomainModel | None:
        async with self._session.autocommit_session() as session:
            stmt = select(Role).where(Role.name == name)
            found_role = await session.execute(stmt)
            answer = found_role.scalar_one_or_none()
        return self._to_domain_entity(answer) if answer else None

    async def find_roles(self, filters) -> list[ReadRoleDomainModel]:
        found_roles = await self._read_repo.find(filters)
        return [self._to_domain_entity(data) for data in found_roles]

    @staticmethod
    def _to_domain_entity(role_model: Role) -> ReadRoleDomainModel:
        return ReadRoleDomainModel(
            uuid=role_model.uuid,
            name=role_model.name,
            created_at=role_model.created_at,
            updated_at=role_model.updated_at,
            data=role_model.data,
        )
