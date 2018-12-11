import datetime as dt

from biscuit.predict import task


def test_add_tags_to_all_items():
    target_date = dt.datetime(2018, 12, 1)
    t = task.AddTagToAllArticles(target_date)
    assert t
