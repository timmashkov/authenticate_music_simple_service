from uuid import UUID

from application.exceptions import EntityNotFoundError
from domain.entities.permission import ReadPermissionDomainModel
from domain.entities.role import ReadRoleDomainModel
from domain.entities.user import ReadUserDomainModel
from domain.repositories.permissions_repository import PermissionABSReadRepository
from domain.repositories.role_repositories import RoleABSReadRepository
from domain.repositories.user_repositories import UserABSReadRepository
from presentation.models._filter import _APIFilter


class QueryUserUseCases:
    def __init__(self, user_repository: UserABSReadRepository) -> None:
        self.user_repository = user_repository

    async def execute_read_users(
        self, filters: _APIFilter
    ) -> list[ReadUserDomainModel]:
        return await self.user_repository.find_users(filters)

    async def execute_read_user(self, user_uuid: UUID) -> ReadUserDomainModel | None:
        if found_user := await self.user_repository.get_by_id(user_uuid):
            return found_user
        raise EntityNotFoundError(user_uuid)


class QueryRoleUseCases:
    def __init__(self, role_repository: RoleABSReadRepository) -> None:
        self.role_repository = role_repository

    async def execute_read_roles(
        self, filters: _APIFilter
    ) -> list[ReadRoleDomainModel]:
        return await self.role_repository.find_roles(filters)

    async def execute_read_role(self, role_name: str) -> ReadRoleDomainModel | None:
        if found_role := await self.role_repository.get_by_name(role_name):
            return found_role
        raise EntityNotFoundError(role_name)


class QueryPermissionUseCases:
    def __init__(self, perm_repository: PermissionABSReadRepository) -> None:
        self.perm_repository = perm_repository

    async def execute_read_perms(
        self, filters: _APIFilter
    ) -> list[ReadPermissionDomainModel]:
        return await self.perm_repository.find_permissions(filters)

    async def execute_read_perm(
        self, perm_uuid: UUID
    ) -> ReadPermissionDomainModel | None:
        if found_perm := await self.perm_repository.get_by_id(perm_uuid):
            return found_perm
        raise EntityNotFoundError(perm_uuid)
