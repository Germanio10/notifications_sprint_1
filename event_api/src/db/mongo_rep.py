import logging
from functools import lru_cache
from db.abstract import AbstractDB
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError
from core.config import settings

logger = logging.getLogger(__name__)


class MongoDB(AbstractDB):
    def __init__(self,):
        self._mongo_client = AsyncIOMotorClient(f"mongodb://{settings.mongo.host}:{settings.mongo.port}")
        self._database = self._mongo_client['NOTY']

    async def get_collection(self, collection_name: str):
        return self._database[collection_name]

    async def save(self, collection_name: str, document: dict):
        collection = await self.get_collection(collection_name)
        try:
            result = await collection.insert_one(document)
            return result.inserted_id
        except DuplicateKeyError as err:
            logger.info(err)

    async def find_one(self, collection_name: str, query: dict):
        collection = await self.get_collection(collection_name)
        try:
            return await collection.find_one(query)
        except Exception as err:
            logger.exception(f'Error when searching for an entry in the {collection_name}: {err}')

    async def update_one(self, collection_name: str, query: dict, update_data: dict):
        collection = await self.get_collection(collection_name)
        update_result = await collection.find_one_and_update(
            query,
            {'$set': update_data},
            return_document=ReturnDocument.AFTER
        )
        return update_result


@lru_cache()
def get_db() -> AbstractDB:
    return MongoDB()
