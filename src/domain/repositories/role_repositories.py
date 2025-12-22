from abc import ABC, abstractmethod
from typing import Any, Union
from uuid import UUID


class RoleABSReadRepository(ABC):

    @abstractmethod
    async def get_by_name(self, name: str) -> Any:
        pass

    @abstractmethod
    async def find_roles(self, filters: Any) -> Any:
        pass


class RoleABSWriteRepository(ABC):

    @abstractmethod
    async def create_role(self, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    async def update_role(self, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    async def delete_role(self, uuid: Union[str, UUID]) -> Any:
        pass
