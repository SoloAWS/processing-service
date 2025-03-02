import logging
from ....seedwork.infrastructure.messaging import PulsarConsumer
from ...processing.infrastructure.messaging.schema_registry import (
    ProcessingStartedSchema,
    ProcessingCompletedSchema,
    ProcessingFailedSchema,
)
from pulsar.schema import AvroSchema
from ....config.settings import Settings

logger = logging.getLogger(__name__)


class LatamProcessingConsumer:
    """Consumer for LATAM processing events with schema validation"""

    def __init__(self, pulsar_host: str = None):
        self.settings = Settings()
        self.consumer = PulsarConsumer(service_name="latam")

        # Configure schema mapping for topics
        schema_mapping = {
            self.settings.PROCESSING_LATAM_STARTED_TOPIC: AvroSchema(
                ProcessingStartedSchema
            ),
            self.settings.PROCESSING_LATAM_COMPLETED_TOPIC: AvroSchema(
                ProcessingCompletedSchema
            ),
            self.settings.PROCESSING_LATAM_FAILED_TOPIC: AvroSchema(
                ProcessingFailedSchema
            ),
        }
        self.consumer.set_schema_mapping(schema_mapping)

    def process_message(self, data):
        """Process messages received from Pulsar with schema validation"""
        logger.info(f"LATAM Processing received message: {data}")

    async def subscribe(self):
        """Subscribe to the LATAM processing topics with schema validation"""
        topics = [
            self.settings.PROCESSING_LATAM_STARTED_TOPIC,
            self.settings.PROCESSING_LATAM_COMPLETED_TOPIC,
            self.settings.PROCESSING_LATAM_FAILED_TOPIC,
        ]

        self.consumer.subscribe(topics, self.process_message)
        logger.info(
            f"Subscribed to LATAM processing topics with schema validation: {topics}"
        )

    def close(self):
        """Close the consumer connection"""
        self.consumer.close()
