from datetime import datetime, timedelta, timezone
from fastapi.responses import JSONResponse

from app.core.config import settings


def set_refresh_token_cookie(response: JSONResponse, refresh_token: str):
    utc_now = datetime.now(timezone.utc)
    exp_delta = timedelta(minutes=settings.jwt_refresh_token_expire_minutes)
    expires = utc_now + exp_delta
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        expires=int(expires.timestamp()),
        httponly=True,
        secure=True,
        samesite='None'
    )
