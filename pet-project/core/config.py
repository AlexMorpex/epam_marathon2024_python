from pydantic import BaseModel, MySQLDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000

class DatabaseConfig(BaseSettings):
    url: MySQLDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10
    alembic_url: str = "mysql+aiomysql://admin:admin@db:3306/petproject"
    naming_convention: dict[str, str] = {  # Добавляем naming_convention
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    class Config:
        env_prefix = "APP_CONFIG__DB__"

class SmtpConfig(BaseSettings):
    host: str
    port: int
    username: str
    password: str

    class Config:
        env_prefix = "APP_CONFIG__SMTP__"

class AccessToken(BaseSettings):
    lifetime_seconds: int = 3600
    reset_password_token_secret: str = ""
    verification_token_secret: str = ""

    class Config:
        env_prefix = "APP_CONFIG__ACCESS_TOKEN__"

class ApiSettings(BaseModel):
    prefix: str = "/api"
    v1_prefix: str = "/v1"
    auth: str = "/auth"
    users: str = "/users"

    @property
    def bearer_token_url(self) -> str:
        parts = (self.prefix, self.v1_prefix, self.auth, "/login")
        path = "".join(parts)
        return path.removeprefix("/")

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    api: ApiSettings = ApiSettings()
    db: DatabaseConfig = DatabaseConfig()  # Настройки БД
    smtp: SmtpConfig = SmtpConfig()  # Настройки SMTP
    access_token: AccessToken = AccessToken()

settings = Settings()
