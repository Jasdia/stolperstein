import websockets
import asyncio
import os

URL = os.getenv('URL')
KEY = os.getenv('KEY')


def gen_json(action):
    action_play = '{"action": "' + action + '"}'
    return action_play


async with websockets.connect(f'{URL}?key={KEY}') as ws:
    ws.send(gen_json('turn_left'))
