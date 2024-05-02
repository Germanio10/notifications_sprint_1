import aiormq
from broker import abstract_broker, rabbit_broker
from core.logger import logger

connection: aiormq.Connection | None = None
channel: aiormq.Channel | None = None


async def on_startup(rabbit_uri: str) -> None:
    global connection
    global channel
    try:
        connection = await aiormq.connect(rabbit_uri)
        channel = await connection.channel()

        abstract_broker.broker = rabbit_broker.RabbitBroker(connection, channel)

        logger.info('Connected to Rabbit successfully.')
    except Exception as er:
        logger.exception(f'Error connecting to Rabbit: {er}')


async def on_shutdown() -> None:
    if channel:
        await channel.close()
    if connection:
        await connection.close()
    logger.info('Disconnected from Rabbit.')
