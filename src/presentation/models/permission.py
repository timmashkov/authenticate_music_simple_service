from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from infrastructure.database.models import Permission
from presentation.models._filter import _APIFilter


class PermissionWriteModel(BaseModel):
    name: str = Field(description=Permission.name.comment)
    layer: str = Field(description=Permission.layer.comment)
    data: dict | None = Field(default_factory=dict, description=Permission.data.comment)


class PermissionReadModel(PermissionWriteModel):
    uuid: UUID
    created_at: datetime = Field(description=Permission.created_at.comment)
    updated_at: datetime = Field(description=Permission.updated_at.comment)


class PermissionFilter(_APIFilter):
    uuid: UUID | None = None
    name: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Constants(_APIFilter.Constants):
        model = Permission
