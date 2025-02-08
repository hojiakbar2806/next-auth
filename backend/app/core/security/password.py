import secrets
from typing import Optional, Protocol, Union

from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher


class PasswordHelper():
    password_hash = PasswordHash((Argon2Hasher(), BcryptHasher()))

    def verify_and_update(
            self,
            plain_password: str,
            hashed_password: str
    ) -> tuple[bool, Union[str, None]]:

        return self.password_hash.verify_and_update(plain_password, hashed_password)

    def hash(self, password: str) -> str:
        return self.password_hash.hash(password)

    def generate(self) -> str:
        return secrets.token_urlsafe()
