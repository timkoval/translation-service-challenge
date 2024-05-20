import pytest


@pytest.mark.asyncio
# @pytest.mark.parametrize(
#     "word, language, expected_status",
#     [
#         ('check', 'spanish', 201),
#         ('check', None, 400),
#         (None, None, 404),
#     ]
# )
async def test_get_all_translations(
    test_client
):
    resp = test_client.get(
        '/translation/words',
    )
    assert resp.status_code == 200

    if 200 == resp.status_code:
        assert 'items' in resp.json()
        assert 'tatal' in resp.json()
        assert 'page' in resp.json()
        assert 'size' in resp.json()
        assert 'pages' in resp.json()
        assert len(resp.json()["items"]) == 2
