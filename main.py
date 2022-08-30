import redis
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse


app = FastAPI()

redis_conn = redis.Redis(host='redis', port=6379, db=0)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Token price</title>
    </head>
    <body>
        <h1>Token price | Format(BaseAsset-QuoteAsset) => (ADA-BTC)</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        symbol = await websocket.receive_text()
        symbol_split = symbol.split("-")

        if symbol_split[1] != "USDT":
            base_asset = symbol_split[0] + "USDT"
            quote_asset = symbol_split[1] + "USDT"

            base_asset_price = redis_conn.get(base_asset)
            quote_assett_price = redis_conn.get(quote_asset)
            try:
                result_price = float(base_asset_price.decode('utf-8')) / float(quote_assett_price.decode('utf-8'))
            except ZeroDivisionError as e:
                result_price = 0
        else:
            result_price = redis_conn.get(symbol.replace("-", "")).decode('utf-8')
        await websocket.send_text(f"{symbol} : {result_price}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
