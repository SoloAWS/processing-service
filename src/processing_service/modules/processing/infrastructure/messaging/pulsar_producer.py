from pulsar import Client, Producer
import json
import logging
from .....seedwork.domain.events import DomainEvent


class PulsarEventPublisher:
    def __init__(self, pulsar_host: str):
        self.client = Client(f"pulsar://{pulsar_host}:6650")
        self.producers: dict[str, Producer] = {}

    def _get_topic_name(self, event_type: str) -> str:
        return f"processing-{event_type.lower()}"

    async def publish_event(self, event: DomainEvent):
        event_type = event.__class__.__name__
        topic = self._get_topic_name(event_type)

        if topic not in self.producers:
            self.producers[topic] = self.client.create_producer(topic)

        try:
            await self.producers[topic].send(
                json.dumps(event.to_dict()).encode("utf-8")
            )
        except Exception as e:
            logging.error(f"Error publishing event to {topic}: {str(e)}")
            raise

    def close(self):
        for producer in self.producers.values():
            producer.close()
        self.client.close()
