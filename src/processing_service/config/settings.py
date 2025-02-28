import logging
from pydantic_settings import BaseSettings
from typing import Dict

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/processing_db"

    # StreamNative Pulsar settings
    PULSAR_SERVICE_URL: str = "pulsar+ssl://pc-52a07d43.gcp-shared-usce1.g.snio.cloud:6651"
    PULSAR_TOKEN: str = ""
    
    # Topics
    PROCESSING_USA_STARTED_TOPIC: str = "persistent://public/default/processing.usa.started"
    PROCESSING_USA_COMPLETED_TOPIC: str = "persistent://public/default/processing.usa.completed"
    PROCESSING_USA_FAILED_TOPIC: str = "persistent://public/default/processing.usa.failed"
    PROCESSING_LATAM_STARTED_TOPIC: str = "persistent://public/default/processing.latam.started"
    PROCESSING_LATAM_COMPLETED_TOPIC: str = "persistent://public/default/processing.latam.completed"
    PROCESSING_LATAM_FAILED_TOPIC: str = "persistent://public/default/processing.latam.failed"
    
    # Topic mappings for easy access
    @property
    def TOPIC_MAPPING(self) -> Dict[str, str]:
        return {
            "processing.usa.started": self.PROCESSING_USA_STARTED_TOPIC,
            "processing.usa.completed": self.PROCESSING_USA_COMPLETED_TOPIC,
            "processing.usa.failed": self.PROCESSING_USA_FAILED_TOPIC,
            "processing.latam.started": self.PROCESSING_LATAM_STARTED_TOPIC,
            "processing.latam.completed": self.PROCESSING_LATAM_COMPLETED_TOPIC,
            "processing.latam.failed": self.PROCESSING_LATAM_FAILED_TOPIC,
        }

    # API settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    class Config:
        env_file = ".env"