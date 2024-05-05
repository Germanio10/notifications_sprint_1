from contextlib import asynccontextmanager

import uvicorn
from api.v1 import events
from async_fastapi_jwt_auth import AuthJWT
from core.config import JWTSettings, settings
from db.mongo import mongo_storage
from db.rabbit import rabbit_storage
from fastapi import FastAPI
from ws import channels


@asynccontextmanager
async def lifespan(app: FastAPI):
    await mongo_storage.on_startup(settings.mongo_uri)
    await rabbit_storage.on_startup(settings.rabbit_uri)

    yield

    await mongo_storage.on_shutdown()
    await rabbit_storage.on_shutdown()


@AuthJWT.load_config
def get_config():
    return JWTSettings()


app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    debug=settings.debug,
    lifespan=lifespan,
)

app.include_router(events.events_router, prefix='/api/v1/notifications', tags=['notifications'])
app.include_router(channels.ws_router, prefix='/ws', tags=['ws'])


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
