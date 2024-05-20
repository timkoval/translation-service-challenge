import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "word, language, expected_status",
    [
        ('check', 'spanish', 201),
        ('check', None, 400),
        (None, None, 404),
    ]
)
async def test_create_translation(
    test_client, mongo_client, word: str, language: str, expected_status: int
):
    resp = test_client.get(
        f'/translation/{word}?language={language}',
    )
    assert resp.status_code == expected_status

    if 201 == expected_status:
        assert 'translations' in resp.json()
        translation_db = await mongo_client.get_translation(word)
        assert translation_db.get('word') == word
        assert translation_db.get('language') == language
