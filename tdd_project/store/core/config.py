from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    PROJECT_NAME: str = "Store API"
    DATABASE_URL: str
    ROOT_PATH: str = "/api/v1"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
