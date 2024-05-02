from http import HTTPStatus

import backoff
from core.logger import logger
from models.message import EmailModel
from python_http_client.exceptions import BadRequestsError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from services.sender.abstract_sender import AbstractSender, SenderError


class SendGridEmailSender(AbstractSender):
    def __init__(self, api_key: str, from_email: str) -> None:
        self.sg_client = SendGridAPIClient(api_key)
        self.from_email = from_email

    @backoff.on_exception(backoff.expo, (SenderError, BadRequestsError))
    async def send(self, msg: EmailModel) -> None:
        message = Mail(
            from_email=self.from_email,
            to_emails=msg.to_email,
            subject=msg.subject,
            html_content=msg.body,
        )

        response = await self.sg_client.send(message)

        if response.status_code != HTTPStatus.OK:
            logger.error(f'Failed to send email: {response.body}')
            raise SenderError(f'Failed to send email: {response.body}')

        logger.info(f'Send email to {msg.to_email}')
