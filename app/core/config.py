from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "fast-api-auth"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # PostgreSQL async connection URL
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/fast_api_auth"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
