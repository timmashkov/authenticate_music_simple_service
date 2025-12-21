from uuid import UUID

from pydantic import SecretStr

from domain.entities.user import (
    CreateUserDomainModel,
    ReadUserDomainModel,
    UpdateUserDomainModel,
)
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
        print(command)
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
