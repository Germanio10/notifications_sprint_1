import smtplib
from email.mime.text import MIMEText
from core.logger import logger
from models.message import EmailModel
from services.sender.abstract_sender import AbstractSender


class MailhogSender(AbstractSender):
    def __init__(self, smtp_host: str, smtp_port: int, from_email: str) -> None:
        self.mailhog_host = smtp_host
        self.mailhog_port = smtp_port
        self.from_email = from_email

    async def send(self, msg: EmailModel) -> None:
        message = MIMEText(msg.body)
        message['Subject'] = msg.subject
        message['From'] = self.from_email
        message['To'] = msg.to_email

        try:
            with smtplib.SMTP(self.mailhog_host, self.mailhog_port) as smtp:
                smtp.send_message(message)
            logger.info(f'The email message was sent to: {msg.to_email}')
        except Exception as e:
            logger.error(f'Failed to send email: {e}')
