from fastapi.responses import JSONResponse
from datetime import datetime, timedelta

from core.security import jwt
from core.config import settings


def to_came_case(name: str) -> str:
    return "".join([word.lower() for word in name.split("_")])+"s"


def create_tokens(username: str):
    refresh_token = jwt.create_refresh_token(username)
    access_token = jwt.create_access_token(username)
    return refresh_token, access_token


def set_refresh_token_cookie(response: JSONResponse, refresh_token: str):
    expires = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRES_MINUTES)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        expires=int(expires.timestamp()),
        httponly=True,
        secure=True,
        samesite='None'
    )
