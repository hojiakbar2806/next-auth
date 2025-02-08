import uuid
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import APIRouter, Cookie, HTTPException, Depends, Request

from app.models.user import User
from app.core.config import settings
from app.core.security.jwt import decode_jwt
from app.database.session import get_session
from app.core.dependency import get_current_user
from app.schemas.user_auth import UserCreate, LoginUser, TokenResponse, UserResponse
from app.services.oauth.github import get_github_access_token, get_github_user_info, github_auth_uri
from app.core.auth import create_access_token, create_refresh_token, hash_password, verify_password, verify_user_token
from app.services.oauth.google import get_google_access_token, get_google_user_info, google_auth_uri

router = APIRouter( prefix="/auth",tags=["Auth"])

one_time_code = {}


@router.get("/login/google")
async def login_via_google(request: Request):
    redirect_uri = request.url_for('authorize_google')
    return RedirectResponse(google_auth_uri(redirect_uri))


@router.get("/google/callback")
async def authorize_google(code: str, request: Request, session: AsyncSession = Depends(get_session)):
    global one_time_code
    token = await get_google_access_token(code, request.url_for("authorize_google"))
    user_info = await get_google_user_info(token)
    query = select(User).where(User.email == user_info.get("email"))
    db_user = (await session.execute(query)).scalar_one_or_none()
    if db_user is None:
        db_user = User(
            username=user_info.get("email"),
            email=user_info.get("email"),
            is_oauth=True,
            oauth_provider="google"
        )
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
    code = uuid.uuid4().hex
    one_time_code[code] = db_user.id
    return RedirectResponse(f"{settings.frontend_token_holder_url}/?code={code}")


@router.get("/login/github")
async def login_via_github(request: Request):
    redirect_uri = request.url_for('authorize_github')
    return RedirectResponse(github_auth_uri(redirect_uri))


@router.get("/github/callback")
async def authorize_github(code: str, request: Request, session: AsyncSession = Depends(get_session)):
    global one_time_code
    token = await get_github_access_token(code, request.url_for("authorize_github"))
    user_info = await get_github_user_info(token)
    query = select(User).where(User.username == user_info.get("login"))
    db_user = (await session.execute(query)).scalar_one_or_none()
    if db_user is None:
        db_user = User(
            username=user_info.get("login"),
            email=f"{user_info.get('login')}@github.com",
            is_oauth=True,
            oauth_provider="github"
        )
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
    code = uuid.uuid4().hex
    one_time_code[code] = db_user.id
    return RedirectResponse(f"{settings.frontend_token_holder_url}/?code={code}")


@router.post("/register", response_model=dict)
async def register_user(user_in: UserCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(User).where(
            (User.username == user_in.username) |
            (User.email == user_in.email))
    )
    existing_db_user = result.scalar_one_or_none()

    if existing_db_user:
        raise HTTPException(
            status_code=400, detail="Username or email already registered")

    user = User(
        username=user_in.username,
        email=user_in.email,
        phone_number=user_in.phone_number,
        hashed_password=hash_password(user_in.hashed_password)
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return {"message": "User registered successfully"}


@router.post("/login", response_model=TokenResponse)
async def login_user(
        user_in: LoginUser,
        session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(User).where(User.username == user_in.username))
    user = result.scalar_one_or_none()

    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(sub=user.id)
    refresh_token = create_refresh_token(sub=user.id)

    return JSONResponse(
        content={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "message": "Login successful",
            "token_type": "bearer"
        }
    )


@router.post("/logout")
async def logout_user(request: Request):
    return JSONResponse(status_code=200, content={"message": "Logout successful"})


@router.get("/session", response_model=UserResponse)
async def get_auth_user(auth_user=Depends(get_current_user)):
    return auth_user


@router.get("/token")
async def refresh_token(code: str):
    global one_time_code
    if code not in one_time_code:
        raise HTTPException(status_code=400, detail="Invalid code")
    refresh_token = create_refresh_token(sub=one_time_code[code])
    del one_time_code[code]
    return JSONResponse(status_code=200, content={"refresh_token": refresh_token})


@router.post("/refresh-token", response_model=TokenResponse)
async def refresh_token(refresh_token: str = Cookie(None), session: AsyncSession = Depends(get_session)):
    if not refresh_token:
        raise HTTPException(status_code=400, detail="You are not logged in")

    user = await verify_user_token(refresh_token, session, ["refresh"])

    access_token = create_access_token(user.id)
    return JSONResponse(status_code=200, content={
        "message": "Access token successfully refreshed",
        "access_token": access_token
    })


@router.post("/check-token")
async def check_token(token: str):
    try:
        decode_jwt(token, ["access", "refresh"])
        return JSONResponse(
            status_code=200,
            content={"message": "Token is valid"}
        )
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Token is invalid",
        )
