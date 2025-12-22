from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from infrastructure.database.models import Role
from presentation.models._filter import _APIFilter


class RoleWriteModel(BaseModel):
    name: str = Field(description=Role.name.comment)
    data: dict | None = Field(default_factory=dict, description=Role.data.comment)


class RoleReadModel(RoleWriteModel):
    uuid: UUID
    created_at: datetime = Field(description=Role.created_at.comment)
    updated_at: datetime = Field(description=Role.updated_at.comment)


class RoleFilter(_APIFilter):
    uuid: UUID | None = None
    name: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Constants(_APIFilter.Constants):
        model = Role
