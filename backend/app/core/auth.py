from datetime import datetime, timedelta, timezone
from typing import List
from fastapi import HTTPException
from passlib import context
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.core.config import settings
from app.core.security.jwt import decode_jwt, encode_jwt

pwd_context = context.CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(sub: str) -> str:
    exp_delta = timedelta(minutes=settings.jwt_access_token_expire_minutes)
    jwt_payload = {"sub": str(sub), "aud": "access"}
    return encode_jwt(jwt_payload, exp_delta)


def create_refresh_token(sub: str) -> str:
    exp_delta = timedelta(minutes=settings.jwt_refresh_token_expire_minutes)
    jwt_payload = {"sub": str(sub), "aud": "refresh"}
    return encode_jwt(jwt_payload, exp_delta)


async def verify_user_token(token: str, session: AsyncSession, audience: List[str]) -> User:
    try:
        credentials_exception = HTTPException(
            status_code=401,
            detail="Invalid token or token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
        payload = decode_jwt(token, audience)
        sub = payload.get("sub")

        if not sub:
            raise credentials_exception

        query = select(User).where(User.id == int(sub))
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        if user is None:
            raise credentials_exception
        return user
    except Exception:
        raise credentials_exception
