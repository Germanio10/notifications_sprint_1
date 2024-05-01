from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongo_uri: str = Field(validation_alias='MONGO_URI', default='mongodb://127.0.0.1:27017/')
    mongo_db: str = Field(validation_alias='MONGO_DB', default='notifications')

    rabbit_uri: str = Field(
        validation_alias='RABBIT_URI', default='amqp://admin:P@ssw0rd@127.0.0.1:5672/'
    )
    queue_instant: str = Field(validation_alias='QUEUE_INSTANT', default='instant.notification')
    queue_from_scheduler: str = Field('send_from_scheduler.notification')
    queue_remove_scheduled: str = Field('remove_scheduled.notification')

    sender: str = Field('print')

    sendgrid_api_key: str = ''
    sendgrid_from_email: str = ''

    mailgun_api_key: str = ''
    mailgun_domain: str = ''
    mailgun_from_email: str = ''


settings = Settings()
