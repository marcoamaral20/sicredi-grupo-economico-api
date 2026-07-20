from beanie import init_beanie
from pymongo import AsyncMongoClient

from app.core.config import settings
from app.core.logging import logger
from app.models.associate import Associate


async def init_database():
    logger.info("Initializing MongoDB connection...")

    client = AsyncMongoClient(settings.mongo_uri)
    database = client[settings.database_name]

    await init_beanie(database=database, document_models=[Associate])

    logger.info("MongoDB initialized successfully.")
