from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.models.user import User
from app.core.auth import verify_user_token
from app.database.session import get_session

auth_schema = HTTPBearer()


async def get_current_user(auth: HTTPAuthorizationCredentials = Depends(auth_schema), session: AsyncSession = Depends(get_session)) -> User:
    return await verify_user_token(auth.credentials, session, ["access"])
