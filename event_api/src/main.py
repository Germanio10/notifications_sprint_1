from contextlib import asynccontextmanager

import uvicorn
from core.logger import LOGGING
from core.config import settings
from db import mongo_storage
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    await mongo_storage.create_database()
    yield
    await mongo_storage.close_connection()


app = FastAPI(
    title='Notification сервис',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    description="Сервис, предоставляющий API для отправки уведомлений на почту пользователями или на сайт",
    version="1.0.0",
    lifespan=lifespan,
)


if __name__ == '__main__':

    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=settings.log_level,
    )
