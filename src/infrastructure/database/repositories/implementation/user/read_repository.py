from uuid import UUID

from sqlalchemy import and_, select

from domain.entities.user import ReadUserDomainModel
from domain.repositories.user_repositories import UserABSReadRepository
from infrastructure.database.models import User
from infrastructure.database.repositories.common.common_read_repo import (
    _CommonReadRepository,
)


class UserReadRepository(UserABSReadRepository):

    def __init__(self, session_adapter) -> None:
        self._read_repo: _CommonReadRepository = _CommonReadRepository(
            session_adapter=session_adapter, model=User
        )

    async def get_by_id(self, user_id: UUID) -> ReadUserDomainModel | None:
        user_model = await self._read_repo.get_item(user_id)
        return self._to_domain_entity(user_model) if user_model else None

    async def get_user_by_login_data(
        self, login: str, password: str
    ) -> ReadUserDomainModel | None:
        async with self._read_repo._session() as session:
            query = select(User).where(
                and_(User.login == login, User.password == password)
            )
            result = await session.execute(query)
            answer = result.scalar_one_or_none()
        return self._to_domain_entity(answer) if answer else None

    async def find_users(self, filters) -> list[ReadUserDomainModel]:
        found_users = await self._read_repo.find(filters)
        return [self._to_domain_entity(data) for data in found_users]

    @staticmethod
    def _to_domain_entity(user_model: User) -> ReadUserDomainModel:
        return ReadUserDomainModel(
            uuid=user_model.uuid,
            login=user_model.login,
            password=user_model.password,
            email=user_model.email,
            age=user_model.age,
            phone_number=user_model.phone_number,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
            data=user_model.data,
        )
