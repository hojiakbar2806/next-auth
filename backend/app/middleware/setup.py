from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.core.config import settings


def setup_cors_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "https://next-auth.hojiakbar.me"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
