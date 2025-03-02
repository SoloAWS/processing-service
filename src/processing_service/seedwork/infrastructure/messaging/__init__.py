from pulsar import Client, Producer, Consumer, Authentication, AuthenticationToken
import json
import logging
from typing import Dict, Any, List, Callable, Optional
from ....config.settings import Settings

logger = logging.getLogger(__name__)


class PulsarClient:
    """Base class for Pulsar client interactions"""

    def __init__(self):
        settings = Settings()
        self.settings = settings
        self.client = Client(
            settings.PULSAR_SERVICE_URL,
            authentication=AuthenticationToken(settings.PULSAR_TOKEN),
        )

    def close(self):
        """Close the Pulsar client connection"""
        self.client.close()


class PulsarProducer(PulsarClient):
    """Simplified producer class for sending messages to Pulsar"""

    def __init__(self):
        super().__init__()
        self.producers: Dict[str, Producer] = {}

    def get_producer(self, topic: str) -> Producer:
        """Get or create a producer for the specified topic"""
        if topic not in self.producers:
            self.producers[topic] = self.client.create_producer(topic)
        return self.producers[topic]

    def send_message(self, topic: str, message: Dict[str, Any]):
        """Send a JSON message to the specified topic"""
        try:
            producer = self.get_producer(topic)
            producer.send(json.dumps(message).encode("utf-8"))
            logger.info(f"Message sent to topic: {topic}")
        except Exception as e:
            logger.error(f"Error sending message to {topic}: {str(e)}")
            raise

    def close(self):
        """Close all producers and the client connection"""
        for producer in self.producers.values():
            producer.close()
        super().close()


class PulsarConsumer(PulsarClient):
    """Consumer class for receiving messages from Pulsar with schema support"""

    def __init__(self, service_name: str):
        super().__init__()
        self.consumers: Dict[str, Consumer] = {}
        self.service_name = service_name
        self.schema_mapping: Dict[str, Any] = {}

    def set_schema_mapping(self, mapping: Dict[str, Any]):
        """Set schema mapping to use for different topics"""
        self.schema_mapping = mapping

    def subscribe(self, topics: List[str], message_handler: Callable[[Any], None]):
        """Subscribe to topics with schema validation support"""
        for topic in topics:
            subscription_name = f"{self.service_name}-sub-{topic.split('/')[-1]}"

            # Get schema for this topic if available
            schema = self.schema_mapping.get(topic)

            def callback(consumer, message):
                try:
                    # Decode based on whether schema is being used
                    if schema:
                        # With schema, pulsar client automatically deserializes
                        data = message.value()
                    else:
                        # Without schema, manually deserialize JSON
                        data = json.loads(message.data().decode("utf-8"))

                    logger.info(f"Received message on {consumer.topic()}")
                    # Process the message with the provided handler
                    message_handler(data)
                    consumer.acknowledge(message)
                except Exception as e:
                    logger.error(
                        f"Error processing message from {consumer.topic()}: {str(e)}"
                    )
                    consumer.negative_acknowledge(message)

            # Create consumer with or without schema
            consumer_args = {
                "topic": topic,
                "subscription_name": subscription_name,
                "consumer_name": f"{self.service_name}-consumer-{topic.split('/')[-1]}",
                "message_listener": callback,
            }

            if schema:
                consumer_args["schema"] = schema

            consumer = self.client.subscribe(**consumer_args)
            self.consumers[topic] = consumer
            logger.info(
                f"Subscribed to topic: {topic}"
                + (f" with schema validation" if schema else "")
            )

    def close(self):
        """Close all consumers and the client connection"""
        for consumer in self.consumers.values():
            consumer.close()
        super().close()
