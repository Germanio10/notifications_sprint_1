from core.logger import logger
from db import mongo
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError
from db import abstract_repository

mongo_client: AsyncIOMotorClient | None = None


async def mongo_conn(mongo_uri) -> None:
    global mongo_client
    try:
        mongo_client = AsyncIOMotorClient(
            mongo_uri,
            uuidRepresentation='standard',
        )
        abstract_repository.db = mongo.MongoDB(mongo_client)

        logger.info('Connected to MongoDB successfully.')
    except ServerSelectionTimeoutError as er:
        logger.exception(f'Error connecting to MongoDB: {er}')
    except Exception as er:
        logger.exception(f'Error connecting to MongoDB: {er}')


async def close_mongo_conn() -> None:
    if mongo_client:
        mongo_client.close()
        logger.info('Disconnected from MongoDB.')
