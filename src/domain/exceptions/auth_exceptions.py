class TokenError(Exception):

    def __init__(self, message: str) -> None:
        self._message = message
        super().__init__(message)

    def __str__(self) -> str:
        return f"TokenError: {self._message}"
