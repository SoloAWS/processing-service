from pulsar import Client, Consumer, Message
import json
import logging


class LatamProcessingConsumer:
    def __init__(self, pulsar_host: str):
        self.client = Client(f"pulsar://{pulsar_host}:6650")
        self.consumers = {}

    def message_callback(self, consumer, message):
        try:
            data = json.loads(message.data().decode("utf-8"))
            logging.info(
                f"LATAM Processing received message on {consumer.topic()}: {data}"
            )
            consumer.acknowledge(message)
        except Exception as e:
            logging.error(f"Error processing message from {consumer.topic()}: {str(e)}")

    async def subscribe(self):
        topics = [
            "processing.latam.started",
            "processing.latam.completed",
            "processing.latam.failed",
        ]

        for topic in topics:
            consumer = self.client.subscribe(
                topic=topic,
                subscription_name=f"latam-sub-{topic}",
                consumer_name=f"latam-consumer-{topic}",
                message_listener=self.message_callback,
            )
            self.consumers[topic] = consumer

    def close(self):
        for consumer in self.consumers.values():
            consumer.close()
        self.client.close()
