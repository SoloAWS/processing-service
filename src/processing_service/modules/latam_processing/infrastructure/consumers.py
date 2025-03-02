import logging
from ....seedwork.infrastructure.messaging import PulsarConsumer
from ....config.settings import Settings

logger = logging.getLogger(__name__)

class LatamProcessingConsumer:
    """Consumer for LATAM processing events"""
    
    def __init__(self, pulsar_host: str = None):
        self.settings = Settings()
        self.consumer = PulsarConsumer(service_name="latam")
    
    def process_message(self, data):
        """Process messages received from Pulsar"""
        logger.info(f"LATAM Processing received message: {data}")
        # Add business logic for handling the message here
    
    async def subscribe(self):
        """Subscribe to the LATAM processing topics"""
        # Only subscribe to the 'started' event topic for now
        topics = [self.settings.PROCESSING_LATAM_STARTED_TOPIC]
        
        self.consumer.subscribe(topics, self.process_message)
        logger.info(f"Subscribed to LATAM processing topics: {topics}")
    
    def close(self):
        """Close the consumer connection"""
        self.consumer.close()