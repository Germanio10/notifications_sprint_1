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
    async def find_one(self, collection_name: str, query: dict) -> dict | None:
        pass

    @abstractmethod
    async def update_one(self, collection_name: str, query: dict, update_data: dict):
        pass

    @abstractmethod
    async def update_notification_after_send(
        self, notification_id: uuid.UUID, cron: bool = False
    ) -> None:
        pass

    @abstractmethod
    async def check_users_settings(
        self, users_ids: list[uuid.UUID], type: str
    ) -> list[uuid.UUID, None]:
        pass

    @abstractmethod
    async def find_notification(self, notification_id: uuid.UUID) -> dict | None:
        pass

    @abstractmethod
    async def find_template(self, template_id: uuid.UUID) -> dict | None:
        pass


db: AbstractRepository | None = None


async def get_db() -> AbstractRepository:
    return db
