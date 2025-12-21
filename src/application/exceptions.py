from uuid import UUID


class EntityNotFoundError(Exception):

    def __init__(self, field: UUID | str) -> None:
        self._message = f"Entity with field {field} not found!"
        super().__init__(self._message)

    def __str__(self) -> str:
        return f"EntityNotFoundError: {self._message}"
