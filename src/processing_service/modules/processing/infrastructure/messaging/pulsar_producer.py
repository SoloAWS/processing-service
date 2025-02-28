import logging
from .....seedwork.domain.events import DomainEvent
from .....seedwork.infrastructure.messaging import PulsarProducer

logger = logging.getLogger(__name__)

class PulsarEventPublisher:
    """Simplified publisher for domain events"""
    
    def __init__(self, pulsar_host: str = None):
        self.producer = PulsarProducer()
    
    def _get_topic_name(self, event_type: str) -> str:
        """Get the fully qualified topic name for the event type"""
        return f"persistent://public/default/processing-{event_type.lower()}"
    
    async def publish_event(self, event: DomainEvent):
        """Publish a domain event to its corresponding topic"""
        event_type = event.__class__.__name__
        topic = self._get_topic_name(event_type)
        
        try:
            self.producer.send_message(topic, event.to_dict())
            logger.info(f"Domain event {event_type} published to {topic}")
        except Exception as e:
            logger.error(f"Failed to publish domain event to {topic}: {str(e)}")
            raise
    
    def close(self):
        """Close the producer connection"""
        self.producer.close()