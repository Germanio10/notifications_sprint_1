import uuid
from abc import ABC, abstractmethod


class AbstractRepository(ABC):

    @abstractmethod
    async def close(self) -> None:
        pass

    @abstractmethod
    async def get_database(self):
        pass

    @abstractmethod
    async def get_collection(self, collection_name: str):
        pass

    @abstractmethod
    async def find_all(self, collection_name: str, query: dict) -> list[dict]:
        pass

    @abstractmethod
    async def find_one(self, collection_name: str, query: dict):
        pass

    @abstractmethod
    async def check_users_settings(
        self, users_ids: list[uuid.UUID], type: str
    ) -> list[uuid.UUID, None]:
        pass


db: AbstractRepository | None = None


async def get_db() -> AbstractRepository:
    return db
