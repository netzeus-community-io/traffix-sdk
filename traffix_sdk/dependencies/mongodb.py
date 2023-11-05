from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from traffix_sdk.config import settings


async def get_mongo_db(
    uri: str = settings.MONGODB_URI, db: str = settings.MONGODB_DATABASE
) -> AsyncIOMotorDatabase:
    """Gets a MongoDB database object to be used with database operations.

    Args:
        uri:        MongoDB URI
        db:         Name of database in MongoDB
    """
    client = AsyncIOMotorClient(str(uri))
    database = client[db]
    return database
