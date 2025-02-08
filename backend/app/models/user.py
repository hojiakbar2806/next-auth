import enum
from app.database.base import Base
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column, Date, DateTime, Enum,
    Integer, String, Boolean, ForeignKey, Text
)


class UserStatus(str, enum.Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    DELETED = 'deleted'


class OAuthProvider(str, enum.Enum):
    GOOGLE = 'google'
    GITHUB = 'github'


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=True)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE)
    is_oauth = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    oauth_provider = Column(Enum(OAuthProvider), nullable=True)
    last_login_at = Column(
        DateTime(timezone=True), nullable=False,
        default=datetime.now(timezone.utc)
    )
    role_id = Column(Integer, ForeignKey('roles.id'))

    profile = relationship("Profile", back_populates="user", uselist=False)
    role = relationship("Role", back_populates="users")


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

    users = relationship("User", back_populates="role")


class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey('users.id'),
        nullable=False, unique=True
    )
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    profile_pic = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)

    user = relationship("User", back_populates="profile")
