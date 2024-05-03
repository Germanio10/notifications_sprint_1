import aiormq
from broker import rabbitmq
from core.logger import logger
from broker import abstract_broker

connection: aiormq.Connection | None = None
channel: aiormq.Channel | None = None


async def rabbit_conn(rabbit_uri) -> None:
    global connection
    global channel
    try:
        connection = await aiormq.connect(rabbit_uri)
        channel = await connection.channel()

        abstract_broker.broker = rabbitmq.RabbitBroker(connection, channel)

        logger.info('Connected to Rabbit successfully.')
    except Exception as er:
        logger.exception(f'Error connecting to Rabbit: {er}')
