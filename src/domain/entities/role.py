from dataclasses import dataclass

from domain.entities.base import BaseDomainEntity


@dataclass
class CreateRoleDomainModel(BaseDomainEntity):
    name: str


@dataclass
class ReadRoleDomainModel(CreateRoleDomainModel):
    pass
