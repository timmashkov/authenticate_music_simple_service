from abc import ABC, abstractmethod
from typing import Any, List, Union
from uuid import UUID


class RoleABSReadRepository(ABC):

    @abstractmethod
    async def get_by_name(self, name: str) -> Any:
        pass

    @abstractmethod
    async def find_roles(self, filters: Any) -> List[Any]:
        pass


class RoleABSWriteRepository(ABC):

    @abstractmethod
    async def create_role(self, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    async def add_role_to_user(
        self, role_uuid: UUID, user_uuid: UUID
    ) -> Any:
        pass

    @abstractmethod
    async def update_role(self, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    async def delete_role(self, uuid: Union[str, UUID]) -> Any:
        pass
