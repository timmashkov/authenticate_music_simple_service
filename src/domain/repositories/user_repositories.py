from abc import ABC, abstractmethod
from typing import Any, List, Union
from uuid import UUID

from sqlalchemy.orm import DeclarativeBase


class UserABSReadRepository(ABC):

    @abstractmethod
    async def get_by_id(self, uuid: Union[str, UUID]) -> DeclarativeBase:
        pass

    @abstractmethod
    async def find_users(self, filters: Any) -> List[DeclarativeBase]:
        pass

    @abstractmethod
    async def get_user_by_login_data(
        self, login: str, password: str
    ) -> DeclarativeBase:
        pass

    @abstractmethod
    async def get_user_with_roles(self, uuid: Union[str, UUID]) -> DeclarativeBase:
        pass


class UserABSWriteRepository(ABC):

    @abstractmethod
    async def create_user(self, **kwargs: Any) -> DeclarativeBase:
        pass

    @abstractmethod
    async def update_user(self, **kwargs: Any) -> DeclarativeBase:
        pass

    @abstractmethod
    async def delete_user(self, uuid: Union[str, UUID]) -> DeclarativeBase:
        pass
