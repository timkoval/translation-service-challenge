from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query, status
from fastapi_pagination import Page, paginate
from app.gemini_utils import get_translation as get_gemini_translation
from app.db import get_db, AsyncIOMotorClient
import logging

from app.models.translation import OptionalFields, SortEnum, Translation, TranslationFull
from app.repositories.translation import delete_translation, get_all_translations, get_translation, create_translation

router = APIRouter(prefix="/translation", tags=["translation"])

@router.get("/words", response_model_exclude_none=True)
async def get_words(filter: Optional[str]=None, sort: SortEnum=SortEnum.ASC, fields: Annotated[list[OptionalFields] | None, Query()] = None, db: AsyncIOMotorClient = Depends(get_db)) -> Page[TranslationFull]:
    if fields is None:
        fields = []
    translations = await get_all_translations(db, filter, sort, fields)
    return paginate(translations)

@router.get("/{word}")
async def translate_word(word: str, language: str, db: AsyncIOMotorClient = Depends(get_db)) -> Translation:
    logging.info(f"WORD TO TRANSLATE: {word}")
    translation = await get_translation(db, word, language)
    if not translation:
        new_translation = await get_gemini_translation(word, language)
        await create_translation(db, word, language, new_translation)
        return new_translation
    return translation

@router.delete("/{word}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_word(word: str, language: str, db: AsyncIOMotorClient = Depends(get_db)):
    logging.info(f"WORD TO TRANSLATE: {word}")
    translation = await get_translation(db, word, language)
    if translation:
        await delete_translation(db, word, language)

