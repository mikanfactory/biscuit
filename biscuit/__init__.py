import json


POCKET_CONFIG_FILE_PATH = './pocket_token/pocket_config.json'
POCKET_ACCESS_TOKEN_PATH = './pocket_token/pocket_access_token.json'
POCKET_REQUEST_TOKEN_PATH = './pocket_token/pocket_request_token.json'


with open(POCKET_ACCESS_TOKEN_PATH, 'r') as f:
    access_token = json.load(f)
