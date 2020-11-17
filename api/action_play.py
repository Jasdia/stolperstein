import os
from websockets import connect
from api.json_answer import calculated_json, generated_json

URL = os.getenv('URL')
KEY = os.getenv('KEY')
action_changed = 'true'
action = 'change_nothing'


async def start_ws():
    async with connect(f'{URL}?key={KEY}') as websocket:
        play_map = await websocket.recv()
        print(play_map)

        if action_changed == 'true':
            await websocket.send(generated_json(f'{action}'))
        else:
            await websocket.send(calculated_json(f'{action}'))
