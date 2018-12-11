from biscuit.predict import core


def test_build_article():
    data = {
        "item_id": "1",
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
