from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.core.config import settings


def setup_session_middleware(app: FastAPI):
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.secret_key.get_secret_value(),
        same_site="None",
        https_only=True,
        domain=".localhost",
    )


def setup_cors_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://api.localhost:8000"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
