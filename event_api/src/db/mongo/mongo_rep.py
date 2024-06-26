from core.config import settings
from core.logger import logger
from db.abstract_repository import AbstractRepository
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument
from pymongo.collection import Collection, InsertOneResult, UpdateResult
from pymongo.errors import DuplicateKeyError


class MongoDB(AbstractRepository):
    def __init__(self, db_client: AsyncIOMotorClient) -> None:
        self._mongo_client: AsyncIOMotorClient = db_client
        self.database = self._mongo_client[settings.mongo_db]

    async def get_collection(self, collection_name: str) -> Collection:
        return self.database[collection_name]

    async def save(self, collection_name: str, document: dict) -> InsertOneResult | None:
        collection = await self.get_collection(collection_name)
        try:
            result: InsertOneResult = await collection.insert_one(document)
            return result.inserted_id
        except DuplicateKeyError as err:
            logger.info(err)

    async def find_one(self, collection_name: str, query: dict) -> dict | None:
        collection = await self.get_collection(collection_name)
        try:
            return await collection.find_one(query)  # type: ignore[no-any-return]
        except Exception as er:
            logger.exception(f'Error when searching for an entry in the {collection_name}: {er}')

    async def update_one(
        self, collection_name: str, query: dict, update_data: dict
    ) -> ReturnDocument:
        collection = await self.get_collection(collection_name)
        update_result: UpdateResult = await collection.find_one_and_update(
            query,
            {'$set': update_data},
            return_document=ReturnDocument.AFTER,
        )
        return update_result

    async def find(self, collection_name: str, query: dict, include_fields: dict) -> list:
        collection = await self.get_collection(collection_name)
        cursor = collection.find(query, include_fields)
        return await cursor.to_list(length=100)
