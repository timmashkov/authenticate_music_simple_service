from abc import ABC, abstractmethod
from typing import Any, Union
from uuid import UUID


class PermissionABSReadRepository(ABC):

    @abstractmethod
    async def get_by_id(self, uuid: Union[str, UUID]) -> Any:
        pass

    @abstractmethod
    async def find_permissions(self, filters: Any) -> Any:
        pass


class PermissionABSWriteRepository(ABC):

    @abstractmethod
    async def create_permission(self, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    async def update_permission(self, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    async def delete_permission(self, uuid: Union[str, UUID]) -> Any:
        pass
