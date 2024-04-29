import orjson
from pydantic import BaseModel


def orjson_dumps(value, *, default):
    return orjson.dumps(value, default=default).decode()


class BaseOrjsonModel(BaseModel):

    class Config:
        model_load = orjson.loads
        model_dump = orjson_dumps
