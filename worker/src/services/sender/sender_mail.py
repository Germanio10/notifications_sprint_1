from core.config import settings
from services.sender.abstract_sender import AbstractSender
from services.sender.email_mailgun import MailgunSender
from services.sender.email_print import PrintEmailSender
from services.sender.email_sendgrid import SendGridEmailSender
from services.sender.mailhog_sender import MailhogSender


async def get_sender(sender_name: str) -> AbstractSender:
    match sender_name:
        case 'mailgun':
            return MailgunSender(
                settings.mailgun_api_key, settings.mailgun_domain, settings.mailgun_from_email
            )
        case 'sendgrid':
            return SendGridEmailSender(settings.sendgrid_api_key, settings.sendgrid_from_email)
        case 'print':
            return PrintEmailSender(settings.sendgrid_from_email)
        case 'mailhog':
            return MailhogSender(
                settings.smtp_host, settings.smtp_port, settings.sendgrid_from_email
                )
        case _:
            raise ValueError(f'Sender {sender_name} not found')
