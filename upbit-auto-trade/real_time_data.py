import websocket, json, time, requests
import hashlib, jwt, uuid
from urllib.parse import urlencode
import os

try:
    import thread
except ImportError:
    import _thread as thread


access_key = '0wZ3tD2iNUVlP3mx3NYa1pXstBBcbmnXvDH6OsbP'
secret_key = 'p5Oqvd6XSM9Yyc0a5V9M4rl4XENRfReJ7MT1BuIM'

def on_message(ws, message):
    json_data = json.loads(message)
    print(json_data)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        ws.send(json.dumps(
            [{"ticket": "test"}, {"type": "ticker", "codes": ["KRW-BTC"]}]))
    thread.start_new_thread(run, ())


websocket.enableTrace(True)
ws = websocket.WebSocketApp("ws://api.upbit.com/websocket/v1",
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
ws.on_open = on_open
print(ws.on_open)
ws.run_forever()