from uuid import UUID

from application.exceptions import EntityNotFoundError
from domain.entities.user import ReadUserDomainModel
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
