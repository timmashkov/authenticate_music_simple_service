from dataclasses import dataclass
from typing import List

from domain.entities import ReadRoleDomainModel
from domain.entities.base import BaseDomainEntity


@dataclass
class UpdateUserDomainModel(BaseDomainEntity):
    age: int
    phone_number: str


@dataclass
class CreateUserDomainModel(UpdateUserDomainModel):
    login: str
    password: str
    email: str


@dataclass
class ReadUserDomainModel(CreateUserDomainModel):
    pass


@dataclass
class UserWithRoles(ReadUserDomainModel):
    roles: List[ReadRoleDomainModel] | None
