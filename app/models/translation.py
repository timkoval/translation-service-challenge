from enum import Enum
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class SortEnum(str, Enum):
    ASC = "asc"
    DESC = "desc"


class OptionalFields(str, Enum):
    DEFINITIONS = "definitions"
    SYNONYMS = "synonyms"
    EXAMPLES = "examples"


class Translation(BaseModel):
    translations: list[str]
    definitions: Optional[list[str]] = None
    synonyms: Optional[list[str]] = None
    examples: Optional[list[str]] = None


class TranslationFull(Translation):
    word: str
    language: Optional[str] = None


class TranslationDB(TranslationFull):
    id: UUID
    create_time: datetime
    update_time: datetime
