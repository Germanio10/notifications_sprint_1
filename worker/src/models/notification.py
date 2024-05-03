import datetime
import enum
import uuid

from pydantic import BaseModel


class EventTypeEnum(str, enum.Enum):
    registered = 'registered'
    recommendations = 'recommendations'
    new_episode = 'new_episode'
    like_comment = 'like_comment'


class NotificationTypeEnum(str, enum.Enum):
    email = 'email'
    web_socket = 'web_socket'


class NotificationStatusEnum(str, enum.Enum):
    shipped = 'shipped'
    not_sent = 'not_sent'


class Notification(BaseModel):
    notification_id: uuid.UUID
    event_type: EventTypeEnum | None
    type: NotificationTypeEnum = NotificationTypeEnum.email
    content_id: uuid.UUID | None
    content_data: str
    template_id: uuid.UUID | None
    users_ids: list[uuid.UUID]
    scheduled: bool = False
    cron: str | None
    scheduled_timestamp: int | None = None

    status: NotificationStatusEnum
    last_time_update: datetime.datetime
    last_time_send: datetime.datetime | None
