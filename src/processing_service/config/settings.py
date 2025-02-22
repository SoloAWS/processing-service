import logging
from pydantic_settings import BaseSettings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = (
        "postgresql+asyncpg://user:password@localhost:5432/processing_db"
    )

    # Pulsar settings
    PULSAR_HOST: str = "localhost"
    PULSAR_PORT: int = 6650

    # API settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    class Config:
        env_file = ".env"
