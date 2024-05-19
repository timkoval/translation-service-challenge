import json
import google.generativeai as genai
from app.models.translation import Translation
from app.setup import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

async def get_translation(word: str, language: str) -> Translation:
    prompt = f'Translate a word "{word}" with Google Translate. Include multiple translations in {language}, multiple definitions in english, multiple synonyms in english and multiple examples in english given by Google Translate. Return a result in JSON in the following format {{ "translations": [list of translations], "definitions": [list of definitions], "synonyms": [list of synonyms], "examples": [list of examples]}}.'
    response = model.generate_content(prompt)
    result = '{' + response.text.rsplit('}')[0].split('{')[1] + '}'
    return Translation.model_validate_json(result)
