import datetime as dt
from unittest.mock import patch


from biscuit.predict import core


def build_article_fixture(item_id="1"):
    return {
        "item_id": item_id,
        "resolved_id": "1",
        "given_url": "http://foo.bar.com/entry/2018/1/1",
        "given_title": "foobarbazz",
        "favorite": "0",
        "status": "0",
        "time_added": "1544521412",
        "time_updated": "1544521412",
        "time_read": "0",
        "time_favorited": "0",
        "sort_id": 0,
        "resolved_title": "foobarbazz",
        "resolved_url": "http://foo.bar.com/entry/2018/1/1",
        "excerpt": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ...",
        "is_article": "1",
        "is_index": "0",
        "has_video": "0",
        "has_image": "1",
        "word_count": "792",
        "lang": "ja",
        "top_image_url": "https://foo.bar.com/foo.png",
        "listen_duration_estimate": 307
    }


def build_article_fixtures():
    acc = {str(i): build_article_fixture(str(i)) for i in range(1, 3)}
    return {
        'status': 1,
        'complete': 0,
        'list': acc,
        'error': None,
        'since': 1544633513
    }


def test_build_article():
    data = build_article_fixture()
    article = core.build_article(data)
    assert article
    assert article == core.Article(
        "1",
        "1",
        "http://foo.bar.com/entry/2018/1/1",
        "foobarbazz",
        "ja"
    )
    assert article.document == core.Document("")


@patch('biscuit.predict.core._post', return_value=build_article_fixtures())
def test_get_targets(mock):
    date = dt.datetime(2018, 12, 1)
    actual = core.get_targets(date)
    assert actual
    assert actual == [
        core.Article(
            "1",
            "1",
            "http://foo.bar.com/entry/2018/1/1",
            "foobarbazz",
            "ja"
        ),
        core.Article(
            "2",
            "1",
            "http://foo.bar.com/entry/2018/1/1",
            "foobarbazz",
            "ja"
        ),
    ]
