from abc import ABC, abstractmethod
from typing import Any, Union
from uuid import UUID


class UserABSReadRepository(ABC):

    @abstractmethod
    async def get_by_id(self, uuid: Union[str, UUID]) -> Any:
        pass

    @abstractmethod
    async def find_users(self, filters: Any) -> Any:
        pass

    @abstractmethod
    async def get_user_by_login_data(self, login: str, password: str) -> Any:
        pass


class UserABSWriteRepository(ABC):

    @abstractmethod
    async def create_user(self, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    async def update_user(self, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    async def delete_user(self, uuid: Union[str, UUID]) -> Any:
        pass
