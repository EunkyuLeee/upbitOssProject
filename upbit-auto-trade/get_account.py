import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests

access_key = '7rSdvFyjJMB311tnLxvg2mV5oaHhtjg3Jx9I7cU8'
secret_key = 'x5ZUFGopyKLzsRlvo7j2kAx73j2QJrr09VxGxrVo'

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