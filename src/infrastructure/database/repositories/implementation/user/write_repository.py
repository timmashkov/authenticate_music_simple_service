from uuid import UUID

from domain.entities.user import CreateUserDomainModel
from domain.repositories.user_repositories import UserABSWriteRepository
from infrastructure.database.database_adapter import DatabaseAdapter
from infrastructure.database.models import User
from infrastructure.database.repositories.common.common_write_repo import (
    _CommonWriteRepository,
)


class UserWriteRepository(UserABSWriteRepository):

    def __init__(self, session_adapter: DatabaseAdapter) -> None:
        self._write_repo: _CommonWriteRepository = _CommonWriteRepository(
            session_adapter=session_adapter, model=User
        )

    async def create_user(self, user_data: CreateUserDomainModel) -> User:
        return await self._write_repo.create_item(**user_data.as_dict())

    async def update_user(
        self, user_uuid: UUID, user_data: CreateUserDomainModel
    ) -> User:
        user_data = user_data.as_dict()
        user_data["uuid"] = user_uuid
        return await self._write_repo.update_item(**user_data)

    async def delete_user(self, uuid: UUID) -> User:
        return await self._write_repo.delete_item(uuid=uuid)
