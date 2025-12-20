from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from uuid import UUID


@dataclass
class UpdateUserDomainModel:
    age: int
    phone_number: str
    data: dict

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class CreateUserDomainModel(UpdateUserDomainModel):
    login: str
    password: str
    email: str


@dataclass
class ReadUserDomainModel(CreateUserDomainModel):
    uuid: UUID
    created_at: datetime
    updated_at: datetime

    def change_password(self, new_hashed_password: str) -> None:
        self.password = new_hashed_password
        self.updated_at = datetime.now(UTC)

    def update_profile(self, age: int, phone_number: str) -> None:
        self.age = age
        self.phone_number = phone_number
        self.updated_at = datetime.now(UTC)
