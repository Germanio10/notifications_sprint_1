import os

import backoff
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient


load_dotenv()


def connect_mongo(host: str, port: int):
    print("Connecting to MongoDB...")
    mongo_client = AsyncIOMotorClient(f"mongodb://{host}:{port}")
    yield mongo_client
    mongo_client.close()


if __name__ == "__main__":
    mongo_host = os.getenv("MONGO_HOST")
    mongo_port = int(os.getenv("MONGO_PORT"))
    connect_mongo(mongo_host, mongo_port)
