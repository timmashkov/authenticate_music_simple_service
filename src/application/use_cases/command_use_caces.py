from uuid import UUID

from pydantic import SecretStr

from domain.entities.permission import (
    CreatePermissionDomainModel,
    ReadPermissionDomainModel,
)
from domain.entities.role import CreateRoleDomainModel, ReadRoleDomainModel
from domain.entities.user import (
    CreateUserDomainModel,
    ReadUserDomainModel,
    UpdateUserDomainModel,
)
from domain.repositories.permissions_repository import PermissionABSWriteRepository
from domain.repositories.role_repositories import RoleABSWriteRepository
from domain.repositories.user_repositories import UserABSWriteRepository
from infrastructure.authenticate.security_manager import SecurityManager


class CommandUserUseCases:
    def __init__(
        self, user_repository: UserABSWriteRepository, security_manager: SecurityManager
    ) -> None:
        self.user_repository = user_repository
        self.security_manager = security_manager

    def _salt_pass(self, password: SecretStr, login: str) -> str:
        return self.security_manager.encode_pass(password.get_secret_value(), login)

    async def execute_create_user(self, **kwargs) -> ReadUserDomainModel:
        kwargs["password"] = self._salt_pass(kwargs["password"], kwargs["login"])
        command = CreateUserDomainModel(**kwargs)
        return await self.user_repository.create_user(command)

    async def execute_update_user(self, **kwargs) -> ReadUserDomainModel:
        command = UpdateUserDomainModel(
            age=kwargs["age"], phone_number=kwargs["phone_number"], data=kwargs["data"]
        )
        return await self.user_repository.update_user(
            user_data=command, user_uuid=kwargs["uuid"]
        )

    async def execute_delete_user(self, user_id: UUID) -> ReadUserDomainModel:
        return await self.user_repository.delete_user(user_id)


class CommandRoleUseCases:
    def __init__(self, role_repository: RoleABSWriteRepository) -> None:
        self.role_repository = role_repository

    async def execute_create_role(self, **kwargs) -> ReadRoleDomainModel:
        command = CreateRoleDomainModel(**kwargs)
        return await self.role_repository.create_role(command)

    async def execute_update_role(self, **kwargs) -> ReadRoleDomainModel:
        command = CreateRoleDomainModel(name=kwargs["name"], data=kwargs["data"])
        return await self.role_repository.update_role(
            role_data=command, role_uuid=kwargs["uuid"]
        )

    async def execute_delete_role(self, role_id: UUID) -> ReadRoleDomainModel:
        return await self.role_repository.delete_role(role_id)


class CommandPermissionUseCases:
    def __init__(self, perm_repository: PermissionABSWriteRepository) -> None:
        self.perm_repository = perm_repository

    async def execute_create_permission(self, **kwargs) -> ReadPermissionDomainModel:
        command = CreatePermissionDomainModel(**kwargs)
        return await self.perm_repository.create_permission(command)

    async def execute_update_permission(self, **kwargs) -> ReadPermissionDomainModel:
        command = CreatePermissionDomainModel(
            name=kwargs["name"], layer=kwargs["layer"], data=kwargs["data"]
        )
        return await self.perm_repository.update_permission(
            permission_data=command, permission_uuid=kwargs["uuid"]
        )

    async def execute_delete_permission(
        self, role_id: UUID
    ) -> ReadPermissionDomainModel:
        return await self.perm_repository.delete_permission(role_id)
