from motor.motor_asyncio import AsyncIOMotorClient
import os
from uuid import UUID
import logging
import json
from datetime import datetime


class MongoHandler():
    def __init__(self, db_name: str, collection_name: str):
        self.__db_name = db_name
        self.__collection_name = collection_name
        self.__db_client = AsyncIOMotorClient(
            os.environ.get('TEST_MONGODB_URL')
        )

    async def get_translation(self, word: str):
        return await self.__db_client[self.__db_name][self.__collection_name]\
            .find_one({'word': word})

    async def insert_translation(self, translation: dict):
        await self.__db_client[self.__db_name][self.__collection_name]\
            .insert_one(translation)

    async def drop_database(self):
        await self.__db_client.drop_database(self.__db_name)

    def close_conn(self):
        self.__db_client.close()


class MongoClient():
    def __init__(self, db_name: str, collection_name: str):
        self.__db_handler = MongoHandler(db_name, collection_name)

    async def __aenter__(self):
        await self.__create_mock_data()
        return self.__db_handler

    async def __create_mock_data(self):
        with open('tests/mock_data/translation.json', 'r') as f:
            translation_json = json.load(f)
            for translation in translation_json:
                translation['create_time'] = datetime.strptime(
                    translation['create_time'], '%Y-%m-%d %H:%M:%S'
                )
                translation['update_time'] = datetime.strptime(
                    translation['update_time'], '%Y-%m-%d %H:%M:%S'
                )
                translation['_id'] = UUID(translation['_id'])
                await self.__db_handler.insert_translation(translation)

    async def __aexit__(
        self, exception_type,
        exception_value, exception_traceback
    ):
        if exception_type:
            logging.error(exception_value)

        await self.__db_handler.drop_database()
        self.__db_handler.close_conn()
        return False
