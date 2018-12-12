import datetime as dt
from typing import List, Dict
from logging import getLogger
from dataclasses import dataclass, field

import requests

from biscuit import access_token

logger = getLogger(__name__)


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


def _post(url: str, params: Dict) -> Dict:
    headers = {
        'content-type': 'application/json',
        'X-Accept': 'application/json'
    }
    resp = requests.post(url, json=params, headers=headers)

    if resp.status_code != 200:
        x_err = resp.headers['X-Error']
        message = f'Error occured during getting request token. HTTP Status: {resp.status_code}, X-Error: {x_err}'  # NOQA
        raise requests.exceptions.HTTPError(message)

    return resp.json()


def build_article(article_data: Dict) -> Article:
    return Article(
        article_data['item_id'],
        article_data['resolved_id'],
        article_data['resolved_url'],
        article_data['resolved_title'],
        article_data['lang']
    )


def get_targets(date: dt.datetime) -> List[Article]:
    params = {
        'contentType': 'article',
        'sort': 'newest',
        'detailType': 'simple',
        'since': int(date.timestamp())
    }
    ret = _post('https://getpocket.com/v3/get', dict(**access_token, **params))
    return [build_article(v) for v in ret['list'].values()]


def get_already_tagged_article() -> List[Article]:
    pass


def get_new_article(date: dt.datetime) -> List[Article]:
    pass
