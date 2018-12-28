import re
import datetime as dt
from typing import List, Dict
from logging import getLogger
from dataclasses import dataclass

import requests

from biscuit import access_token

logger = getLogger(__name__)


@dataclass(frozen=True)
class Article:
    item_id: str
    resolved_id: str
    resolved_url: str
    resolved_title: str
    lang: str
    domain_metadata_name: str


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
    domain_metadata_name = extract_domain_metadata_name(article_data)
    return Article(
        article_data['item_id'],
        article_data['resolved_id'],
        article_data['resolved_url'],
        article_data['resolved_title'],
        article_data['lang'],
        domain_metadata_name
    )


def extract_domain_metadata_name(article_data: Dict) -> str:
    domain_metadata = article_data.get('domain_metadata', None)
    if domain_metadata:
        return domain_metadata.get('name', '')
    return ''


def get_targets(date: dt.datetime) -> List[Article]:
    params = {
        'contentType': 'article',
        'sort': 'newest',
        'detailType': 'simple',
        'tag': '_untagged_',
        'since': int(date.timestamp())
    }
    ret = _post('https://getpocket.com/v3/get', dict(**access_token, **params))
    return [build_article(v) for v in ret['list'].values()]


def download_document(article: Article) -> str:
    if _is_arXiv_pdf(article):
        url = re.sub(r'\/pdf\/', '/abs/', article.resolved_url)
        url = re.sub(r'\.pdf$', '', url)
        return requests.get(url).text

    return requests.get(article.resolved_url).text


def _is_arXiv_pdf(article: Article) -> bool:
    if article.domain_metadata_name and article.domain_metadata_name == 'arXiv':
        return bool(re.search('pdf$', article.resolved_url))
    return False
