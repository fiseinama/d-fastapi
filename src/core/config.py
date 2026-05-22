from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./blogicum.db"
    SECRET_KEY: str = "SUPER_SECRET_KEY_FOR_BLOGICUM_APPLICATION_2026_LONG_KEY"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()