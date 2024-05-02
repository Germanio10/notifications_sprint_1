from contextlib import asynccontextmanager

import uvicorn
from api.v1 import events
from core.config import settings
from db.mongo import mongo_storage
from db.rabbit import rabbit_storage
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    await mongo_storage.on_startup(settings.mongo_uri)
    await rabbit_storage.on_startup(settings.rabbit_uri)
    yield
    await mongo_storage.on_shutdown()
    await rabbit_storage.on_shutdown()


app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    debug=settings.debug,
    lifespan=lifespan,
)

app.include_router(events.events_router, prefix='/api/v1/notifications', tags=['notifications'])


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
