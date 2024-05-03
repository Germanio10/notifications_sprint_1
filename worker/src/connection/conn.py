from broker.abstract_broker import AbstractBroker, get_broker
from connection import mongo_conn, rabbit_conn
from core.config import settings
from db.abstract_repository import AbstractRepository, get_db


async def connection() -> tuple[AbstractRepository, AbstractBroker]:
    await mongo_conn.mongo_conn(settings.mongo_uri)
    await rabbit_conn.rabbit_conn(settings.rabbit_uri)
    db = await get_db()
    broker = await get_broker()
    return db, broker
