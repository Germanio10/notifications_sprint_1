import datetime
import enum
import uuid

from cron_validator import CronValidator
from fastapi import HTTPException, status
from models.base import BaseOrjsonModel
from pydantic import Field, root_validator


class EventTypeEnum(str, enum.Enum):

    registered = 'registered'
    like_comment = 'like_comment'


class NotificationTypeEnum(str, enum.Enum):

    email = 'email'


class NotificationStatusEnum(str, enum.Enum):

    shipped = 'отправлено'
    not_sent = 'не отправлено'


class Event(BaseOrjsonModel):
    event_type: EventTypeEnum | None
    template_id: uuid.UUID | None = None
    users_ids: list[uuid.UUID] = Field(..., min_items=1)
    content_id: uuid.UUID | None
    content_data: str | None
    scheduled: bool = False
    cron: str | None
    scheduled_timestamp: int | None = None

    @root_validator(skip_on_failure=True)
    def validate_fields(cls, values):
        """Валидатор события."""
        scheduled = values.get('scheduled')
        cron = values.get('cron')
        scheduled_timestamp = int(values.get('scheduled_timestamp'))
        event_type = values.get('event_type')
        content_id = values.get('content_id')
        content_data = values.get('content_data')
        template_id = values.get('template_id')
        if not event_type and not content_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Must be one of the fields content_id or event_type',
            )
        if event_type == 'registered' and not template_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='template_id must be specified if event_type is registered',
            )
        if event_type == 'like_comment' and not scheduled:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='If event_type is like_comment, set the required scheduled field to true',
            )
        if event_type == 'like_comment' and not content_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='If event_type is like_comment, set the required specify content_id',
            )
        if content_id and not content_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='If the content_id field is specified, the content_data field is required',
            )
        if scheduled:
            if not cron and not scheduled_timestamp or cron and scheduled_timestamp:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Must be one of the fields scheduled_timestamp or cron',
                )
            current_time = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
            if scheduled_timestamp and scheduled_timestamp < current_time:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='The scheduled_timestamp must be greater than or equal to the current time',
                )
            if cron:
                try:
                    CronValidator.parse(cron)
                except ValueError as err:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f'Invalid field cron: {err}',
                    ) from err
        return values


class Notification(Event):
    notification_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    notification_type: NotificationTypeEnum = NotificationTypeEnum.email
    notification_time_create: datetime.datetime = Field(default=datetime.datetime.now(datetime.timezone.utc))
    notification_status: NotificationStatusEnum = Field(default=NotificationStatusEnum.not_sent)
    last_update: datetime.datetime = Field(default=datetime.datetime.now(datetime.timezone.utc))
    last_notification_send: datetime.datetime | None = None


class NotificationUserSettings(BaseOrjsonModel):

    user_id: uuid.UUID
    notification_type: NotificationTypeEnum = NotificationTypeEnum.email
    enabled: bool = Field(default=True)


class NotificationError(Exception):
    pass


class QueueMessage(BaseOrjsonModel):
    notification_id: uuid.UUID
    users_ids: list[uuid.UUID] = Field(..., min_items=1)
