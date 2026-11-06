from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "fast-api-auth"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # PostgreSQL async connection URL
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/fast_api_auth"

    # JWT Authentication
    SECRET_KEY: str = "supersecretjwtkeyforlocaldevelopmentchangeinproduction"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
