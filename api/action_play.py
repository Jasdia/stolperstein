import websockets
import os

from api.action_build import *

URL = os.getenv('URL')
KEY = os.getenv('KEY')
action_changed = 'true'
action = 'jfdkfj'

async with websockets.connect(f'{URL}?key={KEY}') as ws:
    play_map = ws.recv()

    if action_changed == 'true':
        ws.send(generated_json(f'{action}'))
    else:
        ws.send(calculated_json(f'{action}'))
