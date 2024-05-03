import uuid

from pydantic import BaseModel


class QueueMessage(BaseModel):
    notification_id: uuid.UUID
    users_ids: list[uuid.UUID] | None = None


class QueueRemove(BaseModel):
    notification_id: uuid.UUID
