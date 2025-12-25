from uuid import UUID
from fastapi import HTTPException

class EntityNotFoundError(Exception):

    def __init__(self, field: UUID | str) -> None:
        self._message = f"Entity with field {field} not found!"
        super().__init__(self._message)

    def __str__(self) -> str:
        return f"EntityNotFoundError: {self._message}"


class Unauthorized(HTTPException):

    def __init__(self, field: UUID | str | None) -> None:
        self._field = field
        self._status_code: int =401
        super().__init__(self._status_code)

    def __str__(self) -> str:
        err_message = f"Unauthorized: User with uuid: {self._field} not found!" if self._field else "Unauthorized"
        return err_message
