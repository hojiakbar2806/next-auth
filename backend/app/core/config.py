from pathlib import Path
from dotenv import load_dotenv
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
CORE = Path(__file__).resolve().parent


class Settings(BaseSettings):
    app_name: str
    app_env: str
    app_debug: bool
    app_host: str
    app_port: int
    api_prefix: str
    secret_key: SecretStr
    frontend_token_holder_url: str

    db_user: str = Field(..., alias='POSTGRES_USER')
    db_password: str = Field(..., alias='POSTGRES_PASSWORD')
    db_name: str = Field(..., alias='POSTGRES_DB')
    db_host: str = Field('localhost', alias='POSTGRES_HOST')
    db_port: int = Field(5432, alias='POSTGRES_PORT')

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    jwt_algorithm: str
    jwt_access_token_expire_minutes: int
    jwt_refresh_token_expire_minutes: int

    jwt_public_key_path: Path
    jwt_private_key_path: Path

    google_client_id: str
    google_client_secret: str

    github_client_id: str
    github_client_secret: str

    facebook_client_id: str
    facebook_client_secret: str

    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str

    class Config:
        extra = 'ignore'
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
