import logging
import uuid

from core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger(__name__)

mongo_client: AsyncIOMotorClient | None = None


async def create_database() -> None:
    global mongo_client
    try:
        mongo_client = AsyncIOMotorClient(f"mongodb://{settings.mongo.host}:{settings.mongo.port}",
                                          uuidRepresentation='standard'
)
        db = mongo_client['NOTY']

        if 'notifications' not in await db.list_collection_names():
            collection = db['notifications']
            await collection.create_index([('notification_id', 1), ('content_id', 1)], unique=True)

        if 'templates' not in await db.list_collection_names():
            collection = db['templates']
            await collection.create_index([('template_id', 1)], unique=True)

            template_id = uuid.UUID('3fa85f64-5717-4562-b3fc-2c963f66afa6')
            template = {
                'template_id': template_id,
                'event_type': 'registered',
                'notification_type': 'email',
                'subject': 'Поздравляем с регистрацией!',
                'content_data': """
                                            <!DOCTYPE html>
                                            <html lang="ru">
                                            <head><title>Добро пожаловать!</title></head>
                                            <body>
                                            <h1>Привет {{ name }}!</h1>
                                            <p> {{ content }} </p>
                                            </body>
                                            </html>
                                            """,
            }
            await collection.insert_one(template)

        logger.info('Connected to Mongo')
    except Exception as e:
        logger.exception(f"Error connecting to MongoDB: {e}")


async def close_connection() -> None:
    global mongo_client
    if mongo_client:
        mongo_client.close()
