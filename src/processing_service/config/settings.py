import logging
from pydantic_settings import BaseSettings
from typing import Dict

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = (
        "postgresql+asyncpg://user:password@localhost:5432/processing_db"
    )

    # StreamNative Pulsar settings
    PULSAR_SERVICE_URL: str = (
        "pulsar+ssl://pc-52a07d43.gcp-shared-usce1.g.snio.cloud:6651"
    )
    PULSAR_TOKEN: str = (
        "eyJhbGciOiJSUzI1NiIsImtpZCI6IjFlMGRmYTU5LTdhZWItNTA5Ny1hMDFiLTJhMGFkMTgwNzFiMiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsidXJuOnNuOnB1bHNhcjpvLWxnd3lwOnNuLWluc3RhbmNlIl0sImV4cCI6MTc0MzI5NTQxOSwiaHR0cHM6Ly9zdHJlYW1uYXRpdmUuaW8vc2NvcGUiOlsiYWRtaW4iLCJhY2Nlc3MiXSwiaHR0cHM6Ly9zdHJlYW1uYXRpdmUuaW8vdXNlcm5hbWUiOiJhZG1pbnNlcnZpY2VhY2NvdW50QG8tbGd3eXAuYXV0aC5zdHJlYW1uYXRpdmUuY2xvdWQiLCJpYXQiOjE3NDA3MDM0MjAsImlzcyI6Imh0dHBzOi8vcGMtNTJhMDdkNDMuZ2NwLXNoYXJlZC11c2NlMS5nLnNuaW8uY2xvdWQvYXBpa2V5cy8iLCJqdGkiOiIzMDI1OWRlNzFiMmI0YTFhOWExMmJhZTEzMTcxYWNiMSIsInBlcm1pc3Npb25zIjpbXSwic3ViIjoiRHV0bnVsN1NiTlpvbUFtd21UR0VCQ0JEMU5uaDZpc2hAY2xpZW50cyJ9.N0XAsTN4HRdDx-H2ncAhBVzs3xqw5f_Ir8j69qcnEKIyNmSCL789as-cRASyTFn4sfQVGFXfvYGIeno-0dtjvN5u1NutSlqhcb10wQjut_0Awh7KXmu1bPdb616YxBgE4CXgDygYagPQp2S66Sdxp0s8ghtDPmhNlpMeYzHRM3whBfxQ0tSpFNH2x82dNF6e3fKj7TW1X7C_Qh_tcw7xbUsUmZd1IjS8uFMeAOToVr5eO9NIXLjAKKMVgz10iEURbG84A20LLoaC14dZVXvUtQffm54CVxHUQJzhvVXfyijihkjuoxfVANxh-29OMAPdV_0YiNdS1nV3XRjp9nZytA"
    )

    # Topics
    PROCESSING_USA_STARTED_TOPIC: str = (
        "persistent://public/default/processing.usa.started"
    )
    PROCESSING_USA_COMPLETED_TOPIC: str = (
        "persistent://public/default/processing.usa.completed"
    )
    PROCESSING_USA_FAILED_TOPIC: str = (
        "persistent://public/default/processing.usa.failed"
    )
    PROCESSING_LATAM_STARTED_TOPIC: str = (
        "persistent://public/default/processing.latam.started"
    )
    PROCESSING_LATAM_COMPLETED_TOPIC: str = (
        "persistent://public/default/processing.latam.completed"
    )
    PROCESSING_LATAM_FAILED_TOPIC: str = (
        "persistent://public/default/processing.latam.failed"
    )

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
