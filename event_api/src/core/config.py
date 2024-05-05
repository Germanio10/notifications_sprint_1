from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = Field(validation_alias='PROJECT_NAME', default='notifications')
    debug: bool = Field(validation_alias='DEBUG', default=True)

    mongo_uri: str = Field(validation_alias='MONGO_URI', default='mongodb://127.0.0.1:27017/')
    mongo_db: str = Field(validation_alias='MONGO_DB', default='notifications')

    rabbit_uri: str = Field(
        validation_alias='RABBIT_URI', default='amqp://admin:P@ssw0rd@127.0.0.1:5672/'
    )
    queue_instant: str = Field(validation_alias='QUEUE_INSTANT', default='instant.notification')
    queue_scheduled: str = Field(
        validation_alias='QUEUE_SCHEDULED', default='scheduled.notification'
    )


settings = Settings()


class JWTSettings(BaseModel):
    authjwt_secret_key: str = "secret"
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_secure: bool = False
    authjwt_cookie_csrf_protect: bool = False
