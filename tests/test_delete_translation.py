import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "word, language, expected_status",
    [
        ("challenge", "spanish", 204),
        ("water", "spanish", 204),
        (None, None, 404),
    ]
)
async def test_delete_translation(
    test_client, mongo_client, word: str, language: str, expected_status: int,
):

    path = f'/translation/{word}?language={language}'

    resp = test_client.delete(
        path,
    )
    assert resp.status_code == expected_status

    if 204 == resp.status_code:
        resource_db = await mongo_client.get_translation(word, language)
        assert resource_db is None
