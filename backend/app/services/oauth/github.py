import httpx
from fastapi import HTTPException
from app.core.config import settings


GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_URL = "https://api.github.com/user"
GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"


def github_auth_uri(redirect_uri: str) -> str:
    return (
        f"{GITHUB_AUTH_URL}?client_id={settings.github_client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&scope=user:email"
    )


async def get_github_access_token(code: str, redirect_uri: str) -> str:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url=GITHUB_TOKEN_URL,
                data={
                    "client_id": settings.github_client_id,
                    "client_secret": settings.github_client_secret,
                    "code": code,
                    "redirect_uri": redirect_uri,
                },
                headers={"Accept": "application/json"}
            )
            tokens = response.raise_for_status().json()
            return tokens['access_token']
        except Exception as e:
            raise HTTPException(
                status_code=400, detail="Failed to fetch access token from GitHub"
            )


async def get_github_user_info(access_token: str) -> dict:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url=GITHUB_USER_URL,
                headers={"Authorization": f"token {access_token}"}
            )
            user_info = response.raise_for_status().json()
            return user_info
        except Exception as e:
            raise HTTPException(
                status_code=400, detail="Failed to fetch user info from GitHub"
            )
