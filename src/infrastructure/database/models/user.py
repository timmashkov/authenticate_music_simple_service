from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.models import Base


class User(Base):

    login: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        index=True,
        comment="Логин пользователя",
    )
    password: Mapped[str] = mapped_column(
        Text,
        unique=False,
        nullable=False,
        comment="Зашифрованный пароль пользователя",
    )
    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        index=True,
        comment="Email пользователя",
    )
    age: Mapped[int] = mapped_column(
        Integer,
        unique=False,
        nullable=False,
        comment="Возраст пользователя",
    )
    phone_number: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        comment="Телефонный номер пользователя",
    )
