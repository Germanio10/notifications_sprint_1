import uuid

from core.config import settings
from core.logger import logger
from db.abstract_repository import AbstractRepository
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import Collection
from pymongo.database import Database


class MongoDB(AbstractRepository):
    def __init__(self, mongo_client: AsyncIOMotorClient) -> None:
        self.mongo_client = mongo_client

    async def close(self) -> None:
        if self.mongo_client:
            self.mongo_client.close()
            logger.info('Disconnected from MongoDB.')

    async def get_database(self) -> Database:
        return self.mongo_client[settings.mongo_db]

    async def get_collection(self, collection_name: str) -> Collection:
        database = await self.get_database()
        return database[collection_name]

    async def find_all(self, collection_name: str, query: dict) -> list[dict]:
        collection = await self.get_collection(collection_name)
        return await collection.find(query).to_list(length=None)

    async def find_one(self, collection_name: str, query: dict) -> dict | None:
        collection = await self.get_collection(collection_name)
        return await collection.find_one(query)

    async def check_users_settings(
        self, users_ids: list[uuid.UUID], type: str
    ) -> list[uuid.UUID, None]:
        query = {
            'type': type,
            'enabled': True,
            'user_id': {'$in': users_ids},
        }
        projection = {'user_id': 1}
        user_settings = await self.get_collection('notification_user_settings')
        result = await user_settings.find(query, projection).to_list(length=None)
        users_ids = [doc['user_id'] for doc in result]
        return users_ids
