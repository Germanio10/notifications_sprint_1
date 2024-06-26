import aiormq
from broker.abstract_broker import AbstractBroker
from core.config import settings
from core.logger import logger


class RabbitBroker(AbstractBroker):
    def __init__(self, connection, channel) -> None:
        self.channel = channel
        self.connection = connection

    async def close(self) -> None:
        if self.connection:
            await self.connection.close()
            logger.info('Disconnected from Rabbit.')

    async def create_queue(self) -> None:
        await self.channel.queue_declare(queue=settings.queue_from_scheduler, durable=True)
        await self.channel.queue_declare(queue=settings.queue_remove_scheduled, durable=True)

    async def consume(self, queue, callback) -> None:
        await self.channel.basic_consume(queue, callback, no_ack=True)

    async def send_to_broker(self, body: bytes, exchange: str = '') -> None:
        message_properties = aiormq.spec.Basic.Properties(
            delivery_mode=2,
        )
        try:
            await self.channel.basic_publish(
                exchange=exchange,
                routing_key=settings.queue_from_scheduler,
                body=body,
                properties=message_properties,
            )
        except aiormq.exceptions.AMQPError as er:
            raise str(er) from er
