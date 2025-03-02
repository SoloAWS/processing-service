from typing import Any
from .....seedwork.application.events import EventHandler
from .....seedwork.infrastructure.messaging import PulsarProducer
from ...domain.events import ProcessingStarted, ProcessingCompleted, ProcessingFailed
from ...infrastructure.messaging.schema_registry import event_schemas, event_to_schema_object
from pulsar import Client, Authentication, AuthenticationToken
import logging
from .....config.settings import Settings

logger = logging.getLogger(__name__)

class PulsarEventHandler(EventHandler):
    """Event handler that publishes events to Pulsar with schema validation"""
    
    def __init__(self, pulsar_host: str = None):
        self.settings = Settings()
        self.producer = PulsarProducer()
        # Create client for schema-enabled producers
        self.client = Client(
            self.settings.PULSAR_SERVICE_URL,
            authentication=AuthenticationToken(self.settings.PULSAR_TOKEN)
        )
        
    def _get_topic_name(self, region: str, event_type: str) -> str:
        """Get the fully qualified topic name from the event details"""
        # Create local topic format (e.g., "processing.usa.started")
        topic_key = f"processing.{region.lower()}.{event_type.lower()}"
        
        # Get the fully qualified topic name from settings or use default
        return self.settings.TOPIC_MAPPING.get(
            topic_key, 
            f"persistent://public/default/{topic_key}"
        )
    
    async def handle(self, event: Any):
        """Handle the event by publishing it to the appropriate topic with schema validation"""
        if not isinstance(event, (ProcessingStarted, ProcessingCompleted, ProcessingFailed)):
            return
            
        # Extract region based on event type
        region = event.metadata.region if isinstance(event, ProcessingStarted) else event.region
        
        # Get event type (started, completed, failed)
        event_type = event.__class__.__name__.replace("Processing", "").lower()
        
        # Get the appropriate topic
        topic = self._get_topic_name(region, event_type)
        
        # Send the event
        try:
            # Get schema for this event type
            schema = event_schemas.get(event_type)
            
            if schema:
                schema_obj = event_to_schema_object(event)
                producer = self.client.create_producer(topic, schema=schema)
                producer.send(schema_obj)
                producer.close()
                
                logger.info(f"Event {event.__class__.__name__} published to {topic} with schema validation")
            else:
                # Fall back to original implementation
                self.producer.send_message(topic, event.to_dict())
                logger.info(f"Event {event.__class__.__name__} published to {topic}")
        except Exception as e:
            logger.error(f"Failed to publish event to {topic}: {str(e)}")
            raise
    
    def close(self):
        """Close connections"""
        self.producer.close()
        self.client.close()