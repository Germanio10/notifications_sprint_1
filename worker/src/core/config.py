from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongo_uri: str = Field(validation_alias='MONGO_URI', default='mongodb://127.0.0.1:27017/')
    mongo_db: str = Field(validation_alias='MONGO_DB', default='notifications')

    rabbit_uri: str = Field(
        validation_alias='RABBIT_URI', default='amqp://admin:P@ssw0rd@127.0.0.1:5672/'
    )
    ws_uri: str = Field(validation_alias='WS_URI', default='ws://event_api:8000/ws/notifications')
    queue_instant: str = Field(validation_alias='QUEUE_INSTANT', default='instant.notification')
    queue_from_scheduler: str = Field('send_from_scheduler.notification')
    queue_remove_scheduled: str = Field('remove_scheduled.notification')

    sender: str = Field('mailhog')

    sendgrid_api_key: str = ''
    sendgrid_from_email: str = 'noname@mail.ru'

    mailgun_api_key: str = ''
    mailgun_domain: str = ''
    mailgun_from_email: str = ''
    
    smtp_host: str = Field(validation_alias='HOG_HOST',  default='mailhog')
    smtp_port: int = Field(validation_alias='HOG_PORT',  default=1025)


settings = Settings()
