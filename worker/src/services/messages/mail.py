import uuid

from core.logger import logger
from jinja2 import Template as TemplateJinja
from models.message import EmailModel, MailMessageError
from models.notification import Notification
from models.templates import Template
from services.fake_services.content_data_gen import Content, ContentFilmService
from services.fake_services.email_data_gen import EmailDataGenerator
from services.messages.abstract_message import AbstractMessage
from services.sender.abstract_sender import AbstractSender


class MailMessage(AbstractMessage):
    def __init__(self, email_sender: AbstractSender):
        self.email_sender = email_sender
        self.user_data = EmailDataGenerator()
        self.content_data = ContentFilmService()

    async def send(
        self, notification: Notification, users_ids: list[uuid.UUID], template: Template = None
    ) -> Notification:
        for user_id in users_ids:
            user = await self.user_data.generate_email_data(user_id)
            content: Content = await self.content_data.get_content(notification)

            jinja_subject = TemplateJinja(content.subject)
            jinja_body = TemplateJinja(content.text)

            mail = EmailModel(
                to_email=user.email,
                subject=jinja_subject.render({'subject': f'{content.subject}'}),
                body=jinja_body.render(
                    {
                        'name': user.name,
                        'content': (
                            notification.content_data if notification.content_data else content.film
                        ),
                        'content_id': notification.content_id if notification.content_id else '',
                    }
                ),
            )
            try:
                await self.email_sender.send(mail)
                logger.info(
                    f'Уведомление "{notification.notification_id}" успешно отправлено пользователю {user_id}'
                )
            except MailMessageError as er:
                logger.info(
                    f'Ошибка: {er} при отправке уведомления "{notification.notification_id}"'
                )
                return
        return notification
