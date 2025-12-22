from uuid import UUID

from domain.entities.permission import ReadPermissionDomainModel
from domain.repositories.permissions_repository import PermissionABSReadRepository
from infrastructure.database.models import Permission
from infrastructure.database.repositories.common.common_read_repo import (
    _CommonReadRepository,
)


class PermissionReadRepository(PermissionABSReadRepository):

    def __init__(self, session_adapter) -> None:
        self._read_repo: _CommonReadRepository = _CommonReadRepository(
            session_adapter=session_adapter, model=Permission
        )

    async def get_by_id(self, user_id: UUID) -> ReadPermissionDomainModel | None:
        user_model = await self._read_repo.get_item(user_id)
        return self._to_domain_entity(user_model) if user_model else None

    async def find_permissions(self, filters) -> list[ReadPermissionDomainModel]:
        found_users = await self._read_repo.find(filters)
        return [self._to_domain_entity(data) for data in found_users]

    @staticmethod
    def _to_domain_entity(permission_model: Permission) -> ReadPermissionDomainModel:
        return ReadPermissionDomainModel(
            uuid=permission_model.uuid,
            name=permission_model.name,
            layer=permission_model.layer,
            created_at=permission_model.created_at,
            updated_at=permission_model.updated_at,
            data=permission_model.data,
        )
