import aiormq
from broker.abstract import AbstractBroker


class RabbitBroker(AbstractBroker):

    def __init__(self, connection, channel):
        self.connection = connection
        self.channel = channel

    async def declare_queue(self):
        await self.channel.queue_declare(queue='instant.notification', durable=True)
        await self.channel.queue_declare(queue='sheduled.notification', durable=True)

    async def send_to_broker(self, routing_key: str, body: bytes, exchange: str = ''):
        message_properties = aiormq.spec.Basic.Properties(
            delivery_mode=2
        )
        try:
            await self.channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=body,
                properties=message_properties,
            )
        except aiormq.exceptions.AMQPError as err:
            raise f'Error sending message to broker {err}'
