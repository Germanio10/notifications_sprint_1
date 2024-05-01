import datetime
import uuid

from pydantic import BaseModel


class ResponseNotification(BaseModel):
    event_type: str | None
    type: str
    content_id: uuid.UUID | None
    content_data: str
    template_id: uuid.UUID | None
    users_ids: list[uuid.UUID]
    scheduled: bool
    cron: str | None
    scheduled_timestamp: int | None
    notification_id: uuid.UUID
    time_create: datetime.datetime
    status: str
    last_time_update: datetime.datetime
    last_time_send: datetime.datetime | None


class ResponseTemplate(BaseModel):
    template_id: uuid.UUID
    event_type: str | None
    type: str
    subject: str | None
    content_data: str
