from abc import ABC, abstractmethod
from typing import Any, List, Union
from uuid import UUID

from sqlalchemy.orm import DeclarativeBase


class PermissionABSReadRepository(ABC):

    @abstractmethod
    async def get_by_id(self, uuid: Union[str, UUID]) -> DeclarativeBase:
        pass

    @abstractmethod
    async def find_permissions(self, filters: Any) -> List[DeclarativeBase]:
        pass


class PermissionABSWriteRepository(ABC):

    @abstractmethod
    async def create_permission(self, **kwargs: Any) -> DeclarativeBase:
        pass

    @abstractmethod
    async def update_permission(self, **kwargs: Any) -> DeclarativeBase:
        pass

    @abstractmethod
    async def delete_permission(self, uuid: Union[str, UUID]) -> DeclarativeBase:
        pass
