from uuid import UUID

from domain.entities.user import (
    CreateUserDomainModel,
    ReadUserDomainModel,
    UpdateUserDomainModel,
)
from domain.repositories.user_repositories import UserABSWriteRepository


class CommandUserUseCases:
    def __init__(self, user_repository: UserABSWriteRepository) -> None:
        self.user_repository = user_repository

    async def execute_create_user(self, **kwargs) -> ReadUserDomainModel:
        kwargs["password"] = kwargs["password"].get_secret_value()
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
