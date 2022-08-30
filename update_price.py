import re
import json
import time
import redis
import requests
import schedule


redis_client = redis.Redis(host='redis', port=6379, db=0)
pipe = redis_client.pipeline()


def update_price():
    headers = {
        "Content-Type": "application/json"
    }

    try:
        url = "https://api.binance.com/api/v3/ticker/24hr"
        response = requests.request("GET", url, headers=headers, data={})
        tickers = json.loads(response.text)

        for ticker in tickers:
            symbol = ticker['symbol']
            # isUSDT = re.search("USDT$", symbol)
            # if isUSDT:
            pipe.set(symbol, ticker['lastPrice'])

        # Insert bulk data in redis
        pipe.execute()
        print("Successfuly update token price ...")

    except Exception as e:
        print(e)


# Run every 30 s
schedule.every(0.5).minutes.do(update_price)

while True:
    schedule.run_pending()
    time.sleep(1)
