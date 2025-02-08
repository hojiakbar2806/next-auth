import uvicorn
from fastapi import FastAPI
from app.core.config import settings
from app.middleware.setup import setup_cors_middleware, setup_session_middleware
from app.routers.auth_router import router as auth_router
from starlette.middleware.cors import CORSMiddleware


app = FastAPI()

setup_cors_middleware(app)
setup_session_middleware(app)


@app.get("/")
async def read_root():
    return {
        "app_name": settings.app_name,
        "environment": settings.app_env,
        "debug_mode": settings.app_debug
    }


app.include_router(auth_router, prefix="/auth", tags=["auth"])
