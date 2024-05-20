from typing import Optional
from uuid import uuid4, UUID
from datetime import datetime
import logging
from pymongo import ReturnDocument

from app.db import AsyncIOMotorClient
from app.models.translation import OptionalFields, SortEnum, Translation, TranslationDB
from app.setup import MONGO_DB


__db_name = MONGO_DB
__db_collection = "translation"


async def create_translation(
    conn: AsyncIOMotorClient, word: str, language: str, translation: Translation
) -> TranslationDB:
    new_translation = TranslationDB(
        **translation.model_dump(),
        id=uuid4(),
        word=word,
        language=language,
        create_time=datetime.utcnow(),
        update_time=datetime.utcnow(),
    )
    logging.info(f"Inserting translation {word} in {language} into db...")
    await conn[__db_name][__db_collection].insert_one(new_translation.model_dump())
    logging.info(f"Sample translation {word} in {language} has been inserted into db")
    return new_translation


async def get_translation(
    conn: AsyncIOMotorClient,
    word: str,
    language: str,
) -> TranslationDB | None:
    logging.info(f"Getting translation {word} in {language}...")
    translation = await conn[__db_name][__db_collection].find_one(
        {
            "$and": [
                {"word": word},
                {"language": language},
            ]
        },
    )
    if not translation:
        logging.info(f"Translation of {word} in {language} is None")
    return translation


async def get_all_translations(
    conn: AsyncIOMotorClient,
    filter: Optional[str],
    sort: SortEnum,
    fields: list[OptionalFields],
) -> list[TranslationDB]:
    sort_int = 1
    if sort == SortEnum.DESC:
        sort_int = -1

    projection_map = {
        key: 1 if key in fields else 0 for key in TranslationDB.model_fields.keys()
    }
    projection_map["_id"] = 0
    projection_map["word"] = 1
    projection_map["translations"] = 1
    projection_map = {k: v for k, v in projection_map.items() if k != "_id" and v == 0}

    if filter:
        translations_cursor = (
            conn[__db_name][__db_collection]
            .find({"word": {"$regex": filter}}, projection_map)
            .sort({"word": sort_int})
        )
    else:
        translations_cursor = (
            conn[__db_name][__db_collection]
            .find({}, projection_map)
            .sort({"word": sort_int})
        )

    return await translations_cursor.to_list(None)


async def delete_translation(
    conn: AsyncIOMotorClient,
    word: str,
    language: str,
):
    logging.info(f"Deleting translation of {word} in {language}...")

    result = await conn[__db_name][__db_collection].delete_one(
        {
            "$and": [
                {"word": word},
                {"language": language},
            ]
        },
    )

    if result.deleted_count == 0:
        logging.error(f"Translation of word {word} in {language} not exist")
    else:
        logging.info(f"Translation of {word} in {language} deleted")
