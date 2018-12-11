import json
from logging import getLogger, config

import yaml
import click
import requests
from typing import Dict, Tuple


with open("./conf/logging.yaml", 'r') as c:
    config.dictConfig(yaml.load(c))

logger = getLogger('scripts/auth')

POCKET_CONFIG_FILE_PATH = './pocket_token/pocket_config.json'
POCKET_ACCESS_TOKEN_PATH = './pocket_token/pocket_access_token.json'
POCKET_REQUEST_TOKEN_PATH = './pocket_token/pocket_request_token.json'


def _read_file(path: str) -> Dict:
    with open(path, 'r') as f:
        return json.load(f)


def _write_file(path: str, data: Dict) -> None:
    if path == POCKET_ACCESS_TOKEN_PATH:
        message = f'Access token saved to {path}.'
    elif path == POCKET_REQUEST_TOKEN_PATH:
        message = f'Request token saved to {path}.'
    else:
        raise ValueError("Trying to write wrong path.")

    with open(path, 'w+') as f:
        json.dump(data, f)
        logger.info(message)


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


def get_redirect_uri_and_code() -> Tuple:
    config = _read_file(POCKET_CONFIG_FILE_PATH)
    ret = _post('https://getpocket.com/v3/oauth/request', config)
    return config['redirect_uri'], ret['code']


def get_access_token_and_consumer_key() -> Tuple:
    request_token = _read_file(POCKET_REQUEST_TOKEN_PATH)

    config = _read_file(POCKET_CONFIG_FILE_PATH)
    config.pop('redirect_uri')
    params = dict(**config, **request_token)

    ret = _post('https://getpocket.com/v3/oauth/authorize', params)
    return ret['access_token'], config['consumer_key']


@click.group()
def cmd() -> None:
    pass


@cmd.command()
def generate_authroization_url() -> None:
    redirect_uri, code = get_redirect_uri_and_code()

    _write_file(POCKET_REQUEST_TOKEN_PATH, {'code': code})

    base_url = 'https://getpocket.com/auth/authorize'
    url = f'{base_url}?request_token={code}&redirect_uri={redirect_uri}'
    logger.info(f'Authorization URL generated: {url}')


@cmd.command()
def generate_access_token() -> None:
    access_token, consumer_key = get_access_token_and_consumer_key()
    _write_file(
        POCKET_ACCESS_TOKEN_PATH,
        {'access_token': access_token, 'consumer_key': consumer_key}
    )


@cmd.command()
def test_retrive() -> None:
    access_token = _read_file(POCKET_ACCESS_TOKEN_PATH)
    params = {
        'state': 'unread',
        'contentType': 'article',
        'count': 3
    }
    ret = _post('https://getpocket.com/v3/get', dict(**access_token, **params))
    print(json.dumps(ret))


def main() -> None:
    cmd()


if __name__ == '__main__':
    main()
