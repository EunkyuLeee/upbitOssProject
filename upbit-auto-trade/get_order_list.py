import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests

access_key = '7rSdvFyjJMB311tnLxvg2mV5oaHhtjg3Jx9I7cU8'
secret_key = 'x5ZUFGopyKLzsRlvo7j2kAx73j2QJrr09VxGxrVo'


def ordered_data():
    query = {
        'market': 'KRW-ETH',
        'state': 'done',
    }

    m = hashlib.sha512()
    m.update(urlencode(query).encode())
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key).decode('utf-8')
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get('https://api.upbit.com/v1/orders', params=query, headers=headers)

    print(res.json())

    return res