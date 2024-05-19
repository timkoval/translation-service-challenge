from motor.motor_asyncio import AsyncIOMotorClient
import logging
from app.setup import MONGO_DB, MONGO_URL, MONGO_USER, MONGO_PASSWORD, MIN_CONNECTIONS_COUNT, MAX_CONNECTIONS_COUNT


db_client: AsyncIOMotorClient = None


async def get_db() -> AsyncIOMotorClient:
    db_name = MONGO_DB
    return db_client[db_name]


async def connect_and_init_db():
    global db_client
    try:
        db_client = AsyncIOMotorClient(
            MONGO_URL,
            username=MONGO_USER,
            password=MONGO_PASSWORD,
            maxPoolSize=MAX_CONNECTIONS_COUNT,
            minPoolSize=MIN_CONNECTIONS_COUNT,
            uuidRepresentation="standard",
        )
        logging.info('Connected to mongo.')
    except Exception as e:
        logging.exception(f'Could not connect to mongo: {e}')
        raise


async def close_db_connect():
    global db_client
    if db_client is None:
        logging.warning('Connection is None, nothing to close.')
        return
    db_client.close()
    db_client = None
    logging.info('Mongo connection closed.')
