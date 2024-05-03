import uuid

from pydantic import Field, BaseModel


class ScheduledNotification(BaseModel):
    notification_id: uuid.UUID
    users_ids: list[uuid.UUID] = Field(..., min_items=1)
    cron: str | None
    scheduled_timestamp: int | None = None


class ScheduledByDate(BaseModel):
    notification_id: uuid.UUID
    users_ids: list[uuid.UUID]
    timezone: str
    scheduled_timestamp: int


class ScheduledByCron(BaseModel):
    notification_id: uuid.UUID
    users_ids: list[uuid.UUID]
    timezone: str
    cron: str


class QueueMessage(BaseModel):
    notification_id: uuid.UUID
    users_ids: list[uuid.UUID] = None


class QueueRemove(BaseModel):
    notification_id: uuid.UUID
