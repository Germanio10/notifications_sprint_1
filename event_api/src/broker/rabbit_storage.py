import aiormq
from db.mongo_storage import logger

connection: aiormq.Connection | None = None
channel: aiormq.Channel | None = None


async def init_broker():
    global connection, channel
    try:
        connection = await aiormq.connect('amqp://guest:guest@127.0.0.1:5672/')
        channel = await connection.channel()

        logger.info("Connected to RabbitMQ")
    except Exception as err:
        logger.exception(f"Error connecting to RabbitMQ: {err}")


async def close_connection():
    if channel:
        await channel.close()
    if connection:
        await connection.close()
    logger.info("disconnected from RabbitMQ")
