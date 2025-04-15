from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        validate_assignment=True,
        env_file_encoding="utf-8",
        extra="ignore",
    )
    VERSION: str = "0.1.2"
    PORT: int = 8000
    HOSTNAME: str = os.getenv('HOSTNAME', 'localhost')

settings = Settings()