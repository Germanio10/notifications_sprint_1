from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    async def get_collection(self, collection_name: str):
        pass

    @abstractmethod
    async def save(self, collection_name: str, document: dict):
        pass

    @abstractmethod
    async def find_one(self, collection_name: str, query: dict):
        pass

    @abstractmethod
    async def update_one(self, collection_name: str, query: dict, update_data: dict):
        pass

    @abstractmethod
    async def find(self, collection_name: str, query: dict, include_fields: dict):
        pass


db: AbstractRepository | None = None


def get_db() -> AbstractRepository | None:
    return db
