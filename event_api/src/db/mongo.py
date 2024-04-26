from motor.motor_asyncio import AsyncIOMotorClient

mongo: AsyncIOMotorClient | None = None


def get_mongo() -> AsyncIOMotorClient:
    return mongo
