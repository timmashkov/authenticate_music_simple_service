import hashlib


class SecurityManager:
    def __init__(
        self,
        iterations: int,
        hash_name: str,
        formats: str,
    ) -> None:
        self._iterations = iterations
        self._hash_name = hash_name
        self._formats = formats

    def encode_pass(self, password: str, salt: str) -> str:
        password = password.encode(self._formats)
        salt = salt.encode(self._formats)
        hashed_pass = hashlib.pbkdf2_hmac(
            self._hash_name,
            password=password,
            salt=salt,
            iterations=self._iterations,
        )
        return hashed_pass.hex()

    async def verify_password(
        self,
        password: str,
        salt: str,
        encoded_pass: str,
    ) -> bool:
        hashed_password = self.encode_pass(password=password, salt=salt)
        return hashed_password == encoded_pass
