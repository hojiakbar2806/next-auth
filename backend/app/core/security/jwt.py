import jwt
from pathlib import Path
from pydantic import SecretStr
from typing import List, Optional
from datetime import datetime, timedelta, timezone

from app.core.config import settings

PUBLIC_KEY_PATH = Path(settings.jwt_public_key_path).expanduser()
PRIVATE_KEY_PATH = Path(settings.jwt_private_key_path).expanduser()


def _get_key(algorithm: str, is_private: bool = True) -> str:
    key_path = PRIVATE_KEY_PATH if is_private else PUBLIC_KEY_PATH
    if algorithm == "RS256":
        return key_path.read_text()
    return settings.secret_key.get_secret_value()


def encode_jwt(payload: dict, exp_delta: timedelta, algorithm: Optional[str] = None) -> str:
    utc_now = datetime.now(timezone.utc)
    payload.update({"iat": utc_now, "exp": utc_now + exp_delta})
    algorithm = algorithm or settings.jwt_algorithm
    secret = _get_key(algorithm, is_private=True)
    return jwt.encode(payload, secret, algorithm=algorithm)


def decode_jwt(encoded_jwt: str, audience: List[str]) -> dict:
    algorithm = settings.jwt_algorithm
    secret = _get_key(algorithm, is_private=False)
    return jwt.decode(encoded_jwt, secret, audience=audience, algorithms=[algorithm])
