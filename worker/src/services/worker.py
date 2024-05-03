import json
import uuid

from broker.abstract_broker import AbstractBroker
from core.config import settings
from core.logger import logger
from db.abstract_repository import AbstractRepository
from models.broker_message import QueueMessage, QueueRemove
from models.message import WsMessage
from models.notification import Notification, NotificationTypeEnum
from models.templates import Template
from models.worker_cron import CronModel
from services.messages.abstract_message import AbstractMessage
from websocket import create_connection


class Worker:
    def __init__(
        self,
        db: AbstractRepository,
        broker: AbstractBroker,
        message: AbstractMessage,
    ) -> None:
        self.db = db
        self.broker = broker
        self.message = message
        self.ws_url = settings.ws_uri

    async def on_message(self, message: dict) -> None:
        msg = QueueMessage(**json.loads(message.body))
        notification = await self.get_notification(msg.notification_id)
        if notification.type == NotificationTypeEnum.email:
            await self.send_email(notification, msg.users_ids)
        if notification.type == NotificationTypeEnum.web_socket:
            await self.send_websocket(notification, msg.users_ids)

    async def on_scheduler(self, message: dict) -> None:
        scheduler_msg = QueueMessage(**json.loads(message.body))

        notification = await self.get_notification(scheduler_msg.notification_id)
        if notification.cron:
            await self.cron(notification, scheduler_msg.users_ids)
        if notification.scheduled_timestamp:
            await self.timestamp(notification, scheduler_msg.users_ids)

    async def get_notification(self, notification_id: uuid.UUID) -> Notification | None:
        if notification := await self.db.find_notification(notification_id):
            del notification['_id']
            return Notification.model_validate(notification)

    async def timestamp(
        self, notification: Notification, ids_users_with_same_timezone: list[uuid.UUID]
    ) -> None:
        if notification.type == NotificationTypeEnum.email:
            await self.send_email(notification, ids_users_with_same_timezone)

    async def cron(
        self, notification: Notification, ids_users_with_same_timezone: list[uuid.UUID]
    ) -> None:
        cron = CronModel(
            last_time_update=notification.last_time_send,
            last_time_send=notification.last_time_send,
        )
        if cron.time_difference < cron.time_of_deletion:
            if cron.last_time_send is None or cron.last_time_send < cron.last_time_update:
                if notification.type == NotificationTypeEnum.email:
                    await self.send_email(notification, ids_users_with_same_timezone)
            return
        logger.info(
            f'Удаляю cron для уведомления: "{notification.notification_id}" прошло более суток с момента последнего обновления сообщения.'
        )
        await self.delete_task(notification)
        await self.db.update_notification_after_send(notification.notification_id, cron=True)

    async def delete_task(self, notification: Notification) -> None:
        await self.broker.send_to_broker(
            body=QueueRemove(**notification.model_dump()).model_dump_json().encode()
        )

    async def get_template(self, template_id: uuid.UUID) -> Template | None:
        if template := await self.db.find_template(template_id):
            del template['_id']
            return Template.model_validate(template)

    async def send_email(
        self, notification: Notification, ids_users_with_same_timezone: list[uuid.UUID]
    ) -> None:
        if users_ids := await self.db.check_users_settings(
            ids_users_with_same_timezone, notification.type
        ):
            template = await self.get_template(notification.template_id)
            if await self.message.send(notification, users_ids, template):
                await self.db.update_notification_after_send(notification.notification_id)
            return
        logger.info(
            f'У пользователей "{ids_users_with_same_timezone}" отключены email уведомления.'
        )

    async def send_websocket(
        self,
        notification: Notification,
        ids_users_with_same_timezone: list[uuid.UUID],
    ):
        event = WsMessage(
            type='worker',
            message={
                'users_ids': [str(id) for id in ids_users_with_same_timezone],
                'content_data': notification.content_data,
            },
        )
        ws = create_connection(self.ws_url)
        ws.send(json.dumps(event.model_dump()))

        await self.db.update_notification_after_send(notification.notification_id)
