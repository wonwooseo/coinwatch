import requests
import time


api_url = "https://api.coinone.co.kr/ticker/"
while True:
    res = requests.get(api_url, params={'currency': 'eth'})
    print(res.json()['last'])
    time.sleep(5)  # halt 5 seconds
