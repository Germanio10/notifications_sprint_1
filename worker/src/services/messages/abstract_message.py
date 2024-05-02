from abc import ABC, abstractmethod
import uuid

from models.notification import Notification
from models.templates import Template


class AbstractMessage(ABC):
    @abstractmethod
    async def send(
        self, notification: Notification, users_ids: list[uuid.UUID], template: Template = None
    ) -> Notification:
        pass
