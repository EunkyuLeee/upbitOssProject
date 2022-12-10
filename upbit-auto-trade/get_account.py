import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests

access_key = '0wZ3tD2iNUVlP3mx3NYa1pXstBBcbmnXvDH6OsbP'
secret_key = 'p5Oqvd6XSM9Yyc0a5V9M4rl4XENRfReJ7MT1BuIM'

def account_data():
    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, secret_key).decode('utf-8')
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get('https://api.upbit.com/v1/accounts', headers=headers)
    print(res.json())
    
    return res