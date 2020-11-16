import os
import websockets

from api.json_answer import calculated_json, generated_json

URL = os.getenv('URL')
KEY = os.getenv('KEY')
action_changed = 'true'
action = 'blb'


async with websockets.connect(f'{URL}?key={KEY}') as ws:
    play_map = await ws.recv()

    if action_changed == 'true':
        ws.send(generated_json(f'{action}'))
    else:
        ws.send(calculated_json(f'{action}'))
