from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    POSTGRES_DATABASE_USERNAME: str = "postgres"
    POSTGRES_DATABASE_PASSWORD: str = "postgres"
    POSTGRES_DATABASE_HOST: str = "db"
    POSTGRES_DATABASE_PORT: int = 5432
    POSTGRES_DATABASE_NAME: str = "link_db"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_DATABASE_USERNAME}:"
            f"{self.POSTGRES_DATABASE_PASSWORD}@"
            f"{self.POSTGRES_DATABASE_HOST}:{self.POSTGRES_DATABASE_PORT}/"
            f"{self.POSTGRES_DATABASE_NAME}"
        )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
