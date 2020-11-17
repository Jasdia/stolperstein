import os
from websockets import connect
from api.json_answer import calculated_json, generated_json
from json_mapping.json_class_mapper import map_json_to_dataclass

URL = os.getenv('URL')
KEY = os.getenv('KEY')
action_changed = 'true'
action = 'change_nothing'


async def start_ws():
    async with connect(f'{URL}?key={KEY}') as websocket:
        play_map = await websocket.recv()
        data_class = map_json_to_dataclass(play_map)
        print(data_class)

        if action_changed == 'true':
            await websocket.send(generated_json(f'{action}'))
        else:
            await websocket.send(calculated_json(f'{action}'))
