from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from uuid import UUID


@dataclass
class CreateRoleDomainModel:
    name: str
    data: dict

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class ReadRoleDomainModel(CreateRoleDomainModel):
    uuid: UUID
    created_at: datetime
    updated_at: datetime
