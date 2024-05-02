from core.logger import logger
from models.message import EmailModel
from services.sender.abstract_sender import AbstractSender


class PrintEmailSender(AbstractSender):
    def __init__(self, from_email: str) -> None:
        self.from_email = from_email

    async def send(self, msg: EmailModel) -> None:
        message = {
            'from_email': self.from_email,
            'to_emails': msg.to_email,
            'subject': msg.subject,
            'html_content': msg.body,
        }

        logger.info(f'The email message: {message} was sent to: {msg.to_email}')
