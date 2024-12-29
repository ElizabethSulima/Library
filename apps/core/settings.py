from dotenv import load_dotenv
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()


class Config(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")

    # DB settings
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "db"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    @computed_field
    def async_dsn(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:"
            f"{self.DB_PASSWORD}@{self.DB_HOST}:"
            f"{self.DB_PORT}/{self.DB_NAME}"
        )


config = Config()
