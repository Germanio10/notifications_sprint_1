import datetime
import enum
import uuid
from http import HTTPStatus

from fastapi import HTTPException
from pydantic import BaseModel, Field, model_validator


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


class Event(BaseModel):
    event_type: EventTypeEnum | None
    template_id: uuid.UUID | None
    users_ids: list[uuid.UUID] = Field(..., min_items=1)
    type: NotificationTypeEnum = NotificationTypeEnum.email
    content_id: uuid.UUID | None
    content_data: str | None
    scheduled: bool = False
    cron: str | None = None
    scheduled_timestamp: int | None = None

    @model_validator(mode='before')
    def validate_fields(cls, values):
        scheduled = values.get('scheduled')
        cron = values.get('cron')
        scheduled_timestamp = int(values.get('scheduled_timestamp'))
        event_type = values.get('event_type')
        content_id = values.get('content_id')
        content_data = values.get('content_data')
        template_id = values.get('template_id')
        if not event_type and not content_id:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Must be one of the fields content_id or event_type',
            )
        if event_type == EventTypeEnum.registered and not template_id:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='template_id must be specified if event_type is registered',
            )
        if event_type == EventTypeEnum.recommendations and not content_data:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='If event_type is recommendations, set the required specify content_data',
            )
        if event_type == EventTypeEnum.new_episode and not content_data:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='If event_type is recommendations, set the required specify content_data',
            )
        if event_type == EventTypeEnum.like_comment and not scheduled:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='If event_type is like_comment, set the required scheduled field to true',
            )
        if event_type == EventTypeEnum.like_comment and not content_id:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='If event_type is like_comment, set the required specify content_id',
            )
        if content_id and not content_data:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='If the content_id field is specified, the content_data field is required',
            )
        if scheduled:
            if not cron and not scheduled_timestamp or cron and scheduled_timestamp:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail='Must be one of the fields scheduled_timestamp or cron',
                )
            current_time = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
            if scheduled_timestamp and scheduled_timestamp < current_time:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail='The scheduled_timestamp must be greater than or equal to the current time',
                )
        return values


class Notification(Event):
    notification_id: uuid.UUID = Field(..., default_factory=uuid.uuid4)
    time_create: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
    status: NotificationStatusEnum = NotificationStatusEnum.not_sent
    last_time_update: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
    last_time_send: datetime.datetime | None = None


class NotificationUserSettings(BaseModel):
    user_id: uuid.UUID
    type: NotificationTypeEnum = NotificationTypeEnum.email
    enabled: bool = True


class NotificationError(Exception):
    pass


class QueueMessage(BaseModel):
    notification_id: uuid.UUID
    users_ids: list[uuid.UUID] = Field(..., min_items=1)


class WsMessage(BaseModel):
    type: str
    message: dict
