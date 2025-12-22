from dataclasses import asdict, dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class CreatePermissionDomainModel:
    name: str
    layer: str
    data: dict

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class ReadPermissionDomainModel(CreatePermissionDomainModel):
    uuid: UUID
    created_at: datetime
    updated_at: datetime
