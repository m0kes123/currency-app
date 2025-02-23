from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        validate_assignment=True,
        env_file_encoding="utf-8",
        extra="ignore",
    )
    VERSION: str
    PORT: int

settings = Settings()