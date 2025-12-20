from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, SecretStr

from infrastructure.database.models import User
from presentation.models._filter import _APIFilter


class CredentialsModel(BaseModel):
    login: str = Field(description=User.login.comment)
    password: SecretStr = Field(description=User.password.comment)


class UserWritePartialModel(BaseModel):
    age: int = Field(description=User.age.comment)
    phone_number: str = Field(description=User.phone_number.comment)
    data: dict | None = Field(default_factory=dict, description=User.data.comment)


class UserWriteModel(CredentialsModel, UserWritePartialModel):
    email: EmailStr = Field(description=User.email.comment)


class UserReadModel(UserWriteModel):
    uuid: UUID
    created_at: datetime = Field(description=User.created_at.comment)
    updated_at: datetime = Field(description=User.updated_at.comment)


class UserFilter(_APIFilter):
    uuid: UUID | None = None
    login: str | None = None
    age: int | None = None
    phone_number: str | None = None
    email: EmailStr | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Constants(_APIFilter.Constants):
        model = User
