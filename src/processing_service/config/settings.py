from pydantic import BaseSettings


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "postgresql+asyncpg://user:password@postgres:5432/processing_db"

    # Pulsar settings
    PULSAR_HOST: str = "pulsar"
    PULSAR_PORT: int = 6650

    # API settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    class Config:
        env_file = ".env"
