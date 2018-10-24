import configparser
import base64
import hashlib
import hmac
import json
import time
from urllib.request import urlopen, Request


config = configparser.ConfigParser()
config.read("config.ini")
ACCESS_TOKEN = config["KEYS"]["ACCESS_KEY"]
SECRET_KEY = config["KEYS"]["SECRET_KEY"]
HOST = 'https://api.coinone.co.kr/'


def get_base_payload():
    return {
        'access_token': ACCESS_TOKEN,
    }


def str_2_byte(s, encode='utf-8'):
    return bytes(s, encode)


def get_encoded_payload(payload):
    payload['nonce'] = int(time.time() * 1000)
    dumped_json = json.dumps(payload)
    encoded_json = base64.b64encode(str_2_byte(dumped_json))
    return encoded_json


def get_signature(encoded_payload):
    signature = hmac.new(str_2_byte(SECRET_KEY.upper()), encoded_payload,
                         hashlib.sha512)
    return signature.hexdigest()


def get_response(url, payload):
    encoded_payload = get_encoded_payload(payload)
    signature = get_signature(encoded_payload)
    headers = {
        'Content-Type': 'application/json',
        'X-COINONE-PAYLOAD': encoded_payload,
        'X-COINONE-SIGNATURE': signature,
    }
    api_url = HOST + url
    req = Request(api_url, data=encoded_payload, headers=headers,
                  method='POST')
    with urlopen(req) as res:
        data = res.read().decode('utf-8')
        return json.loads(data)


def create_payload(data):
    payload = get_base_payload()
    payload.update(data)
    return payload


response = get_response('v2/order/complete_orders/', create_payload({
  'currency': 'btc',
}))
print(response)
