import datetime
import uuid
from functools import lru_cache
from http import HTTPStatus

from broker.abstract_broker import AbstractBroker, get_broker
from core.config import settings
from db.abstract_repository import AbstractRepository, get_db
from fastapi import Depends, HTTPException
from models.notifications import (
    Event,
    Notification,
    NotificationUserSettings,
    QueueMessage,
    UserNotification,
)
from models.templates import Template


class Notifications:
    def __init__(self, db: AbstractRepository, broker: AbstractBroker) -> None:
        self.db = db
        self.broker = broker

    async def create_notification(self, event: Event) -> Notification:
        if event.content_id:
            if existing_doc := await self.find_and_update_content(
                event.content_id, event.content_data
            ):
                return existing_doc
        notification = Notification(**event.model_dump())
        await self.save_user_settings(notification)
        await self.db.save('notifications', notification.model_dump())
        if notification.scheduled:
            await self.broker.send_to_broker(
                body=QueueMessage(**notification.model_dump()).model_dump_json().encode(),
                routing_key=settings.queue_scheduled,
            )
            return notification.model_dump()
        await self.broker.send_to_broker(
            body=QueueMessage(**notification.model_dump()).model_dump_json().encode(),
            routing_key=settings.queue_instant,
        )
        return notification.model_dump()

    async def save_user_settings(self, notification: Notification) -> None:
        for user_id in notification.users_ids:
            user = NotificationUserSettings(user_id=user_id, **notification.model_dump())
            query = {'user_id': user.user_id, 'type': user.type}
            if await self.db.find_one('notification_user_settings', query):
                continue
            await self.db.save('notification_user_settings', user.model_dump())

    async def find_and_update_content(self, content_id, content_data):
        query = {'content_id': content_id}
        if existing_content := await self.db.find_one('notifications', query):
            res = await self.db.update_one(
                'notifications',
                existing_content,
                {
                    'content_data': content_data,
                    'last_time_update': datetime.datetime.now(datetime.timezone.utc),
                },
            )
            del res['_id']
            return res
        return existing_content

    async def create_template(self, template: Template) -> Template:
        template = Template(**template.model_dump())

        if await self.db.find_one('templates', {'template_id': template.template_id}):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Template is already exists',
            )
        if await self.db.save('templates', template.model_dump()):
            return template.model_dump()

    async def get_user_notifications(self, user_id: str) -> list[UserNotification]:
        notifications = await self.db.find(
            'notifications',
            {"users_ids": uuid.UUID(user_id)},
            {
                'event_type': 1,
                'content_data': 1,
                '_id': 0,
            },
        )
        print(notifications)
        return [UserNotification(**notify) for notify in notifications]


@lru_cache
def get_notification_service(
    db: AbstractRepository = Depends(get_db),
    broker: AbstractBroker = Depends(get_broker),
) -> Notifications:
    return Notifications(db, broker)
