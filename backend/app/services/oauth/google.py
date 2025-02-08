import httpx
from fastapi import HTTPException
from app.core.config import settings


GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USER_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"


def google_auth_uri(redirect_uri: str) -> str:
    return (
        f"{GOOGLE_AUTH_URL}?response_type=code"
        f"&client_id={settings.google_client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&scope=openid email profile"
    )


async def get_google_access_token(code: str, redirect_uri: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "code": code,
                    "client_id": settings.google_client_id,
                    "client_secret": settings.google_client_secret,
                    "redirect_uri": redirect_uri,
                    "grant_type": "authorization_code",
                }
            )
            tokens = response.raise_for_status().json()
            return tokens["access_token"]
        except Exception as e:
            raise HTTPException(
                status_code=400, detail="Failed to fetch access token from Google")


async def get_google_user_info(access_token: str) -> dict:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url=GOOGLE_USER_URL,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            user_info = response.raise_for_status().json()
            return user_info
        except Exception as e:
            raise HTTPException(
                status_code=400, detail="Failed to fetch user info from Google"
            )
