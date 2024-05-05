from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = Field(validation_alias='PROJECT_NAME_', default='notifications')
    debug: bool = Field(validation_alias='DEBUG_', default=True)

    mongo_uri: str = Field(validation_alias='MONGO_URI_', default='mongodb://127.0.0.1:27017/')
    mongo_db: str = Field(validation_alias='MONGO_DB_', default='notifications')

    rabbit_uri: str = Field(
        validation_alias='RABBIT_URI_', default='amqp://admin:P@ssw0rd@127.0.0.1:5672/'
    )
    queue_instant: str = Field(validation_alias='QUEUE_INSTANT_', default='instant.notification')
    queue_scheduled: str = Field(
        validation_alias='QUEUE_SCHEDULED_', default='scheduled.notification'
    )


settings = Settings()


class JWTSettings(BaseModel):
    authjwt_secret_key: str = "secret"
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_secure: bool = False
    authjwt_cookie_csrf_protect: bool = False
