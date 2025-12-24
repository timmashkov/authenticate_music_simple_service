from dataclasses import dataclass

from domain.entities.base import BaseDomainEntity


@dataclass
class CreatePermissionDomainModel(BaseDomainEntity):
    name: str
    layer: str


@dataclass
class ReadPermissionDomainModel(CreatePermissionDomainModel):
    pass
