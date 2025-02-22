from typing import Any
from .....seedwork.application.events import EventHandler
from ...domain.events import ProcessingStarted, ProcessingCompleted, ProcessingFailed
from pulsar import Client, Producer
import json
import logging


class PulsarEventHandler(EventHandler):
    def __init__(self, pulsar_host: str):
        self.client = Client(f"pulsar://{pulsar_host}:6650")
        self.producers: dict[str, Producer] = {}

    def _get_topic_for_region(self, region: str, event_type: str) -> str:
        # Topics will be like: processing.latam.started, processing.usa.completed
        return f"processing.{region.lower()}.{event_type.lower()}"

    async def handle(self, event: Any):
        if isinstance(
            event, (ProcessingStarted, ProcessingCompleted, ProcessingFailed)
        ):
            region = event.metadata.region if hasattr(event, "metadata") else "unknown"
            event_type = event.__class__.__name__
            topic = self._get_topic_for_region(region, event_type)

            if topic not in self.producers:
                self.producers[topic] = self.client.create_producer(topic)

            try:
                self.producers[topic].send(json.dumps(event.to_dict()).encode("utf-8"))
                logging.info(f"Event published to topic {topic}")
            except Exception as e:
                logging.error(f"Error publishing event to {topic}: {str(e)}")
                raise

    def close(self):
        for producer in self.producers.values():
            producer.close()
        self.client.close()
