from typing import Optional
from datetime import datetime, date
from pydantic import BaseModel, EmailStr, Field

from app.models.user import OAuthProvider, UserStatus


class LoginUser(BaseModel):
    username: str = Field(..., example="johndoe")
    password: str = Field(..., min_length=8, alias="password")


class UserCreate(BaseModel):
    username: str = Field(..., example="johndoe")
    email: EmailStr = Field(..., example="johndoe@example.com")
    phone_number: Optional[str] = Field(
        None, pattern=r"^\+998\d{9}$", example="+998901234567"
    )
    hashed_password: str = Field(..., min_length=8, alias="password")


class ProfileBase(BaseModel):
    first_name: Optional[str] = Field(None, example="John")
    last_name: Optional[str] = Field(None, example="Doe")
    bio: Optional[str] = Field(None, example="Software Developer")
    profile_pic: Optional[str] = Field(
        None, example="https://example.com/profile.jpg"
    )
    date_of_birth: Optional[date]


class ProfileResponse(ProfileBase):
    id: int

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    username: str = Field(..., example="johndoe")
    email: EmailStr = Field(..., example="johndoe@example.com")
    phone_number: Optional[str] = Field(
        None, pattern=r"^\+998\d{9}$", example="+998901234567"
    )
    status: UserStatus
    is_oauth: bool
    oauth_provider: Optional[OAuthProvider]
    is_superuser: bool
    last_login_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    username: str = Field(..., example="johndoe")
    password: str = Field(..., min_length=8, example="strongpassword123")


class UserWithProfile(BaseModel):
    user: UserResponse
    profile: Optional[ProfileResponse]

    class Config:
        from_attributes = True


class SessionResponse(BaseModel):
    user: UserResponse
    expires: datetime

    class Config:
        from_attributes = True
