import logging

from pydantic import Field
from pydantic_settings import BaseSettings


class MongoSettings(BaseSettings):
    host: str = Field(validation_alias='MONGO_HOST', default='localhost')
    port: int = Field(validation_alias='MONGO_PORT', default=27017)


class Settings(BaseSettings):
    mongo: MongoSettings = MongoSettings()
    log_level: int | str = Field(validation_alias='LOG_LEVEL', default=logging.DEBUG)
    sentry_dsn: str = Field(validation_alias='SENTRY_DSN', default='')


settings = Settings()
