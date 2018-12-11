import datetime as dt
from typing import List, Dict
from dataclasses import dataclass, field


@dataclass
class Document:
    text: str


@dataclass
class Article:
    item_id: str
    resolved_id: str
    resolved_url: str
    resolved_title: str
    lang: str
    document: Document = field(default=Document(""))


def build_article(article_data: Dict) -> Article:
    return Article(
        article_data['item_id'],
        article_data['resolved_id'],
        article_data['resolved_url'],
        article_data['resolved_title'],
        article_data['lang'],
    )


def get_targets(date: dt.date) -> List[Article]:
    pass


def get_already_tagged_article() -> List[Article]:
    pass


def get_new_article(date: dt.date) -> List[Article]:
    pass
